package org.example;

public enum Sheet {

    Advisors("1XxDYTjzktnWbEpkxpq_DoQ29cPAbf8XOirtM6qtTx3M"),

    ;

    String spreadsheetId;

    Sheet(String spreadsheetId) {
        this.spreadsheetId = spreadsheetId;
    }
}
