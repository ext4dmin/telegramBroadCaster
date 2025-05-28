import os
import importlib
import sqlite3
import pytest


def test_db_crud(tmp_path, monkeypatch):
    db_file = tmp_path / 'msgs.db'
    monkeypatch.setenv('DB_PATH', str(db_file))

    import db
    importlib.reload(db)

    # Изначально БД пустая
    assert db.get_unsent_messages() == []

    # Добавляем сообщение
    msg_text = 'Hello'
    msg_id = db.add_message(msg_text)
    unsent = db.get_unsent_messages()
    assert len(unsent) == 1
    assert unsent[0][0] == msg_id
    assert unsent[0][1] == msg_text
    assert unsent[0][2] is None

    # Отмечаем как отправленное
    db.mark_sent(msg_id)
    assert db.get_unsent_messages() == []