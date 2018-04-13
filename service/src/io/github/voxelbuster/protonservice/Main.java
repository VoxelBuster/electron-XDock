package io.github.voxelbuster.protonservice;

import io.github.voxelbuster.protonservice.audio.AudioAPI;
import io.github.voxelbuster.protonservice.util.AppSettings;
import io.github.voxelbuster.protonservice.util.Debug;

import java.io.File;

public class Main {
    public static void main(String args[]) {
        Debug.log("Starting protonService");
        AppSettings.dataDir = System.getProperty("user.home") + "/electronXDock/data/";
        if (!new File(AppSettings.dataDir + "user/").isDirectory()) {
            Debug.log("Creating user data directory at " + AppSettings.dataDir + "user/");
            new File(AppSettings.dataDir + "user/music/").mkdirs();
            new File(AppSettings.dataDir + "user/res/").mkdirs();
            new File(AppSettings.dataDir + "user/logs/").mkdirs();
        }
        Debug.log("Starting audio system");
        try {
            AudioAPI.initAudio();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
