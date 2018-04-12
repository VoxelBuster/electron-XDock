package io.github.voxelbuster.winxdock.util;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.*;

public class Chrono implements ActionListener {
    JFrame frameToUpdate;

    public Chrono (JFrame frame) {
        Timer timer = new Timer(16, this); // Fixed to 60 fps
        this.frameToUpdate = frame;
        timer.start();
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        frameToUpdate.repaint();
    }
}
