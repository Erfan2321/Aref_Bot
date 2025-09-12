package org.example;

import com.google.api.client.json.JsonFactory;
import com.google.api.client.json.jackson2.JacksonFactory;
import org.telegram.telegrambots.bots.DefaultBotOptions;
import org.telegram.telegrambots.bots.TelegramLongPollingBot;
import org.telegram.telegrambots.meta.api.methods.send.SendMessage;
import org.telegram.telegrambots.meta.api.objects.Update;
import org.telegram.telegrambots.meta.api.objects.replykeyboard.ReplyKeyboardMarkup;
import org.telegram.telegrambots.meta.api.objects.replykeyboard.buttons.KeyboardRow;
import org.telegram.telegrambots.meta.exceptions.TelegramApiException;
import com.google.api.services.sheets.v4.Sheets;
import com.google.api.services.sheets.v4.SheetsScopes;
import com.google.api.services.sheets.v4.model.ValueRange;
import com.google.api.client.googleapis.javanet.GoogleNetHttpTransport;
import com.google.api.client.googleapis.auth.oauth2.GoogleCredential;


import java.util.*;
import java.io.FileInputStream;
import java.io.IOException;
import java.security.GeneralSecurityException;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

public class MyTelegramBot extends TelegramLongPollingBot{

    private static final String APPLICATION_NAME = "My Java App";
    private static final JsonFactory JSON_FACTORY = JacksonFactory.getDefaultInstance();

    private Sheets service;

    private final Map<String, Advisor> advisors = new HashMap<>();

    public Status currentStatus = Status.Main;


    public MyTelegramBot() throws GeneralSecurityException, IOException {
        super(new DefaultBotOptions());
        APIConnection();

        ScheduledExecutorService scheduler = Executors.newSingleThreadScheduledExecutor();
        scheduler.scheduleAtFixedRate(() -> {
            try {
                loadConsultantsFromSheet();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }, 0, 1, TimeUnit.DAYS);
    }

    @Override
    public void onUpdateReceived(Update update) {
        if (update.hasMessage() && update.getMessage().hasText()) {
            String messageText = update.getMessage().getText();
            long chatId = update.getMessage().getChatId();

            SendMessage message = new SendMessage();
            message.setChatId(chatId);

            if (messageText != null) {
                if (messageText.equals(Command.Start.name)) {
                    message.setText("یکی از گزینه‌های زیر رو انتخاب کن:");
                    message.setReplyMarkup(getMainKeyboard(Status.Main));
                    currentStatus = Status.Main;
                } else {
                    if (currentStatus == Status.Main) {

//                        if (messageText.equals(Status.Alp.name)) {
//                            currentStatus = Status.Alp;
//                            message.setText("اینجا آزمون‌های آلپ رو نشون می‌دیم...");
//                        } else if (messageText.equals(Status.ArefBranches.name)) {
//                            currentStatus = Status.ArefBranches;
//                            message.setText("اینجا لیست شعب عارف میاد...");
//                        } else if (messageText.equals(Status.RankReport.name)) {
//                            currentStatus = Status.RankReport;
//                            message.setText("اینجا کارنامه کنکور رتبه‌ها میاد...");
//                        } else if (messageText.equals(Status.Advisors.name)) {
//                            currentStatus = Status.Advisors;
//                            message.setText("یکی از مشاوران رو انتخاب کن:");
//                            message.setReplyMarkup(getConsultantsKeyboard());
//                        } else if (messageText.equals("پشتیبانی")) {
//                            message.setText("@arefeducation");
//                        }
                    }
                    else if (currentStatus == Status.Advisors) {
                        Advisor advisor = advisors.get(messageText);
                        if (advisor != null) {
                            String response = "نام : " + advisor.getName() + "\n"
                                    + "وضعیت : " + advisor.getStatus() + "\n"
                                    + "روزهای کاری : " + advisor.getWorkDays() + "\n"
                                    + "ساعات حضور : " + advisor.getWorkHours();
                            message.setText(response);
                        } else {
                            message.setText("مشاور مورد نظر پیدا نشد!");
                        }
                    }
                }
            }

            try {
                execute(message);
            } catch (TelegramApiException e) {
                e.printStackTrace();
            }
        }
    }

    private void changeStatus(Status status) {
        // TODO
    }
    private ReplyKeyboardMarkup getMainKeyboard(Status status) {

        ReplyKeyboardMarkup keyboardMarkup = new ReplyKeyboardMarkup();
        keyboardMarkup.setResizeKeyboard(true);

        List<KeyboardRow> rows = new ArrayList<>();
        KeyboardRow row = new KeyboardRow();

        for (var command : status.commands) {
            row.add(command.name);

            if (row.size() == 2) {
                rows.add(row);
                row = new KeyboardRow();
            }
        }

        if (!row.isEmpty())
            rows.add(row);

        keyboardMarkup.setKeyboard(rows);
        return keyboardMarkup;
    }


    private void loadConsultantsFromSheet() throws IOException {

        String spreadsheetId = Sheet.Advisors.spreadsheetId;
        String range = "Sheet1!A2:D";

        ValueRange response = service.spreadsheets().values()
                .get(spreadsheetId, range)
                .execute();

        List<List<Object>> values = response.getValues();
        advisors.clear();
        if (values == null || values.isEmpty()) return;

        for (List<Object> row : values) {
            if (row.size() < 4) continue;
            String name = row.get(0).toString().trim();
            String status = row.get(1).toString().trim();
            String workDays = row.get(2).toString().replace(",", " ").trim();
            String workHours = row.get(3).toString().trim();

            advisors.put(name, new Advisor(name, status, workDays, workHours));
        }
    }
    private void APIConnection() throws IOException, GeneralSecurityException {

        String credentialsFilePath = "phonic-botany-471215-u2-97e72590c944.json";
        GoogleCredential credential = GoogleCredential.fromStream(new FileInputStream(credentialsFilePath))
                .createScoped(Collections.singleton(SheetsScopes.SPREADSHEETS_READONLY));

        service = new Sheets.Builder(
                GoogleNetHttpTransport.newTrustedTransport(),
                JSON_FACTORY,
                credential
        ).setApplicationName(APPLICATION_NAME).build();
    }


    public String getBotUsername() {return TelegramData.BOT_NAME;}
    public String getBotToken() {return TelegramData.BOT_TOKEN;}
}
