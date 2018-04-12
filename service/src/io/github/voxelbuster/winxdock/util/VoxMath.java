package io.github.voxelbuster.winxdock.util;

import java.awt.*;

public class VoxMath {
    /**
     * Gets an angle between two points
     * @param centerPt
     * @param targetPt
     * @return
     */
    public static double calcRot(Point centerPt, Point targetPt)
    {
        double theta = Math.atan2(targetPt.y - centerPt.y, targetPt.x - centerPt.x) + Math.PI/2.0;
        double angle = Math.toDegrees(theta);
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
    public static Point centerObject(Dimension childObj, Dimension parentObj) {
        return new Point(parentObj.width / 2 - childObj.width / 2, parentObj.height / 2 - childObj.height / 2);
    }
}
