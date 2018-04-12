package io.github.voxelbuster.winxdock.assets;

import io.github.voxelbuster.winxdock.util.Debug;

import java.awt.*;
import java.io.File;
import java.util.HashMap;

public class FontLoader {
    public static HashMap<String, Font> fontsMap = new HashMap<>();

    public static void loadFont(String resource) {
        Debug.log("Loading font " + resource);
        try {
            fontsMap.put(resource, Font.createFont(Font.TRUETYPE_FONT, new File("res/font/" + resource + ".ttf")));
        } catch (Exception e) {
            Debug.error("Error loading font " + resource);
            e.printStackTrace();
        }
    }
}
