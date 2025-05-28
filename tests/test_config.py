import os
import importlib
import pytest


def test_config_env(monkeypatch):
    # Задаём тестовые значения переменных окружения
    test_env = {
        'API_ID': '111',
        'API_HASH': 'hash_value',
        'SESSION_NAME': 'test_session',
        'CHATS_CSV': 'chats_test.csv',
        'DB_PATH': 'db_test.sqlite',
        'LOG_PATH': 'log_test.log'
    }
    for key, val in test_env.items():
        monkeypatch.setenv(key, val)

    # Импортируем и перезагружаем модуль config
    import config
    importlib.reload(config)

    assert config.API_ID == 111
    assert config.API_HASH == 'hash_value'
    assert config.SESSION_NAME == 'test_session'
    assert config.CHATS_CSV == 'chats_test.csv'
    assert config.DB_PATH == 'db_test.sqlite'
    assert config.LOG_PATH == 'log_test.log'