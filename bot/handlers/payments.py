from decimal import Decimal
from telegram import Update
from telegram.ext import ContextTypes, CallbackQueryHandler
from asgiref.sync import sync_to_async
from ..models import Product, Order, UserProfile
from ..keyboards import payment_methods_keyboard, main_menu_keyboard

# Асинхронные обертки для ORM-методов
@sync_to_async
def get_product_with_price(product_id):
    try:
        return Product.objects.select_related().get(id=product_id, is_active=True)
    except Product.DoesNotExist:
        return None

@sync_to_async
def create_order_with_product(user_id, product):
    order = Order.objects.create(
        user_id=user_id,
        product=product,
        status='pending'
    )
    return Order.objects.select_related('product').get(id=order.id)

@sync_to_async
def get_order_with_product(order_id, user_id):
    try:
        return Order.objects.select_related('product').get(id=order_id, user_id=user_id)
    except Order.DoesNotExist:
        return None

@sync_to_async
def save_order_payment_data(order_id, payment_method):
    order = Order.objects.get(id=order_id)
    order.payment_data = {
        'method': payment_method,
        'status': 'waiting_confirmation'
    }
    order.save()
    return order

@sync_to_async
def cancel_order(order_id, user_id):
    try:
        order = Order.objects.get(id=order_id, user_id=user_id)
        order.status = 'cancelled'
        order.save()
        return True
    except Order.DoesNotExist:
        return False

async def initiate_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    product_id = int(query.data.split('_')[1])
    product = await get_product_with_price(product_id)

    if product:
        user_id = query.from_user.id
        order = await create_order_with_product(user_id, product)

        payment_text = f"""
        🛒 Оформление заказа

        Товар: {product.name}
        Цена: {product.price} руб.

        Выберите способ оплаты:
        """

        await query.edit_message_text(
            payment_text,
            reply_markup=payment_methods_keyboard(order.id)
        )
    else:
        await query.edit_message_text(
            "❌ Товар не найден.",
            reply_markup=main_menu_keyboard()
        )

async def process_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data.split('_')
    payment_method = data[1]
    order_id = int(data[2])

    order = await get_order_with_product(order_id, query.from_user.id)

    if order:
        product_price = order.product.price

        if payment_method == 'card':
            payment_info = f"""
            💳 Оплата банковской картой:

            Номер карты: 1234 5678 9012 3456
            Получатель: Иван Иванов
            Сумма: {product_price} руб.

            После оплаты отправьте скриншот чека @admin_username
            """

        elif payment_method == 'crypto':
            payment_info = f"""
            📱 Оплата криптовалютой:

            BTC адрес: bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh
            ETH адрес: 0x742d35Cc6634C0532925a3b844Bc454e4438f44e
            USDT (TRC20): TAbnT7PkYjLPz6bLpWnq6mLmXyX2n2n2n2

            Сумма: {product_price} руб. (конвертируйте по курсу на момент оплаты)

            После оплаты отправьте хэш транзакции @admin_username
            """

        await save_order_payment_data(order.id, payment_method)

        await query.edit_message_text(
            payment_info,
            reply_markup=main_menu_keyboard()
        )
    else:
        await query.edit_message_text(
            "❌ Заказ не найден.",
            reply_markup=main_menu_keyboard()
        )

async def cancel_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Если есть order_id в контексте (можно расширить при необходимости)
    order_id = context.user_data.get('current_order_id')

    if order_id:
        # Помечаем заказ как отмененный
        success = await cancel_order(order_id, query.from_user.id)
        if success:
            message = "❌ Оплата отменена. Заказ удален."
        else:
            message = "⚠️ Не удалось найти заказ для отмены."
    else:
        message = "❌ Оплата отменена."

    await query.edit_message_text(
        message,
        reply_markup=main_menu_keyboard()
    )

payment_handlers = [
    CallbackQueryHandler(initiate_payment, pattern='^buy_'),
    CallbackQueryHandler(process_payment, pattern='^pay_(card|crypto)_'),
    CallbackQueryHandler(cancel_payment, pattern='^cancel_payment$')
]
