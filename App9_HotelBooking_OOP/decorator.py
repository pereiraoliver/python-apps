"""Notes and examples for Python decorators."""


# Case 1: A decorator for a function without arguments
def add_greeting_messages(function):
    def decorated_function():
        print("Decorator start")
        function()
        print("Decorator finish")

    return decorated_function


@add_greeting_messages
def greet_without_arguments():
    print("I'm greet function!")


greet_without_arguments()


# Case 2: A decorator that forwards positional and keyword arguments
def log_function_call(function):
    def decorated_function(*args, **kwargs):
        print("Calling function...")
        result = function(*args, **kwargs)
        print("Function finished")
        return result

    return decorated_function


@log_function_call
def greet_with_arguments(name, age):
    print(f"Hi {name}, you are {age}")


greet_with_arguments("Oliver", 30)


# Case 3: Stacking multiple decorators
def first_decorator(function):
    def decorated_function():
        print("Decorator 1 start")
        function()
        print("Decorator 1 finish")

    return decorated_function


def second_decorator(function):
    def decorated_function():
        print("Decorator 2 start")
        function()
        print("Decorator 2 finish")

    return decorated_function


@first_decorator
@second_decorator
def greet_with_stacked_decorators():
    print("I'm greet function!")


greet_with_stacked_decorators()
