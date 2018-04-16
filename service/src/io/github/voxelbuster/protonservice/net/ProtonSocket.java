package io.github.voxelbuster.protonservice.net;

import io.github.voxelbuster.protonservice.util.AppSettings;
import io.github.voxelbuster.protonservice.util.Debug;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.ArrayList;

public class ProtonSocket {

    private ServerSocket serverSock = new ServerSocket(AppSettings.serverPort);

    private Socket socket;

    private DataInputStream serverIS;
    private DataOutputStream serverOS;

    public ProtonSocket() throws IOException {
        socket = serverSock.accept();
        serverIS = new DataInputStream(socket.getInputStream());
        serverOS = new DataOutputStream(socket.getOutputStream());

        ArrayList<String> outBuffer = new ArrayList<>();

        if (socket.isConnected()) {
            serverOS.writeUTF("svc-conn\n"); // TODO finish protocol
            Thread inThread = new Thread(() -> {
                while (!ProtonSocket.this.isDead()) {
                    try {
                        Thread.sleep(5);
                        String inp = serverIS.readUTF();
                        String[] buffer = inp.split("\n");
                        for (String msg : buffer) {
                            if (msg.equals("get batStat")) {
                                // TODO send battery status json
                            } else if (msg.equals("quit")) {
                                Debug.log("Client requested service shutdown...");
                                socket.shutdownInput();
                                socket.shutdownOutput();
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
                        for (int i=outBuffer.size()-1;i>-1;i--) { // Longest waiting output is bottom of the list, most recent is 0.
                            serverOS.writeChars(outBuffer.remove(i));
                        }
                        serverOS.writeChars("test\n");
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

    public boolean isDead() {
        if (socket.isOutputShutdown() && socket.isInputShutdown()) {
            return true;
        } else {
            return false;
        }
    }
}
