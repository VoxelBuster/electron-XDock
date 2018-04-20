package io.github.voxelbuster.protonservice.util;

import com.sun.deploy.util.WinRegistry;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;

/**
 * Various methods for interacting with the Windows OS or kernel. Most of these functions will probably break on non-Windows systems.
 */
public class SystemAPI {
    public static final String startMenuPath = "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\";
    // TODO get installed programs from start menu dir

    public static double getBattery() {
        Kernel32.SYSTEM_POWER_STATUS powerStatus = new Kernel32.SYSTEM_POWER_STATUS();
        Kernel32.INSTANCE.GetSystemPowerStatus(powerStatus);
        if (powerStatus.BatteryLifePercent < 0) {
            return 1d; // If there's negative battery there probably isn't a battery.
        } else {
            return ((double) powerStatus.BatteryLifePercent) / 100d;
        }
    }

    public static boolean isCharging() {
        Kernel32.SYSTEM_POWER_STATUS powerStatus = new Kernel32.SYSTEM_POWER_STATUS();
        Kernel32.INSTANCE.GetSystemPowerStatus(powerStatus);
        return powerStatus.ACLineStatus == 1;
    }

    public static boolean hasBattery() {
        return !(getBattery() < 0d);
    }

    public static String[] runProcessForOutput(String cmds) throws IOException, InterruptedException {
        Process proc = Runtime.getRuntime().exec(cmds);
        Debug.log("Waiting for command process...");
        proc.waitFor();
        InputStreamReader isr = new InputStreamReader(proc.getInputStream());
        BufferedReader stringReader = new BufferedReader(isr);
        ArrayList<String> strList = new ArrayList<>();
        while (stringReader.ready()) {
            strList.add(stringReader.readLine());
        }
        return strList.toArray(new String[0]);
    }

    public static String readRegistry(String path, String key) {
        int root;
        if (path.toUpperCase().startsWith("HKEY_CURRENT_USER")) {
            root = WinRegistry.HKEY_CURRENT_USER;
            path = path.replace("HKEY_CURRENT_USER\\","");
        } else if (path.toUpperCase().startsWith("HKEY_CLASSES_ROOT")) {
            root = WinRegistry.HKEY_CLASSES_ROOT;
            path = path.replace("HKEY_CLASSES_ROOT\\","");
        } else if (path.toUpperCase().startsWith("HKEY_CURRENT_CONFIG")) {
            root = WinRegistry.HKEY_CURRENT_CONFIG;
            path = path.replace("HKEY_CURRENT_CONFIG\\","");
        } else if (path.toUpperCase().startsWith("HKEY_DYN_DATA")) {
            root = WinRegistry.HKEY_DYN_DATA;
            path = path.replace("HKEY_DYN_DATA\\","");
        } else if (path.toUpperCase().startsWith("HKEY_LOCAL_MACHINE")) {
            root = WinRegistry.HKEY_LOCAL_MACHINE;
            path = path.replace("HKEY_LOCAL_MACHINE\\","");
        } else if (path.toUpperCase().startsWith("HKEY_PERFORMANCE_DATA")) {
            root = WinRegistry.HKEY_PERFORMANCE_DATA;
            path = path.replace("HKEY_PERFORMANCE_DATA\\","");
        } else if (path.toUpperCase().startsWith("HKEY_USERS")) {
            root = WinRegistry.HKEY_USERS;
            path = path.replace("HKEY_USERS\\","");
        } else {
            root = WinRegistry.HKEY_LOCAL_MACHINE;
            path = path.substring(path.indexOf("\\") + 1);
        }
        return WinRegistry.getString(root, path, key);
    }
}
