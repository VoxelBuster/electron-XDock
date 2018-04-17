const net = require('net');
const protonAPI = require('./protonAPI.js');
const { StringDecoder } = require('string_decoder');

const decoder = new StringDecoder('utf8');

while (net == undefined || protonAPI == undefined) {}

var client = new net.Socket();

var dataInBuffer = '', lastBatteryJSON = {};
var retries = 0;

var lastBatteryReading = 0, hasBattery = true, isCharging = true;
var installedGames = [], installedApps = [], songs = [];

function init() {
      client.connect(19700, 'localhost', function() {
      	console.log('Connected to protonService');
        client.write('get batStat\n');
      });
}

client.on('data', function(data) {
  var array = [...data];
  array.splice(0,2);
  for (var i=0;i<array.length;i++) {
    dataInBuffer = dataInBuffer + String.fromCharCode(array[i]);
  }
  console.log(dataInBuffer);
  if (dataInBuffer.startsWith('batStat')) {
    lastBatteryJSON = JSON.parse(dataInBuffer.split(';')[1]);

  }
  dataInBuffer = '';
});

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
}

function updateBattery() {
  client.write('get batStat\n');
}

module.exports.lastBatteryReading = lastBatteryReading;
module.exports.hasBattery = hasBattery;
module.exports.isCharging = isCharging;
module.exports.installedGames = installedGames;
module.exports.installedApps = installedApps;
module.exports.songs = songs;

module.exports.init = init;
module.exports.disconnect = disconnect;
