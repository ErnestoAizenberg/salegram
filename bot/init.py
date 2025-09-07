import os
import django
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from django.conf import settings

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TGSaleDB.settings')
django.setup()

from .handlers.start import start, start_handlers
from .handlers.products import product_handlers
from .handlers.payments import payment_handlers

def setup_bot():
    application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()

    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))

    # Группируем обработчики callback queries
    application.add_handler(CallbackQueryHandler(start_handlers[0].callback, pattern='^(back_to_main|help)$'))
    application.add_handler(CallbackQueryHandler(product_handlers[0].callback, pattern='^catalog$'))
    application.add_handler(CallbackQueryHandler(product_handlers[1].callback, pattern='^product_'))
    application.add_handler(CallbackQueryHandler(payment_handlers[0].callback, pattern='^buy_'))
    application.add_handler(CallbackQueryHandler(payment_handlers[1].callback, pattern='^pay_(card|crypto)_'))
    application.add_handler(CallbackQueryHandler(payment_handlers[2].callback, pattern='^cancel_payment$'))

    return application

if __name__ == '__main__':
    app = setup_bot()
    print("Бот запущен...")
    app.run_polling()
