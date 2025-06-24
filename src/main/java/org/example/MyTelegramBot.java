package org.example;

import org.telegram.telegrambots.bots.DefaultBotOptions;
import org.telegram.telegrambots.bots.TelegramLongPollingBot;
import org.telegram.telegrambots.meta.api.methods.send.SendMessage;
import org.telegram.telegrambots.meta.api.objects.Update;
import org.telegram.telegrambots.meta.api.objects.replykeyboard.ReplyKeyboardMarkup;
import org.telegram.telegrambots.meta.api.objects.replykeyboard.buttons.KeyboardRow;
import org.telegram.telegrambots.meta.exceptions.TelegramApiException;

import java.util.ArrayList;
import java.util.List;

public class MyTelegramBot extends TelegramLongPollingBot {

    public MyTelegramBot() {
        super(new DefaultBotOptions());
    }

    @Override
    public void onUpdateReceived(Update update) {
        if (update.hasMessage() && update.getMessage().hasText()) {
            String messageText = update.getMessage().getText();
            long chatId = update.getMessage().getChatId();

            SendMessage message = new SendMessage();
            message.setChatId(chatId);

            switch (messageText) {
                case "/start":
                    message.setText("یکی از گزینه‌های زیر رو انتخاب کن:");
                    message.setReplyMarkup(getMainKeyboard());
                    break;

                case "🔢 عدد":
                    message.setText("لطفاً یک عدد وارد کن:");
                    break;

                case "🔤 کلمه":
                    message.setText("لطفاً یک کلمه وارد کن:");
                    break;

                default:
                    message.setText("دریافت شد: " + messageText);
                    break;
            }

            try {
                execute(message);
            } catch (TelegramApiException e) {
                e.printStackTrace();
            }
        }
    }

    private ReplyKeyboardMarkup getMainKeyboard() {
        ReplyKeyboardMarkup keyboardMarkup = new ReplyKeyboardMarkup();
        keyboardMarkup.setResizeKeyboard(true); // بهتره برای موبایل

        KeyboardRow row = new KeyboardRow();
        row.add("🔢 عدد");
        row.add("🔤 کلمه");

        List<KeyboardRow> keyboard = new ArrayList<>();
        keyboard.add(row);

        keyboardMarkup.setKeyboard(keyboard);
        return keyboardMarkup;
    }

    @Override
    public String getBotUsername() {
        return "MyTestJavaBot222_bot";
    }
    @Override
    public String getBotToken() {
        return "7999300553:AAG_8GqNWONP1W8Y_OP6XG4cLBUqglN89CI";
    }


}
