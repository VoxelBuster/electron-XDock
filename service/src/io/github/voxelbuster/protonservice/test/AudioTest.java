package io.github.voxelbuster.protonservice.test;

import io.github.voxelbuster.protonservice.audio.AudioAPI;

// Some resource files are missing and this test case will not work as a result
@Deprecated
public class AudioTest {
    public static void main(String[] args) throws Exception {
        AudioAPI.initAudio();
        AudioAPI.stream("res/music/start.mp3");
    }
}
