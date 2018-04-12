package io.github.voxelbuster.winxdock.audio;

import com.badlogic.audio.analysis.FFT;
import com.badlogic.audio.io.AudioDevice;
import com.badlogic.audio.io.MP3Decoder;
import com.badlogic.audio.io.WaveDecoder;

import java.io.File;
import java.io.FileInputStream;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;

public class AudioAPI {

    private static AudioDevice device;
    private static HashMap<String, ArrayList<ArrayList<Float>>> soundsMap = new HashMap<>();

    /**
     * Generates a two-dimensional list of audio samples in blocks of 1024
     * @param filename String
     * @return samples - float[][]
     * @throws Exception
     */
    public static ArrayList<ArrayList<Float>> readSamples(String filename) throws Exception {
        File waveFile = new File(filename);
        FileInputStream fis = new FileInputStream(waveFile);
        if (filename.endsWith(".wav")) {
            WaveDecoder decoder = new WaveDecoder(fis);
            ArrayList<ArrayList<Float>> sampleBlockList = new ArrayList<>();
            float[] samples = new float[1024];
            while (decoder.readSamples(samples) > 0) {
                ArrayList<Float> temp = new ArrayList<>();
                Float[] convList = new Float[1024];
                for (int i=0;i<convList.length;i++) {
                    convList[i] = samples[i];
                }
                Collections.addAll(temp, convList);
                sampleBlockList.add(temp);
            }
            return sampleBlockList;
        } else if (filename.endsWith(".mp3")) {
            MP3Decoder decoder = new MP3Decoder(fis);
            ArrayList<ArrayList<Float>> sampleBlockList = new ArrayList<>();
            float[] samples = new float[1024];
            while (decoder.readSamples(samples) > 0) {
                ArrayList<Float> temp = new ArrayList<>();
                Float[] convList = new Float[1024];
                for (int i=0;i<convList.length;i++) {
                    convList[i] = samples[i];
                }
                Collections.addAll(temp, convList);
                sampleBlockList.add(temp);
            }
            return sampleBlockList;
        } else {
            return new ArrayList<>();
        }
    }

    /**
     * Gets audio frequencies of a sound
     * @param filename
     * @return
     * @throws Exception
     */
    public static List<Float> getFrequencies(String filename) throws Exception {
        File waveFile = new File(filename);
        FileInputStream fis = new FileInputStream(waveFile);

        FFT fft = new FFT( 1024, 44100 );
        float[] samples = new float[1024];
        float[] spectrum = new float[1024 / 2 + 1];
        float[] lastSpectrum = new float[1024 / 2 + 1];
        List<Float> spectralFlux = new ArrayList<Float>( );

        if (filename.endsWith(".wav")) {
            WaveDecoder decoder = new WaveDecoder(fis);
            while( decoder.readSamples( samples ) > 0 )
            {
                fft.forward( samples );
                System.arraycopy( spectrum, 0, lastSpectrum, 0, spectrum.length );
                System.arraycopy( fft.getSpectrum(), 0, spectrum, 0, spectrum.length );

                float flux = 0;
                for( int i = 0; i < spectrum.length; i++ )
                    flux += (spectrum[i] - lastSpectrum[i]);
                spectralFlux.add( flux );
            }
        } else if (filename.endsWith(".mp3")) {
            MP3Decoder decoder = new MP3Decoder(fis);
            while (decoder.readSamples(samples) > 0) {
                fft.forward(samples);
                System.arraycopy(spectrum, 0, lastSpectrum, 0, spectrum.length);
                System.arraycopy(fft.getSpectrum(), 0, spectrum, 0, spectrum.length);

                float flux = 0;
                for (int i = 0; i < spectrum.length; i++)
                    flux += (spectrum[i] - lastSpectrum[i]);
                spectralFlux.add(flux);
            }
        }
        return spectralFlux;
    }

    public static void initAudio() throws Exception {
        device = new AudioDevice();
    }

    public static AudioDevice getDevice() {
        return device;
    }

    public static void play(String name) throws Exception {
        ArrayList<ArrayList<Float>> samples = soundsMap.get(name);
        for (ArrayList<Float> sample : samples) {
            float[] convList = new float[1024];
            for (int i=0;i<convList.length;i++) {
                convList[i] = sample.get(i);
            }
            device.writeSamples(convList);
        }
    }

    public static ArrayList<ArrayList<Float>> getSamples(String name) {
        return soundsMap.get(name);
    }

    public static void load(String name, String filename) throws Exception {
        soundsMap.put(name, readSamples(filename));
    }

    /**
     * Streams an audio file from disk and plays it in a separate thread.
     * @param filename
     */
    public static void stream(String filename) {
        new Thread(() -> {
            if (filename.endsWith(".mp3")) {
                MP3Decoder decoder = null;
                try {
                    decoder = new MP3Decoder(new FileInputStream(filename));
                } catch (Exception e) {
                    e.printStackTrace();
                }
                float[] samples = new float[1024];
                while (decoder.readSamples(samples) > 0) {
                    device.writeSamples(samples);
                }
            } else {
                WaveDecoder decoder = null;
                try {
                    decoder = new WaveDecoder(new FileInputStream(filename));
                } catch (Exception e) {
                    e.printStackTrace();
                }
                float[] samples = new float[1024];
                while (decoder.readSamples(samples) > 0) {
                    device.writeSamples(samples);
                }
            }
        }).start();
    }
}
