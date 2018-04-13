package io.github.voxelbuster.protonservice.net;

import io.github.voxelbuster.protonservice.util.AppSettings;

import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;

public class ProtonSocket {

    private ServerSocket serverSock = new ServerSocket(AppSettings.serverPort);

    private Socket socket;

    private DataInputStream serverIS;
    private DataOutputStream serverOS;

    public ProtonSocket() throws IOException {
        socket = serverSock.accept();
        serverIS = new DataInputStream(socket.getInputStream());
        serverOS = new DataOutputStream(socket.getOutputStream());

        if (socket.isConnected()) {
            serverOS.writeUTF("svc-conn"); // TODO finish protocol
        } else {
            new ProtonSocket();
            return;
        }
    }
}
