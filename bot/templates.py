from typing import Dict, Any
import yaml

class Templates:
    """Класс для работы с текстовыми шаблонами бота"""

    def __init__(self, config: Dict[str, Any]):
        """
        Инициализация класса шаблонов

        Args:
            config: Конфигурация из YAML файла
        """
        self.config = config
        self.templates = config.get('templates', {})
        self.payment_config = config.get('payment', {})
        self.admin_config = config.get('admin', {})

    def welcome(self) -> str:
        """Шаблон приветственного сообщения"""
        return self.templates.get('welcome', '')

    def help(self) -> str:
        """Шаблон сообщения помощи"""
        template = self.templates.get('help', '')
        return template.format(
            payment_admin=self.admin_config.get('contacts', {}).get('payment', ''),
            support_admin=self.admin_config.get('contacts', {}).get('support', ''),
            partnership_admin=self.admin_config.get('contacts', {}).get('partnership', ''),
            working_hours=self.admin_config.get('working_hours', '')
        )

    def payment_card(self, amount: float) -> str:
        """Шаблон оплаты картой"""
        template = self.templates.get('payment_card', '')
        card_config = self.payment_config.get('card', {})
        return template.format(
            card_number=card_config.get('number', ''),
            recipient=card_config.get('recipient', ''),
            amount=amount,
            instructions=card_config.get('instructions', ''),
            admin_contact=self.admin_config.get('contacts', {}).get('payment', '')
        )

    def payment_crypto(self, amount: float) -> str:
        """Шаблон оплаты криптовалютой"""
        template = self.templates.get('payment_crypto', '')
        crypto_config = self.payment_config.get('crypto', {})
        return template.format(
            btc_address=crypto_config.get('btc', ''),
            eth_address=crypto_config.get('eth', ''),
            usdt_address=crypto_config.get('usdt', ''),
            amount=amount,
            instructions=crypto_config.get('instructions', ''),
            admin_contact=self.admin_config.get('contacts', {}).get('payment', '')
        )

    def order_created(self, product_name: str, product_price: float) -> str:
        """Шаблон создания заказа"""
        template = self.templates.get('order_created', '')
        return template.format(
            product_name=product_name,
            product_price=product_price
        )

    def get_raw_template(self, template_name: str) -> str:
        """Получить сырой шаблон без форматирования"""
        return self.templates.get(template_name, '')
