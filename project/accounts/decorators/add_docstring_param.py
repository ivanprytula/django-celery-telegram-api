# Option 1
def add_f_docstring_param(*substrings):
    def wrapper_add_docstring_param(func):
        func.__doc__ = f"""{func.__doc__}
        \r{' '.join(substrings)}"""
        return func

    return wrapper_add_docstring_param


@add_f_docstring_param('yo', 'hello', 'wazzup')
def say_hello(name):
    """Very simple example of passing variables to func's docstring."""
    print(f'Hello, my friend, {name}!')
    return 42


say_hello('Mike')
print(say_hello.__doc__)
print(say_hello, '\n')


# Option 2

def add_format_docstring_parameter(*sub):
    def dec(obj):
        obj.__doc__ = obj.__doc__.format(*sub)
        return obj

    return dec


@add_format_docstring_parameter('Ocean')
def foo():
    """My Docstring Lies Over The {0}."""
    pass


foo()
print(foo.__doc__)
