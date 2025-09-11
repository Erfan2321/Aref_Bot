package org.example;

import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;

public enum Status {

    Main(List.of(Command.Alp, Command.ArefBranches, Command.Advisors, Command.RankReport)),

    Alp (List.of()),
    ArefBranches(List.of()),
    Advisors(List.of()),
    RankReport(List.of()),

    ;

    public final List<Command> commands;

    Status(List<Command> commands) {
        this.commands = commands;
    }

}
