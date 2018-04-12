package io.github.voxelbuster.winxdock.renderer;

import com.jogamp.opengl.GLAutoDrawable;
import com.jogamp.opengl.GLCapabilities;
import com.jogamp.opengl.GLEventListener;
import com.jogamp.opengl.GLProfile;
import com.jogamp.opengl.awt.GLJPanel;
import io.github.voxelbuster.winxdock.assets.FontLoader;
import io.github.voxelbuster.winxdock.assets.ImageLoader;
import io.github.voxelbuster.winxdock.util.*;

import javax.imageio.ImageIO;
import javax.swing.*;
import java.awt.*;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.awt.event.MouseMotionListener;
import java.awt.geom.AffineTransform;
import java.awt.image.AffineTransformOp;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.util.Calendar;
import java.util.Date;

import static io.github.voxelbuster.winxdock.assets.ImageLoader.imageMap;

public class DockFrame extends JFrame {
    private Toolkit tk = Toolkit.getDefaultToolkit();
    private int mouseX;
    private int mouseY;

    private Point screenCenter;

    private int selectorRotation = 0;
    private boolean centerSelect = false;

    public static DockCanvas innerCanvas;

    public DockFrame() {
        super("WinXDock");
        GraphicsEnvironment ge = GraphicsEnvironment.getLocalGraphicsEnvironment();
        GraphicsDevice gd = ge.getDefaultScreenDevice();
        GLProfile glprofile = GLProfile.getDefault();
        GLCapabilities glcapabilities = new GLCapabilities(glprofile);
        setIconImage(new ImageIcon("res/ico/appicon.png").getImage());
        setSize(new Dimension(tk.getScreenSize().width, tk.getScreenSize().height));
        setUndecorated(true);
        innerCanvas = new DockCanvas(glcapabilities);
        setContentPane(innerCanvas);
        setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
        if (AppSettings.background) {
            setBackground(AppSettings.bgColor);
        } else {
            setBackground(new Color(0, 0, 0, 0));
        }

        if (!gd.isWindowTranslucencySupported(GraphicsDevice.WindowTranslucency.TRANSLUCENT)) {
            Debug.error("Translucency is not supported");
            System.exit(1);
        }
        loadUI();
        loadFonts();

        registerUI();
        registerAnimations();

        setVisible(true);

        screenCenter = new Point(getWidth() / 2, getHeight() / 2);

        new Chrono(this); // Start custom repaint timer

        addMouseMotionListener(new MouseMotionListener() {
            @Override
            public void mouseDragged(MouseEvent e) {
                mouseX = e.getX();
                mouseY = e.getY();
            }

            @Override
            public void mouseMoved(MouseEvent e) {
                mouseX = e.getX();
                mouseY = e.getY();
                Point m = new Point(mouseX, mouseY);
                GUIAnimator centerPulse = AnimationRegistry.getAnimator("centerPulse");
                if (GUIRegistry.get("centerCircle").isPointInBounds(m)) {
                    centerPulse.setReverse(false);
                    centerSelect = false;
                } else {
                    if (GUIRegistry.get("centerMenu").isPointInBounds(m)) {
                        centerSelect = true;
                        double angle = VoxMath.calcRot(screenCenter, m);
                        System.out.println(angle);
                    } else {
                        centerSelect = false;
                    }
                    centerPulse.setReverse(true);
                }
            }
        });

        addMouseListener(new MouseListener() {
            @Override
            public void mouseClicked(MouseEvent e) {
                mouseX = e.getX();
                mouseY = e.getY();
                Point m = new Point(mouseX, mouseY);
                GUIAnimator centerMenu = AnimationRegistry.getAnimator("centerMenu");
                if (GUIRegistry.get("centerCircle").isPointInBounds(m)) {
                    if (centerMenu.getReverse()) {
                        centerMenu.setReverse(false);
                    } else {
                        centerMenu.setReverse(true);
                    }
                }
            }

            @Override
            public void mousePressed(MouseEvent e) {

            }

            @Override
            public void mouseReleased(MouseEvent e) {

            }

            @Override
            public void mouseEntered(MouseEvent e) {

            }

            @Override
            public void mouseExited(MouseEvent e) {
                mouseX = 0;
                mouseY = 0;
                centerSelect = false;
            }
        });
    }

