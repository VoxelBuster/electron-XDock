const net = require('net');
const protonAPI = require('./protonAPI.js');

var client = new net.Socket();

var dataInBuffer = '';

function init() {
    client.connect(19700, '127.0.0.1', function() {
    	console.log('Connected to protonService');
      protonAPI.sleep(500);
      client.write('quit'.toString('utf8'));
      client.end();
    });
}

client.on('data', function(data) {
  if (data != '\n') {
    dataInBuffer = dataInBuffer + data;
  } else {
    console.log('data_recv: ' + dataInBuffer + '\r\n');
    dataInBuffer = '';
  }
});

client.on('close', function() {
	// Disconnected from server
});

var lastBatteryReading = 0, hasBattery = true, isCharging = true;

var installedGames = [], installedApps = [], songs = [];


module.exports.lastBatteryReading = lastBatteryReading;
module.exports.hasBattery = hasBattery;
module.exports.isCharging = isCharging;
module.exports.installedGames = installedGames;
module.exports.installedApps = installedApps;
module.exports.songs = songs;

module.exports.init = init;
