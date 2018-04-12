package io.github.voxelbuster.winxdock.util;

import java.awt.*;

public class AppSettings {
    // Data Settings
    public static String dataDir = "";
    public static boolean debug = true;

    // UI Settings
    public static boolean time12Hr = true;

    // Graphics Settings
    public static double screenRatio = 2d/3d; // How much of the screen should the dock take up--relative to full screen
    public static boolean doubleBuffer = false, textGlow = true, fpsCounter = true;
    public static boolean background = false, useBgImage = true;
    public static Color bgColor = new Color(0x000000);
    public static Image bgImage = null;
}
