var geom = require('./geometry.js');

function calcRot(centerPt, targetPt) {
  var theta = Math.atan2(targetPt.y - centerPt.y, targetPt.x - centerPt.x) + Math.PI/2.0;
  var angle = Math.toDegrees(theta);
  if (angle < 0) {
      angle += 360;
  }
  return angle;
}

function centerObject(childObj, parentObj) {
    return new geom.Point(parentObj.width / 2 - childObj.width / 2, parentObj.height / 2 - childObj.height / 2);
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

module.exports.calcRot = calcRot;
module.exports.centerObject = centerObject;
module.exports.sleep = sleep;