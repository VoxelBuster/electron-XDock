// This file is required by the index.html file and will
// be executed in the renderer process for that window.
// All of the Node.js APIs are available in this process.
var imageMap, animations;

const protonAPI = require('./scripts/protonAPI.js');
const anim = require('./scripts/GUIAnimator.js');
const ps = require('./scripts/protonService.js');
const appSettings = require('./appSettings.js');
const $ = require('jquery');
const paper = require('paper');
const format = require('string-format');

var dockCanvas, ctx, cvWidth, cvHeight;

var currentFrame = 0;

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

  animations.centerBatteryFg.loop = true;

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
  protonAPI.sleep(1000/appSettings.fps); // Limit to 60fps

  //update animations
  animations.centerBatteryFg.advance();
}

function drawCenterCircle() {
  var ccRect = new paper.Rectangle(0,0,imageMap.centerCircle.width, imageMap.centerCircle.height);
  var centerCirclePt = protonAPI.centerObject(ccRect, new paper.Rectangle(0,0,cvWidth, cvHeight));
  ctx.drawImage(imageMap.centerCircle, centerCirclePt.x, centerCirclePt.y, ccRect.width, ccRect.height);
  // Do animation math
  var batteryCrop = ((ccRect.height / 2) * (1-ps.lastBatteryReading)) + 256;
  console.log(ps.lastBatteryReading);
  if (ps.isCharging) {
    ctx.globalAlpha = ((animations.centerBatteryFg.getCurrentFrame() + 1) % 30) / 30;
    if (animations.centerBatteryFg.getCurrentFrame() >= 30) {
      ctx.globalAlpha = ctx.globalAlpha * -1;
    }
  }
  // Draw the battery bar
  ctx.drawImage(imageMap.centerBatteryFg, 0, batteryCrop, ccRect.width, ccRect.height - batteryCrop, centerCirclePt.x, centerCirclePt.y + batteryCrop, ccRect.width, ccRect.height - batteryCrop);
  ctx.globalAlpha = 1;

  // Draw time string
  var centerPt = new paper.Point(cvWidth / 2, cvHeight / 2);
  var d = new Date();
  var sec = d.getSeconds(), min = d.getMinutes(), hr = d.getHours() % 12;

  if (hr == 0) {
    hr = 12;
  }

  ctx.textBaseline = 'middle';
  ctx.textAlign = 'center';
  ctx.shadowColor = "#00fbfe";
  ctx.shadowBlur = 10;
  ctx.font = format("bold {0}px 'Software Tester'", 152 * screenRatio);
  ctx.fillStyle = "#00fbfe";
  ctx.fillText(format("{0}:{1}", hr.toLocaleString('en-US', {minimumIntegerDigits: 2, useGrouping:false}),
  min.toLocaleString('en-US', {minimumIntegerDigits: 2, useGrouping:false})), centerPt.x, centerPt.y);
}
