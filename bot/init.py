import os
import django
import logging
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from telegram.error import TelegramError, TimedOut, NetworkError
from django.conf import settings

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TGSaleDB.settings')
django.setup()

from .handlers.start import start, start_handlers
from .handlers.products import product_handlers
from .handlers.payments import payment_handlers

print(settings.TELEGRAM_BOT_TOKEN)
def setup_bot():
    try:
        # Создаем application с увеличенными таймаутами
        application = Application.builder() \
            .token(settings.TELEGRAM_BOT_TOKEN) \
            .read_timeout(30) \
            .write_timeout(30) \
            .connect_timeout(30) \
            .pool_timeout(30) \
            .build()

        logger.info("Application создан успешно")

        # Добавляем обработчики
        application.add_handler(CommandHandler("start", start))
        logger.info("Обработчик команды start добавлен")

        # Группируем обработчики callback queries
        callback_patterns = [
            ('back_to_main|help', start_handlers[0].callback, 'start_handler'),
            ('catalog', product_handlers[0].callback, 'catalog_handler'),
            ('product_', product_handlers[1].callback, 'product_handler'),
            ('buy_', payment_handlers[0].callback, 'buy_handler'),
            ('pay_(card|crypto)_', payment_handlers[1].callback, 'payment_method_handler'),
            ('cancel_payment', payment_handlers[2].callback, 'cancel_payment_handler')
        ]

        for pattern, callback, handler_name in callback_patterns:
            application.add_handler(CallbackQueryHandler(callback, pattern=pattern))
            logger.info(f"Обработчик {handler_name} добавлен (pattern: {pattern})")

        logger.info("Все обработчики успешно добавлены")
        return application

    except Exception as e:
        logger.error(f"Ошибка при настройке бота: {e}", exc_info=True)
        raise

async def error_handler(update, context):
    """Глобальный обработчик ошибок"""
    try:
        logger.error(f"Ошибка в обработчике: {context.error}", exc_info=True)

        # Отправляем сообщение об ошибке пользователю
        if update and update.effective_chat:
            try:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="⚠️ Произошла ошибка. Пожалуйста, попробуйте позже."
                )
            except Exception as send_error:
                logger.error(f"Не удалось отправить сообщение об ошибке: {send_error}")
    except Exception as handler_error:
        logger.error(f"Ошибка в error_handler: {handler_error}")

def main():
    try:
        logger.info("Запуск бота...")
        app = setup_bot()

        # Добавляем глобальный обработчик ошибок
        app.add_error_handler(error_handler)
        logger.info("Глобальный обработчик ошибок добавлен")

        print("Бот запущен...")
        logger.info("Бот начал polling")

        # Запускаем с обработкой ошибок
        app.run_polling(
            poll_interval=1.0,
            timeout=30,
            drop_pending_updates=True,
            allowed_updates=['message', 'callback_query']
        )

    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
    except TelegramError as e:
        logger.error(f"Ошибка Telegram API: {e}", exc_info=True)
    except NetworkError as e:
        logger.error(f"Сетевая ошибка: {e}", exc_info=True)
    except TimedOut as e:
        logger.error(f"Таймаут: {e}", exc_info=True)
    except Exception as e:
        logger.critical(f"Критическая ошибка при запуске бота: {e}", exc_info=True)
    finally:
        logger.info("Бот завершил работу")

if __name__ == '__main__':
    main()
