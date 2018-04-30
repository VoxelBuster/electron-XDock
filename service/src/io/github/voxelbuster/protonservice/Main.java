package io.github.voxelbuster.protonservice;

import io.github.voxelbuster.protonservice.audio.AudioAPI;
import io.github.voxelbuster.protonservice.net.ProtonSocket;
import io.github.voxelbuster.protonservice.util.AppSettings;
import io.github.voxelbuster.protonservice.util.Debug;

import javax.swing.*;
import java.io.File;

public class Main {
    public static void main(String args[]) throws Exception {
        Debug.log("Starting protonService");
        UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
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

        Debug.log("Launching server socket");
        ProtonSocket ps = new ProtonSocket();

        while (!ps.isDead()) {

        }
    }
}
