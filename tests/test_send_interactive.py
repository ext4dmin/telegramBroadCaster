import pytest
import builtins
import sys
from send import prompt_yes_no_cancel, interactive_input


def test_prompt_yes(monkeypatch):
    monkeypatch.setattr(builtins, 'input', lambda _: 'y')
    assert prompt_yes_no_cancel('Test') == 'y'


def test_prompt_no(monkeypatch):
    monkeypatch.setattr(builtins, 'input', lambda _: 'n')
    assert prompt_yes_no_cancel('Test') == 'n'


def test_prompt_cancel(monkeypatch):
    monkeypatch.setattr(builtins, 'input', lambda _: 'c')
    assert prompt_yes_no_cancel('Test') == 'c'


def test_exit_on_no(monkeypatch):
    # при первом же вводе 'n' скрипт должен завершиться
    inputs = iter(['n'])
    monkeypatch.setattr(builtins, 'input', lambda _: next(inputs))
    with pytest.raises(SystemExit) as e:
        interactive_input()
    assert e.value.code == 0