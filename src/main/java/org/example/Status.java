package org.example;

import java.util.regex.Matcher;

public enum Status {

    Main("/start"),
    Alp ("آزمون های آلپ"),
    ArefBranches("شعب عارف"),
    Advisors("مشاوران مجموعه"),
    RankReport("کارنامه کنکور رتبه ها"),

    ;

    public final String name;

    Status(String name) {
        this.name = name;
    }

    public Matcher match(String input) { // TODO
        return null;
    }
}
