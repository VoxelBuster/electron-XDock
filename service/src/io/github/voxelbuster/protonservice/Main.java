package io.github.voxelbuster.protonservice;

import io.github.voxelbuster.protonservice.net.ProtonSocket;
import io.github.voxelbuster.protonservice.util.AppSettings;
import io.github.voxelbuster.protonservice.util.Debug;

public class Main {
    public static void main(String args[]) throws Exception {
        Debug.log("Starting protonService");

        Debug.log("Launching server socket");
        ProtonSocket ps = new ProtonSocket();

        if (!AppSettings.debug) {
           Runtime.getRuntime().exec("start runtime\\Python27\\python.exe electronUI.pyc");
        }

        while (!ps.isDead()) {
            Thread.sleep(1000); // Keeps Java from eating the CPU for no reason.
        }
    }
}
