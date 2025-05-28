import os
import importlib

import pytest


def test_db_crud_operations(tmp_path, monkeypatch):
    # Настраиваем файл БД в папке tmp_path
    db_file = tmp_path / 'test_messages.db'
    monkeypatch.setenv('DB_PATH', str(db_file))

    # Импортируем и перезагружаем модуль db
    import db
    importlib.reload(db)

    # В начале - нет непросланных сообщений
    unsent = db.get_unsent_messages()
    assert isinstance(unsent, list)
    assert unsent == []

    # Добавляем сообщение без изображения
    msg_id = db.add_message('Test message', None)
    unsent = db.get_unsent_messages()
    assert len(unsent) == 1
    assert unsent[0][0] == msg_id
    assert unsent[0][1] == 'Test message'
    assert unsent[0][2] is None

    # Помечаем сообщение как отправленное
    db.mark_sent(msg_id)
    unsent_after = db.get_unsent_messages()
    assert unsent_after == []