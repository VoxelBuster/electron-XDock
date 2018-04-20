package io.github.voxelbuster.protonservice.net;

import io.github.voxelbuster.protonservice.util.AppSettings;
import io.github.voxelbuster.protonservice.util.Debug;
import io.github.voxelbuster.protonservice.util.SystemAPI;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.ArrayList;

public class ProtonSocket {

    private ServerSocket serverSock = new ServerSocket(AppSettings.serverPort);

    private Socket socket;

    private BufferedReader serverIS;
    private DataOutputStream serverOS;

    public ProtonSocket() throws IOException {
        socket = serverSock.accept();
        serverIS = new BufferedReader(new InputStreamReader(socket.getInputStream()));
        serverOS = new DataOutputStream(socket.getOutputStream());

        ArrayList<String> outBuffer = new ArrayList<>();

        if (socket.isConnected()) {
            Debug.log("Connected to client");
            outBuffer.add("winBg;" + SystemAPI.readRegistry("HKEY_CURRENT_USER\\Control Panel\\Desktop", "WallPaper") + "\n");
            outBuffer.add("smPaths;" + genPathData(EnumPathData.PROGRAMS) + "\n");
            Thread inThread = new Thread(() -> {
                while (!ProtonSocket.this.isDead()) {
                    try {
                        Thread.sleep(5);
                        if (!serverIS.ready()) continue;
                        String inp = serverIS.readLine();
                        String[] buffer = inp.split("\n");
                        for (String msg : buffer) {
                            Debug.log("data_recv: " + msg);
                            if (msg.contains("get batStat")) {
                                outBuffer.add("batStat;" + genBatteryData() + "\n");
                            } else if (msg.equals("quit")) {
                                Debug.log("Client requested service shutdown...");
                                socket.close();
                            }
                        }
                    } catch (Exception e) {
                        Debug.error("Exception in service input thread:");
                        e.printStackTrace();
                    }
                }
            });
            Thread outThread = new Thread(() -> {
                while (!ProtonSocket.this.isDead()) {
                    try {
                        Thread.sleep(5);
                        while (!outBuffer.isEmpty()) {
                            serverOS.writeUTF(outBuffer.remove(0)); // Remove the top element until empty
                        }
                    } catch (Exception e) {
                        Debug.error("Exception in service output thread:");
                        e.printStackTrace();
                    }
                }
            });
            inThread.start();
            try {
                Thread.sleep(3);
            } catch (InterruptedException e) {
                Debug.error("Main thread sleep interrupted!");
                e.printStackTrace();
            }
            outThread.start();
        } else {
            new ProtonSocket();
            return;
        }
    }

    private String genBatteryData() {
        JSONObject root = new JSONObject();
        root.put("batteryLife", SystemAPI.getBattery());
        root.put("isCharging", SystemAPI.isCharging());
        root.put("hasBattery", SystemAPI.hasBattery());
        return root.toJSONString();
    }

    private enum EnumPathData {
        PROGRAMS,
        MUSIC,
        GAMES
    }

    private String genPathData (EnumPathData epd) {
        JSONObject root = new JSONObject();
        switch (epd) {
            case PROGRAMS:
                JSONArray pathArr = new JSONArray();
                for (String s : SystemAPI.startMenuPaths) {
                    pathArr.add(s);
                }
                root.put("paths", pathArr);
                break;
            case GAMES:
                break;
            case MUSIC:
                break;
            default:
                break;
        }
        return root.toJSONString();
    }

    public boolean isDead() {
        if ((socket.isOutputShutdown() && socket.isInputShutdown()) || socket.isClosed()) {
            return true;
        } else {
            return false;
        }
    }
}
