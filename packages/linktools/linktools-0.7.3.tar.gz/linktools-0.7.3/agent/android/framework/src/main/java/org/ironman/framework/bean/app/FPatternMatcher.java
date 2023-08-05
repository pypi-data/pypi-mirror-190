package org.ironman.framework.bean.app;

import android.os.PatternMatcher;

public class FPatternMatcher {

    public enum Type {
        literal,
        prefix,
        simpleGlob,
        advancedGlob;
    }

    public String path;
    public Type type;

    public FPatternMatcher(PatternMatcher patternMatcher) {
        path = patternMatcher.getPath();
        type = getType(patternMatcher.getType());
    }

    public static Type getType(int type) {
        switch (type) {
            case android.os.PatternMatcher.PATTERN_LITERAL:
                return Type.literal;
            case android.os.PatternMatcher.PATTERN_PREFIX:
                return Type.prefix;
            case android.os.PatternMatcher.PATTERN_SIMPLE_GLOB:
                return Type.simpleGlob;
            case android.os.PatternMatcher.PATTERN_ADVANCED_GLOB:
                return Type.advancedGlob;
        }
        return null;
    }
}
