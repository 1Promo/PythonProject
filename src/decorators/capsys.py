@pytest.fixture
def example_function():
    @log()
    def func(x, y):
        return x + y

    return func


@pytest.fixture
def example_function_with_file():
    @log(filename="test.log")
    def func(x, y):
        return x + y

    return func
