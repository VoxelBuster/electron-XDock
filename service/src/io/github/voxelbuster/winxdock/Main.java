package io.github.voxelbuster.winxdock;

import io.github.voxelbuster.winxdock.assets.ConfigLoader;
import io.github.voxelbuster.winxdock.audio.AudioAPI;
import io.github.voxelbuster.winxdock.renderer.DockFrame;
import io.github.voxelbuster.winxdock.util.AppSettings;
import io.github.voxelbuster.winxdock.util.Debug;

import java.io.File;
import java.io.FileNotFoundException;

public class Main {
    public static void main(String args[]) {
        Debug.log("Starting WinXDock");
        Debug.log("Forcing hardware acceleration");
        System.setProperty("sun.java2d.opengl", "true");
        AppSettings.dataDir = System.getProperty("user.home") + "/WinXDock/data/";
        if (!new File(AppSettings.dataDir + "user/").isDirectory()) {
            Debug.log("Creating user data directory at " + AppSettings.dataDir + "user/");
            new File(AppSettings.dataDir + "user/music/").mkdirs();
            new File(AppSettings.dataDir + "user/res/").mkdirs();
            new File(AppSettings.dataDir + "user/logs/").mkdirs();
        }
        try {
            ConfigLoader.readAppSettings();
        } catch (Exception e) {
            Debug.error("App config file not found or caused a read error, generating.");
            e.printStackTrace();
            ConfigLoader.createAppSettings();
        }
        Debug.log("Starting audio system");
        try {
            AudioAPI.initAudio();
        } catch (Exception e) {
            e.printStackTrace();
        }
        Debug.log("Starting parent window");
        DockFrame df = new DockFrame();
    }
}
