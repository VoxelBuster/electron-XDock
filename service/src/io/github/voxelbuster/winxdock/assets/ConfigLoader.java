package io.github.voxelbuster.winxdock.assets;

import io.github.voxelbuster.winxdock.util.AppSettings;
import io.github.voxelbuster.winxdock.util.Debug;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

import java.awt.*;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.lang.reflect.Field;

public class ConfigLoader {
    public static void readAppSettings() throws IOException, ParseException, IllegalAccessException {
        JSONParser parser = new JSONParser();
        JSONObject root = (JSONObject) parser.parse(new FileReader(new File(AppSettings.dataDir + "appsettings.json")));
        Field[] settings = AppSettings.class.getDeclaredFields();
        for (Field pref : settings) {
            if (pref.getType() == Color.class) {
                Color c = new Color(Math.toIntExact((Long) root.get(pref.getName())));
                pref.set(pref.getName(), c);
            } else {
                pref.set(pref.getName(), root.get(pref.getName()));
            }
        }
    }

    /**
     * Uses reflection to write AppSettings into a json file.
     */
    public static void createAppSettings() {
        Debug.log("Creating appsettings.json");
        File f = new File(AppSettings.dataDir + "appsettings.json");
        JSONObject root = new JSONObject();
        try {
            f.createNewFile();
            Field[] setttings = AppSettings.class.getDeclaredFields();
            for (Field pref : setttings) {
                if (pref.getType() == Boolean.class) {
                    root.put(pref.getName(), pref.getBoolean(null));
                } else if (pref.getType() == Integer.class) {
                    root.put(pref.getName(), pref.getInt(null));
                } else if (pref.getType() == String.class) {
                    root.put(pref.getName(), pref.get(null).toString());
                } else if (pref.getType() == Color.class) {
                    root.put(pref.getName(), ((Color) pref.get(null)).getRGB());
                } else {
                    root.put(pref.getName(), pref.get(null));
                }
            }
            FileWriter writer = new FileWriter(new File(AppSettings.dataDir + "appsettings.json"));
            root.writeJSONString(writer);
            writer.close();
        } catch (Exception e) {
            Debug.error("Error creating appsettings.json");
            e.printStackTrace();
        }
    }
}
