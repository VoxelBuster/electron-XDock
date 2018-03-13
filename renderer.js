// This file is required by the index.html file and will
// be executed in the renderer process for that window.
// All of the Node.js APIs are available in this process.
var imageMap;

const protonAPI = require('./protonAPI.js');
// const appSettings = require('./appSettings.js');
const geom = require( './geometry.js');
const $ = require('jQuery');

var dockCanvas, ctx, cvWidth, cvHeight;

$(document).ready(function() {
  dockCanvas = document.getElementById('dockCanvas');
  ctx = dockCanvas.getContext('2d');
  cvWidth = dockCanvas.width;
  cvHeight = dockCanvas.height;
  preprocessImages();
  animate();
});

function preprocessImages() {
  imageMap = {
    centerCircle: document.getElementById('centerCircle')
  };

  imageMap.centerCircle.width *= screenRatio;
  imageMap.centerCircle.height *= screenRatio;
}

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
  var centerCirclePt = protonAPI.centerObject(new geom.Rectangle(0,0,imageMap.centerCircle.width, imageMap.centerCircle.height), new geom.Rectangle(0,0,cvWidth, cvHeight));
  ctx.drawImage(imageMap.centerCircle, centerCirclePt.x, centerCirclePt.y, imageMap.centerCircle.width, imageMap.centerCircle.height);
}