    private void registerAnimations() {
        AnimationRegistry.register(new GUIAnimator(60), "chargingFade");
        GUIAnimator centerPulse = new GUIAnimator(5);
        centerPulse.setLoop(false);
        AnimationRegistry.register(centerPulse, "centerPulse");
        GUIAnimator centerMenu = new GUIAnimator(10);
        centerMenu.setLoop(false);
        centerMenu.setReverse(true);
        AnimationRegistry.register(centerMenu, "centerMenu");
    }

    private void registerUI() {
        GUIRegistry.register(new GUIRegistry.GUIObject(new Rectangle(0,0,0,0), GUIRegistry.EnumObjectShape.ELLIPSE), "centerCircle");
        GUIRegistry.register(new GUIRegistry.GUIObject(new Rectangle(0,0,0,0), GUIRegistry.EnumObjectShape.ELLIPSE), "centerMenu");
    }

    private void loadUI() {
        ImageLoader.loadGUI("centercircle");
        ImageLoader.loadGUI("center_battery_fg");
        ImageLoader.loadGUI("center_menu_bg");
        ImageLoader.loadGUI("center_menu_select");
        if (AppSettings.useBgImage) {
            try {
                String path = SystemAPI.readRegistry("HKEY_CURRENT_USER\\Control Panel\\Desktop", "Wallpaper");
                Debug.log("Found desktop wallpaper: " + path);
                AppSettings.bgImage = ImageIO.read(new File(path));
            } catch (IOException e) {
                Debug.error("Registry or file read error");
                e.printStackTrace();
            }
        }
    }

    private void loadFonts() {
        FontLoader.loadFont("header");
        FontLoader.loadFont("monospace");
    }

    // START DOCK CANVAS CLASS
    private class DockCanvas extends GLJPanel {
        long oldTime;
        int oldMin = 0;

        public DockCanvas(GLCapabilities gc) {
            super(gc);
            setIgnoreRepaint(true);
            setDoubleBuffered(AppSettings.doubleBuffer);
            oldTime = System.currentTimeMillis();
            addGLEventListener(new GLEventListener() {
                @Override
                public void init(GLAutoDrawable glAutoDrawable) {

                }

                @Override
                public void dispose(GLAutoDrawable glAutoDrawable) {

                }

                @Override
                public void display(GLAutoDrawable glAutoDrawable) {
                    GLAPI.render( glAutoDrawable.getGL().getGL2(), glAutoDrawable.getSurfaceWidth(), glAutoDrawable.getSurfaceHeight() );
                }

                @Override
                public void reshape(GLAutoDrawable glAutoDrawable, int x, int y, int width, int height) {
                    GLAPI.setup( glAutoDrawable.getGL().getGL2(), width, height );
                }
            });
        }

        @Override
        public void paintComponent(Graphics g) {
            long start = System.currentTimeMillis();
            AnimationRegistry.getAnimator("chargingFade").advance();
            if (AppSettings.background && AppSettings.useBgImage) {
                g.drawImage(AppSettings.bgImage, 0, 0, this); // Draw background
            }

            drawCenterCircle(g);

            g.setColor(Color.GREEN);
            g.setFont(new Font("Arial", Font.BOLD, 24));

            long frametime = start - oldTime;
            oldTime = start;
            if (frametime != 0 && AppSettings.fpsCounter) {
                g.drawString(1000 / frametime + " fps", 20, 20);
            }

        }

        Dimension centerCircle, timeBaseDim, timeDim;
        Point centeredPos;
        Image scaledCenterCircle, scaledCenterMenu, scaledBatteryFg, blurredTimeImg, scaledMenuSelect;
        BufferedImage fgImg, timeImg;

