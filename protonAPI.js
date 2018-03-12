function calcRot(centerPt, targetPt) {
  var theta = Math.atan2(targetPt.y - centerPt.y, targetPt.x - centerPt.x) + Math.PI/2.0;
  var angle = Math.toDegrees(theta);
  if (angle < 0) {
      angle += 360;
  }
  return angle;
}

    /**
     * Gives a point that centers the child dimension inside of the parent
     * @param childObj Child dimension
     * @param parentObj Parent dimension
     * @return centered Point
     */
function centerObject(childObj, parentObj) {
    return new Point(parentObj.width / 2 - childObj.width / 2, parentObj.height / 2 - childObj.height / 2);
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
