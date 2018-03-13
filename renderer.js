// This file is required by the index.html file and will
// be executed in the renderer process for that window.
// All of the Node.js APIs are available in this process.
var imageMap = {
  centerCicle: document.getElementById('centerCicle')
};

const protonAPI = require('./protonAPI.js');
const appSettings = require('./appSettings.js');
const geom = require( './geometry.js');
const $ = require('jQuery');

var dockCanvas, ctx, cvWidth, cvHeight;

$(document).ready(function() {
  dockCanvas = document.getElementById('dockCanvas');
  ctx = dockCanvas.getContext('2d');
  cvWidth = dockCanvas.width;
  cvHeight = dockCanvas.height;
  animate();
})

function animate() {
  // call again next time we can draw
  requestAnimationFrame(animate);
  // clear canvas
  ctx.clearRect(0, 0, cvWidth, cvHeight);
  drawCenterCircle();
  ctx.fillStyle = '#ff0000';
  
  protonAPI.sleep(16); // Limit to 60fps
}

function drawCenterCircle() {
  var centerCirclePt = protonAPI.centerObject(new geom.Rectangle(imageMap.centerCicle.width, imageMap.centerCicle.height), new geom.Rectangle(cvWidth, cvHeight));
  ctx.drawImage(imageMap.centerCicle, centerCirclePt.x, centerCirclePt.y,
    imageMap.centerCicle.width * appSettings.screenRatio, imageMap.centerCicle.height * appSettings.screenRatio);
}