        boolean imagesProcessed = false;
        int timeBlurRadius = 20;

        /**
         * All of the drawing functions that are really expensive to execute
         */
        private void reprocessUI() {
            // Center circle functions
            double h = getHeight(), dim1 = h * AppSettings.screenRatio;
            centerCircle = new Dimension((int) dim1, (int) dim1);
            centeredPos = VoxMath.centerObject(centerCircle, getSize());
            GUIRegistry.register(new GUIRegistry.GUIObject(new Rectangle(centeredPos.x,centeredPos.y,centerCircle.width,centerCircle.height), GUIRegistry.EnumObjectShape.ELLIPSE), "centerCircle");
            Point ccPt = VoxMath.centerObject(new Dimension((int) (getWidth() * 1.5),
                    (int) (getHeight() * 1.5)), new Dimension(getWidth(), getHeight()));
            GUIRegistry.register(new GUIRegistry.GUIObject(new Rectangle(ccPt.x,ccPt.y,(int) (getWidth() * 1.5),
                    (int) (getHeight() * 1.5)), GUIRegistry.EnumObjectShape.ELLIPSE), "centerMenu");
            scaledCenterCircle = imageMap.get("centercircle").getScaledInstance(centerCircle.width, centerCircle.height, Image.SCALE_DEFAULT);
            scaledCenterMenu = imageMap.get("center_menu_bg").getScaledInstance(centerCircle.width, centerCircle.height, Image.SCALE_DEFAULT);
            scaledMenuSelect = imageMap.get("center_menu_select").getScaledInstance((int)(centerCircle.width * 1.44), (int)(centerCircle.height * 1.44), Image.SCALE_DEFAULT);
            scaledBatteryFg = imageMap.get("center_battery_fg").getScaledInstance(centerCircle.width, centerCircle.height, Image.SCALE_DEFAULT);

            // Center time functions
            timeBaseDim = new Dimension(630, 110);
            timeDim = new Dimension((int) (timeBaseDim.width * AppSettings.screenRatio), (int) (timeBaseDim.height * AppSettings.screenRatio));
            timeImg = new BufferedImage(timeBaseDim.width, timeBaseDim.height, BufferedImage.TYPE_INT_ARGB);
            Graphics2D timeG = timeImg.createGraphics();
            Font timeFont = FontLoader.fontsMap.get("monospace");
            Date d = Calendar.getInstance().getTime();
            int hour = d.getHours(), min = d.getMinutes();
            if (AppSettings.time12Hr) {
                hour = d.getHours() % 12;
                if (hour == 0) {
                    hour = 12;
                }
            }
            timeG.setColor(new Color(0x00fbfe));
            timeG.setFont(timeFont.deriveFont(196f).deriveFont(Font.BOLD));
            timeG.drawString(String.format("%02d", hour) + ":" + String.format("%02d", min), 0, timeBaseDim.height);
            oldMin = min;

            if (AppSettings.textGlow) {
                timeBlurRadius = 20;
                blurredTimeImg = EffectAPI.blurImage(timeImg, timeBlurRadius);
            }
            imagesProcessed = true;
        }

