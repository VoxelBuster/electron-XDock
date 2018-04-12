package io.github.voxelbuster.winxdock.renderer;

import javafx.geometry.Point2D;
import javafx.scene.shape.Ellipse;
import javafx.scene.shape.Line;

import java.awt.*;
import java.util.HashMap;

public class GUIRegistry {
    public enum EnumObjectShape {
        RECT,
        ELLIPSE,
        LINE,
        POINT
    }

    public static class GUIObject {
        private Rectangle dimension;
        private final EnumObjectShape shape;

        public GUIObject(Rectangle dim, EnumObjectShape shape) {
            this.dimension = dim;
            this.shape = shape;
        }

        public boolean isPointInBounds(Point p) {
            switch (shape) {
                case RECT:
                    if (dimension.contains(p)) {
                        return true;
                    } else {
                        return false;
                    }
                case LINE:
                    Line l = new Line(dimension.x, dimension.y, dimension.width, dimension.height);
                    if (l.contains(p.x, p.y)) {
                        return true;
                    } else {
                        return false;
                    }
                case POINT:
                    if (p.x == dimension.x && p.y == dimension.y) {
                        return true;
                    } else {
                        return false;
                    }
                case ELLIPSE:
                    Ellipse e = new Ellipse(dimension.x + dimension.width / 2, dimension.y + dimension.height / 2,
                            dimension.width / 2, dimension.height / 2);
                    if (e.contains(new Point2D(p.x, p.y))) {
                        return true;
                    } else {
                        return false;
                    }
                default:
                    return false;
            }
        }

        public void setRectangle(Rectangle rect) {
            this.dimension = rect;
        }
    }

    private static HashMap<String, GUIObject> objects = new HashMap<>();
    public static void register(GUIObject obj, String name) {
        objects.put(name, obj);
    }

    public static void remove(String name) {
        objects.remove(name);
    }

    public static GUIObject get(String name) {
        return objects.get(name);
    }
}
