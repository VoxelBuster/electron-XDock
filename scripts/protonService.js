const net = require('net');

var client = new net.Socket();

function init() {
    client.connect(19700, '127.0.0.1', function() {
    	console.log('Connected to protonService');
    	//client.write('');
    });
}

client.on('data', function(data) {
  // Recieve data from server
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
