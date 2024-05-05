package t.me.youthrassvet;

import com.github.pengrad.telegrambot.TelegramBot;
import com.github.pengrad.telegrambot.model.Update;
import com.github.pengrad.telegrambot.request.SendMessage;
import com.github.pengrad.telegrambot.response.SendResponse;
import com.github.pengrad.telegrambot.response.GetUpdatesResponse;
import com.github.pengrad.telegrambot.request.GetUpdates;
import com.github.pengrad.telegrambot.UpdatesListener;

import java.util.List;

public class BirthdayBot {

    public static void main(String[] args) {
        TelegramBot bot = new TelegramBot("BOT_TOKEN");

        // Регистрируем слушатель для обновлений
        bot.setUpdatesListener(updates -> {
            for (Update update : updates) {
                long chatId = update.message().chat().id();

                SendResponse response = bot.execute(new SendMessage(chatId, "Привет от вашего бота!"));
                if (response.isOk()) {
                    System.out.println("Сообщение успешно отправлено");
                } else {
                    System.out.println("Ошибка отправки сообщения: " + response.description());
                }
            }
            return UpdatesListener.CONFIRMED_UPDATES_ALL;
        });

        try {
            Thread.sleep(10000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        bot.removeGetUpdatesListener();
    }
}
