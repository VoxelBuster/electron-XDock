package io.github.voxelbuster.winxdock.test;

import io.github.voxelbuster.winxdock.audio.AudioAPI;

public class AudioTest {
    public static void main(String[] args) throws Exception {
        AudioAPI.initAudio();
        AudioAPI.stream("res/music/start.mp3");
    }
}
