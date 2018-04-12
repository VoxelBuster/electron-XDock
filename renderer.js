// This file is required by the index.html file and will
// be executed in the renderer process for that window.
// All of the Node.js APIs are available in this process.
var imageMap, animations;

const protonAPI = require('./scripts/protonAPI.js');
const anim = require('./scripts/GUIAnimator.js');
const protonService = require('./scripts/protonService.js');
const $ = require('jquery');
const paper = require('paper');
const format = require('string-format');

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
    centerCircle: document.getElementById('centerCircle'),
    centerBatteryFg: document.getElementById('centerBatteryFg')
  };

  animations = {
    centerBatteryFg: new anim.GUIAnimator(60)
  }

  imageMap.centerCircle.width *= screenRatio;
  imageMap.centerCircle.height *= screenRatio;
}

function animate() {
  // call again next time we can draw
  requestAnimationFrame(animate);
  // clear canvas
  ctx.clearRect(0, 0, cvWidth, cvHeight);
  ctx.fillStyle = "rgba(0,0,0,0)";
  ctx.imageSmoothingEnabled = false;
  ctx.beginPath();
  drawCenterCircle();
  ctx.closePath();
  protonAPI.sleep(16); // Limit to 60fps
}

function drawCenterCircle() {
  var ccRect = new paper.Rectangle(0,0,imageMap.centerCircle.width, imageMap.centerCircle.height);
  var centerCirclePt = protonAPI.centerObject(ccRect, new paper.Rectangle(0,0,cvWidth, cvHeight));
  ctx.drawImage(imageMap.centerCircle, centerCirclePt.x, centerCirclePt.y, ccRect.width, ccRect.height);
  ctx.drawImage(imageMap.centerBatteryFg, centerCirclePt.x, centerCirclePt.y, ccRect.width, ccRect.height);

  // Draw time string
  var centerPt = new paper.Point(cvWidth / 2, cvHeight / 2);
  var d = new Date();
  var sec = d.getSeconds(), min = d.getMinutes(), hr = d.getHours();

  ctx.textBaseline = 'middle';
  ctx.textAlign = 'center';
  ctx.shadowColor = "#00fbfe";
  ctx.shadowBlur = 10;
  ctx.font = format("bold {0}px 'Software Tester'", 152 * screenRatio);
  ctx.fillStyle = "#00fbfe";
  ctx.fillText(format("{0}:{1}", hr.toLocaleString('en-US', {minimumIntegerDigits: 2, useGrouping:false}),
  min.toLocaleString('en-US', {minimumIntegerDigits: 2, useGrouping:false})), centerPt.x, centerPt.y);
}
