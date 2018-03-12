function Point(x,y) {
  this.x = x;
  this.y = y;
}

function Rectangle(x,y,width,height) {
  this.x = x;
  this.y = y;
  this.width = width;
  this.height = height;
}

module.exports.Point = Point;
module.exports.Rectangle = Rectangle;