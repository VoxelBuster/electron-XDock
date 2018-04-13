package io.github.voxelbuster.protonservice.util;

import java.util.logging.Level;
import java.util.logging.Logger;

public class Debug {
    private static Logger log;
    static {
        log = Logger.getLogger("WinXDock");
        if (AppSettings.debug) {
            Logger.getGlobal().setLevel(Level.FINE);
            log.setLevel(Level.FINE);
        }
    }

    public static void log(String s) {
        log.log(Level.INFO, s);
    }

    public static void debug(String s) {
        log.log(Level.FINE, s);
    }

    public static void warn(String s) {
        log.log(Level.WARNING, s);
    }

    public static void error(String s) {
        log.log(Level.SEVERE, s);
    }

}
