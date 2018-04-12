package io.github.voxelbuster.winxdock.assets;

import io.github.voxelbuster.winxdock.util.Debug;

import javax.imageio.ImageIO;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.util.HashMap;

public class ImageLoader {
    public static HashMap<String, BufferedImage> imageMap = new HashMap<>();

    public static void loadGUI(String resource) {
        Debug.log("Loading resource " + resource);
        BufferedImage img = null;
        try {
            img = ImageIO.read(new File("res/ui/" + resource + ".png"));
        } catch (IOException e) {
            e.printStackTrace();
        }
        imageMap.put(resource, img);
    }

    public static Image get(String resource) {
        return imageMap.get(resource);
    }
}
