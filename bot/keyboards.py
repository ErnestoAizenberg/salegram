from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("🛍️ Каталог товаров", callback_data='catalog')],
        # [InlineKeyboardButton("💰 Мой баланс", callback_data='balance'),
        # InlineKeyboardButton("📦 Мои заказы", callback_data='orders')],
        [InlineKeyboardButton("ℹ️ Помощь", callback_data='help')]
    ]
    return InlineKeyboardMarkup(keyboard)

def products_keyboard(products):
    keyboard = []
    for product in products:
        keyboard.append([InlineKeyboardButton(
            f"{product.name} - {product.price} руб.",
            callback_data=f'product_{product.id}'
        )])
    keyboard.append([InlineKeyboardButton("⬅️ Назад", callback_data='back_to_main')])
    return InlineKeyboardMarkup(keyboard)

def product_detail_keyboard(product_id):
    keyboard = [
        [InlineKeyboardButton("🛒 Купить", callback_data=f'buy_{product_id}')],
        [InlineKeyboardButton("⬅️ Назад к каталогу", callback_data='catalog')]
    ]
    return InlineKeyboardMarkup(keyboard)

def payment_methods_keyboard(order_id):
    keyboard = [
        [InlineKeyboardButton("💳 Банковская карта", callback_data=f'pay_card_{order_id}')],
        [InlineKeyboardButton("📱 Криптовалюта", callback_data=f'pay_crypto_{order_id}')],
        [InlineKeyboardButton("❌ Отмена", callback_data='cancel_payment')]
    ]
    return InlineKeyboardMarkup(keyboard)

def admin_keyboard():
    keyboard = [
        [InlineKeyboardButton("📊 Статистика", callback_data='admin_stats')],
        [InlineKeyboardButton("📦 Управление заказами", callback_data='admin_orders')],
        [InlineKeyboardButton("🛍️ Управление товарами", callback_data='admin_products')]
    ]
    return InlineKeyboardMarkup(keyboard)
