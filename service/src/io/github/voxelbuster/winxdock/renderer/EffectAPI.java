package io.github.voxelbuster.winxdock.renderer;

import io.github.voxelbuster.winxdock.util.VoxMath;

import java.awt.*;
import java.awt.image.BufferedImage;
import java.awt.image.ConvolveOp;
import java.awt.image.Kernel;

public class EffectAPI {
    /**
     * Applies a convolution filter to the image with the given radius and returns the result.
     * @param source
     * @param radius
     * @return
     */
    public static BufferedImage blurImage(Image source, int radius) {
        int width = source.getWidth(null), height = source.getHeight(null);
        BufferedImage expanded = new BufferedImage(width + 2 * radius, height + 2 * radius, BufferedImage.TYPE_INT_ARGB);
        Graphics2D g = expanded.createGraphics();
        Point centered = VoxMath.centerObject(new Dimension(width, height),
                new Dimension(expanded.getWidth(), expanded.getHeight()));
        g.drawImage(source, centered.x, centered.y, null);
        int size = radius * 2 + 1;
        float weight = 1.0f / (size * size);
        float[] data = new float[size * size];

        for (int i = 0; i < data.length; i++) {
            data[i] = weight;
        }

        Kernel kernel = new Kernel(size, size, data);
        ConvolveOp op = new ConvolveOp(kernel, ConvolveOp.EDGE_NO_OP, null);
        return op.filter(expanded, null);
    }

    public static BufferedImage toBufferedImage(Image img)
    {
        if (img instanceof BufferedImage)
        {
            return (BufferedImage) img;
        }

        // Create a buffered image with transparency
        BufferedImage bimage = new BufferedImage(img.getWidth(null), img.getHeight(null), BufferedImage.TYPE_INT_ARGB);

        // Draw the image on to the buffered image
        Graphics2D bGr = bimage.createGraphics();
        bGr.drawImage(img, 0, 0, null);
        bGr.dispose();

        // Return the buffered image
        return bimage;
    }
}
