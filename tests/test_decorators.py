import pytest
from decorators import log


# Тест успешного выполнения с логированием в консоль
def test_success_console(capsys, basic_function):
    basic_function(1, 2)
    captured = capsys.readouterr()
    assert captured.out.strip() == "test_func ok"


# Тест обработки ошибок с логированием в консоль
def test_error_console(capsys, basic_function):
    with pytest.raises(TypeError):
        basic_function(1, "a")
    captured = capsys.readouterr()
    assert "test_func error: TypeError" in captured.out
    assert "(1, 'a')" in captured.out


# Тест с пустыми аргументами
def test_empty_args(capsys):
    @log()
    def test_func():
        return "success"

    test_func()
    captured = capsys.readouterr()
    assert captured.out.strip() == "test_func ok"


# Тест с ключевыми аргументами
def test_kwargs_logging(capsys):
    @log()
    def test_func(x, y, z=0):
        return x + y + z

    test_func(1, 2, z=3)
    captured = capsys.readouterr()
    assert captured.out.strip() == "test_func ok"


# Тест с исключением ValueError
def test_value_error(capsys):
    @log()
    def test_func(x):
        if x < 0:
            raise ValueError("Negative value")
        return x

    with pytest.raises(ValueError):
        test_func(-1)
    captured = capsys.readouterr()
    assert "test_func error: ValueError" in captured.out
    assert "(-1,)" in captured.out


# Тест с вложенными исключениями
def test_nested_exceptions(capsys):
    @log()
    def test_func():
        try:
            raise Exception("Inner exception")
        except Exception as e:
            raise RuntimeError("Outer exception") from e

    with pytest.raises(RuntimeError):
        test_func()
    captured = capsys.readouterr()
    assert "test_func error: RuntimeError" in captured.out


# Тест с разными типами данных
def test_different_data_types(capsys):
    @log()
    def test_func(x, y, z):
        return x + y + z

    test_func(1, 2.0, "3")
    captured = capsys.readouterr()
    assert captured.out.strip() == "test_func ok"
