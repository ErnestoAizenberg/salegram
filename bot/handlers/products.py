from telegram import Update
from telegram.ext import ContextTypes, CallbackQueryHandler
from asgiref.sync import sync_to_async
from ..models import Product
from ..keyboards import products_keyboard, product_detail_keyboard, main_menu_keyboard

# Асинхронные обертки для синхронных методов ORM
@sync_to_async
def get_active_products():
    return list(Product.objects.filter(is_active=True))

@sync_to_async
def get_product_by_id(product_id):
    try:
        return Product.objects.get(id=product_id, is_active=True)
    except Product.DoesNotExist:
        return None

@sync_to_async
def product_exists():
    return Product.objects.filter(is_active=True).exists()

async def show_catalog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Используем асинхронную версию
    products_exists = await product_exists()

    if not products_exists:
        await query.edit_message_text(
            "😔 В данный момент товары отсутствуют.",
            reply_markup=main_menu_keyboard()
        )
        return

    # Получаем продукты асинхронно
    products = await get_active_products()

    catalog_text = "🛍️ Каталог товаров:\n\n"
    for product in products:
        catalog_text += f"• {product.name} - {product.price} руб.\n"

    await query.edit_message_text(
        catalog_text,
        reply_markup=products_keyboard(products)
    )

async def show_product_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    product_id = int(query.data.split('_')[1])

    # Используем асинхронную версию
    product = await get_product_by_id(product_id)

    if product:
        product_text = f"""
        🛍️ {product.name}

        💰 Цена: {product.price} руб.

        📝 Описание:
        {product.description}

        После оплаты файл будет отправлен вам автоматически.
        """

        await query.edit_message_text(
            product_text,
            reply_markup=product_detail_keyboard(product.id)
        )
    else:
        await query.edit_message_text(
            "❌ Товар не найден или недоступен.",
            reply_markup=main_menu_keyboard()
        )

product_handlers = [
    CallbackQueryHandler(show_catalog, pattern='^catalog$'),
    CallbackQueryHandler(show_product_detail, pattern='^product_')
]
