package io.github.voxelbuster.protonservice;

import io.github.voxelbuster.protonservice.audio.AudioAPI;
import io.github.voxelbuster.protonservice.net.ProtonSocket;
import io.github.voxelbuster.protonservice.util.Debug;

public class Main {
    public static void main(String args[]) throws Exception {
        Debug.log("Starting protonService");
//        UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
        Debug.log("Starting audio system");
        try {
            AudioAPI.initAudio();
        } catch (Exception e) {
            e.printStackTrace();
        }

        Debug.log("Launching server socket");
        ProtonSocket ps = new ProtonSocket();

//        if (!AppSettings.debug) {
//           Runtime.getRuntime().exec("python ..\\electronUI.py");
//        }

        while (!ps.isDead()) {

        }
    }
}
