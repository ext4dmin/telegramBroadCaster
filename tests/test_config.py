import os
import importlib
import pytest


def test_config_env(monkeypatch):
    # Устанавливаем тестовые переменные окружения
    env = {
        'API_ID': '101',
        'API_HASH': 'abc123',
        'SESSION_NAME': 'sess_test',
        'CHATS_CSV': 'test_chats.csv',
        'DB_PATH': 'test_db.sqlite',
        'LOG_PATH': 'test.log'
    }
    for k, v in env.items():
        monkeypatch.setenv(k, v)

    # Перезагружаем модуль config
    import config
    importlib.reload(config)

    assert config.API_ID == 101
    assert config.API_HASH == 'abc123'
    assert config.SESSION_NAME == 'sess_test'
    assert config.CHATS_CSV == 'test_chats.csv'
    assert config.DB_PATH == 'test_db.sqlite'
    assert config.LOG_PATH == 'test.log'