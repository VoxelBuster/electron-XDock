// This file is required by the index.html file and will
// be executed in the renderer process for that window.
// All of the Node.js APIs are available in this process.
var dockCanvas = document.getElementById('dockCanvas');
var ctx = dockCanvas.getContext('2d');
var cvWidth = dockCanvas.width;
var cvHeight = dockCanvas.height;

var imageMap = {
  centerCicle: document.getElementById('centerCicle')
};

const protonAPI = require('./protonAPI.js');
const appSettings = require('./appSettings.js');
const geom = require( './geometry.js');

function animate() {
  // call again next time we can draw
  while (true) {
    // clear canvas
    ctx.clearRect(0, 0, cvWidth, cvHeight);
    drawCenterCircle();
    ctx.fillStyle = '#ff0000';
    
    protonAPI.sleep(16); // Limit to 60fps
  }
}

function drawCenterCircle() {
  var centerCirclePt = protonAPI.centerObject(new geom.Rectangle(imageMap.centerCicle.width, imageMap.centerCicle.height), new geom.Rectangle(cvWidth, cvHeight));
  ctx.drawImage(imageMap.centerCicle, centerCirclePt.x, centerCirclePt.y,
    imageMap.centerCicle.width * appSettings.screenRatio, imageMap.centerCicle.height * appSettings.screenRatio);
  ctx.fillRect(200,200,100,100);
}

animate();