        private void drawCenterCircle(Graphics gWindow) {
            BufferedImage ccImage = new BufferedImage(getWidth(), getHeight(), BufferedImage.TYPE_INT_ARGB);
            Graphics g = ccImage.createGraphics();
            if (!imagesProcessed) {
                reprocessUI();
            }

            Date d = Calendar.getInstance().getTime();
            int hour = d.getHours(), min = d.getMinutes();
            if (min != oldMin) {
                reprocessUI();
            }

            // Calculate how much of the battery bar should show
            int batteryFgTrim = (int) (centerCircle.height * 0.25 + centerCircle.height * 0.5 * (1d - SystemAPI.getBattery()));
            fgImg = new BufferedImage(centerCircle.width, centerCircle.height, BufferedImage.TYPE_INT_ARGB);
            Graphics2D fgG = fgImg.createGraphics();
            if (SystemAPI.isCharging()) {
                GUIAnimator fgAnimator = AnimationRegistry.getAnimator("chargingFade");
                float alpha;
                if (fgAnimator.getCurrentFrame() >= 30) {
                    alpha = (fgAnimator.getCurrentFrame() % 30) / 30f;
                } else {
                    alpha = 1f - (fgAnimator.getCurrentFrame() % 30) / 30f;
                }
                AlphaComposite ac = AlphaComposite.getInstance(AlphaComposite.SRC_OVER, alpha);
                fgG.setComposite(ac);
            }
            fgG.drawImage(scaledBatteryFg, 0, 0 - batteryFgTrim, null);
            Point batteryFgPoint = new Point(centeredPos.x, centeredPos.y + batteryFgTrim);

            // Render time in center of circle

            Point timePt = VoxMath.centerObject(timeDim, getSize());

            // Draw all of the images
            GUIAnimator centerPulse = AnimationRegistry.getAnimator("centerPulse");
            GUIAnimator centerMenu = AnimationRegistry.getAnimator("centerMenu");
            centerPulse.advance();
            centerMenu.advance();
            Point cMenuPt = VoxMath.centerObject(new Dimension((int) (centerCircle.width * (0.18 * centerMenu.getCurrentFrame())), (int) (centerCircle.height * (0.18 * centerMenu.getCurrentFrame()))),
                    new Dimension(ccImage.getWidth(), ccImage.getHeight()));
            Point selectorPt = VoxMath.centerObject(new Dimension(scaledMenuSelect.getWidth(null), scaledMenuSelect.getHeight(null)), new Dimension(getWidth(), getHeight()));
            g.drawImage(scaledCenterMenu, cMenuPt.x, cMenuPt.y, (int) (centerCircle.width * (0.18 * centerMenu.getCurrentFrame())), (int) (centerCircle.height * (0.18 * centerMenu.getCurrentFrame())), this);
            /*if (centerSelect) {

                AffineTransform rot = new AffineTransform();
                rot.rotate(selectorRotation, scaledMenuSelect.getWidth(null) / 2, scaledMenuSelect.getHeight(null) / 2);
                AffineTransformOp op = new AffineTransformOp(rot, AffineTransformOp.TYPE_BILINEAR);
                g.drawImage(op.filter(EffectAPI.toBufferedImage(scaledMenuSelect), null), selectorPt.x, selectorPt.y, null);
            }*/
            g.drawImage(scaledCenterCircle, centeredPos.x, centeredPos.y,this);
            g.drawImage(fgImg, batteryFgPoint.x, batteryFgPoint.y, this);
            Rectangle timeRect = new Rectangle(timePt.x + (int) (50 * AppSettings.screenRatio), timePt.y, timeDim.width, timeDim.height);
            if (AppSettings.textGlow) {
                g.drawImage(blurredTimeImg, timeRect.x - timeBlurRadius / 2, timeRect.y - timeBlurRadius / 2,
                        timeRect.width + timeBlurRadius, timeRect.height + timeBlurRadius, this);
            }
            g.drawImage(timeImg, timeRect.x, timeRect.y, timeRect.width, timeRect.height, this);

            // Draw root image to screen
            Point ccPt = VoxMath.centerObject(new Dimension((int) (getWidth() * (1 + centerPulse.getCurrentFrame() * 0.015)),
                    (int) (getHeight() * (1 + centerPulse.getCurrentFrame() * 0.015))), new Dimension(getWidth(), getHeight()));
            gWindow.drawImage(ccImage, ccPt.x, ccPt.y, (int) (getWidth() * (1 + centerPulse.getCurrentFrame() * 0.015)),
                    (int) (getHeight() * (1 + centerPulse.getCurrentFrame() * 0.015)), this);
        }
    }
}
