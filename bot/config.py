import yaml
from pathlib import Path
from typing import Dict, Any, List
from functools import lru_cache

class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        """Загрузка конфигурации из YAML файла"""
        config_path = Path(__file__).parent / 'config.yaml'

        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                self._raw_config = yaml.safe_load(f) or {}
        except FileNotFoundError:
            raise Exception("Config file not found! Create config.yaml")
        except yaml.YAMLError as e:
            raise Exception(f"Error parsing YAML config: {e}")

    @property
    def payment(self) -> Dict[str, Any]:
        return self._raw_config.get('payment', {})

    @property
    def admin(self) -> Dict[str, Any]:
        return self._raw_config.get('admin', {})

    @property
    def bot(self) -> Dict[str, Any]:
        return self._raw_config.get('bot', {})

    @property
    def templates(self) -> Dict[str, str]:
        return self._raw_config.get('templates', {})

    # Геттеры для часто используемых значений
    @property
    def card_config(self) -> Dict[str, str]:
        return self.payment.get('card', {})

    @property
    def crypto_config(self) -> Dict[str, str]:
        return self.payment.get('crypto', {})

    @property
    def admin_contacts(self) -> Dict[str, str]:
        return self.admin.get('contacts', {})

    @property
    def working_hours(self) -> str:
        return self.admin.get('working_hours', '')

    def get_template(self, template_name: str) -> str:
        """Получить текстовый шаблон"""
        return self.templates.get(template_name, '')

    def get_bot_token(self) -> str:
        """Получить токен бота"""
        return self.bot.get('token', '')

    def get_admin_ids(self) -> List[int]:
        """Получить ID администраторов"""
        return self.bot.get('admin_ids', [])


config_path = Path(__file__).parent / 'config.yaml'
with open(config_path, 'r', encoding='utf-8') as f:
    raw_config = yaml.safe_load(f) or {}

# Глобальный экземпляр конфига
config = Config()
