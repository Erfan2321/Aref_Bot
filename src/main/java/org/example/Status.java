package org.example;

import java.util.List;

public enum Status {

    Main(List.of(Command.Alp, Command.ArefBranches, Command.Advisors, Command.RankReport, Command.Support)),

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
