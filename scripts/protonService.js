const net = require('net');
const protonAPI = require('./protonAPI.js');
const { StringDecoder } = require('string_decoder');
const globals = require('./globals.js');
const decoder = new StringDecoder('utf8');

while (net == undefined || protonAPI == undefined) {}

var client = new net.Socket();

var dataInBuffer = '', lastBatteryJSON = {};
var retries = 0;
var connected = false;

function init() {
      client.connect(19700, 'localhost', function() {
        connected = true;
      	console.log('Connected to protonService');
        client.write('get batStat\n');
      });
}

client.on('close', function() {
	protonAPI.quit();
});

client.on('error', function(err) {
  console.log('Service socket error!')
  console.log(err);
  if (err.code == 'ECONNREFUSED') {
    console.log('Could not establish connection to service. Aborting app.');
    protonAPI.quit();
  }
  else if (err.code == 'ECONNRESET') {
    console.log('Service forcibly closed the connection. Aborting app.');
    protonAPI.quit();
  }
});

function disconnect() {
  client.end('quit');
  connected = false;
}

function isConnected() {
  return connected;
}

function updateBattery() {
  client.write('get batStat\n');
    client.on('data', (data) => {
      var array = [...data];
      array.splice(0,2);
      for (var i=0;i<array.length;i++) {
        dataInBuffer = dataInBuffer + String.fromCharCode(array[i]);
      }
      console.log(dataInBuffer);
      if (dataInBuffer.startsWith('batStat')) {
        let lastBatteryJSON = JSON.parse(dataInBuffer.split(';')[1]);
        module.exports.hasBattery = lastBatteryJSON.hasBattery == 'true';
        module.exports.isCharging = lastBatteryJSON.isCharging == 'true';
        module.exports.lastBatteryReading = parseFloat(lastBatteryJSON.batteryLife);
      }
      dataInBuffer = '';
    });
}

module.exports.lastBatteryReading = 0;
module.exports.hasBattery = true;
module.exports.isCharging = false;

module.exports.installedGames = {};
module.exports.installedApps = {};
module.exports.songs = {};

module.exports.init = init;
module.exports.disconnect = disconnect;
module.exports.isConnected = isConnected;
module.exports.updateBattery = updateBattery;
