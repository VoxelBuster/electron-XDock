package io.github.voxelbuster.winxdock.renderer;

import java.util.HashMap;

public class AnimationRegistry {
    private static final HashMap<String, GUIAnimator> registry = new HashMap<>();

    public static void register(GUIAnimator animator, String name) {
        registry.put(name, animator);
    }

    public static GUIAnimator getAnimator(String name) {
        return registry.get(name);
    }

    public static void remove(String name) {
        registry.remove(name);
    }

    public static void advanceAll() {
        for (GUIAnimator animator : registry.values()) {
            animator.advance();
        }
    }
    public static void resetAll() {
        for (GUIAnimator animator : registry.values()) {
            animator.reset();
        }
    }

}
