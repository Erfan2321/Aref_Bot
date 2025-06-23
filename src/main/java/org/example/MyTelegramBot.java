package org.example;

import org.telegram.telegrambots.bots.TelegramLongPollingBot;
import org.telegram.telegrambots.meta.api.methods.send.SendMessage;
import org.telegram.telegrambots.meta.exceptions.TelegramApiException;

import java.util.ArrayList;


public class MyTelegramBot extends TelegramLongPollingBot {

    public void onUpdateReceived(org.telegram.telegrambots.meta.api.objects.Update update) {

        ArrayList<Integer> numbers = new ArrayList<>();

        if (update.hasMessage() && update.getMessage().hasText()) {

            String messageText = update.getMessage().getText();
            long chatId = update.getMessage().getChatId();

            SendMessage message = new SendMessage();
            message.setChatId(chatId);
            int number;

            if (messageText.trim().equalsIgnoreCase("average")) {
                message.setText("" + calculateAvg(numbers));
                numbers.clear();
            }
            else {
                try {
                    number = Integer.parseInt(messageText);
                    numbers.add(number);

                } catch (Exception e) {
                    message.setText("Wrong entry");
                }
            }

            try {
                execute(message);
            } catch (TelegramApiException e) {
                e.printStackTrace();
            }
        }
    }
    private int calculateAvg (ArrayList<Integer> numbers) {

        int sum = 0;
        for (Integer integer : numbers)
            sum += integer;

        return sum/numbers.size();
    }
    public String getBotUsername() {
        return "MyTestJavaBot123_bot";
    }
    public String getBotToken() {
        return "7661881146:AAEujXxenoQI7msIWRp4a93bV3h_4Soh0po";
    }
}