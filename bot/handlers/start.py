from telegram import Update
from telegram.ext import ContextTypes, CallbackQueryHandler
from asgiref.sync import sync_to_async
from ..models import UserProfile
from ..keyboards import main_menu_keyboard

# Асинхронные обертки для ORM-методов
@sync_to_async
def get_or_create_user_profile(user_id, username, first_name, last_name, language_code):
    profile, created = UserProfile.objects.get_or_create(
        user_id=user_id,
        defaults={
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'language_code': language_code
        }
    )

    if not created:
        profile.username = username
        profile.first_name = first_name
        profile.last_name = last_name
        profile.save()

    return profile

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id

    # Создаем или обновляем профиль пользователя асинхронно
    await get_or_create_user_profile(
        user_id=user_id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        language_code=user.language_code
    )

    welcome_text = """
    👋 Добро пожаловать в магазин баз данных!

    Здесь вы можете приобрести качественные базы данных для вашего бизнеса.

    🛍️ Каталог товаров - просмотр доступных баз данных
    💰 Мой баланс - информация о вашем балансе
    📦 Мои заказы - история ваших покупок
    ℹ️ Помощь - поддержка и ответы на вопросы

    Выберите действие:
    """

    await update.message.reply_text(welcome_text, reply_markup=main_menu_keyboard())

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == 'back_to_main':
        await query.edit_message_text(
            "Главное меню:",
            reply_markup=main_menu_keyboard()
        )

    elif data == 'help':
        help_text = """
        ℹ️ Помощь

        Если у вас возникли вопросы или проблемы:

        • По вопросам оплаты: @admin_username
        • Техническая поддержка: @support_username
        • По сотрудничеству: @partner_username

        Рабочее время: 10:00-22:00 (МСК)
        """
        await query.edit_message_text(help_text, reply_markup=main_menu_keyboard())

start_handlers = [
    CallbackQueryHandler(handle_callback, pattern='^(back_to_main|help)$')
]
