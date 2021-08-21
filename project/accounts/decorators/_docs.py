"""
Decorators wrap a function/class, modifying its behavior.

This formula is a good boilerplate template for building more complex decorators.

******
import functools

def decorator(func):
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        # Do something before
        value = func(*args, **kwargs)
        # Do something after
        return value
    return wrapper_decorator
******
"""
import functools
import math
import random
import time
from dataclasses import dataclass
from datetime import datetime


# 1 case: Decorating Functions Without Arguments
def my_decorator(func):
    def wrapper():
        print("Something is happening before the function is called.")
        func()
        print("Something is happening after the function is called.")

    return wrapper


# 1 case: Easy, ver.2
def not_during_the_night(func):
    def wrapper():
        if 7 <= datetime.now().hour < 22:
            func()
            # We can call wrapped func any reasonable number of times
            # func()
            # func()
        else:
            pass  # Hush, the neighbors are asleep

    return wrapper


# @my_decorator
def say_whee():
    print("Whee!")


say_whee_simple = my_decorator(say_whee)
say_whee_dynamic = not_during_the_night(say_whee)

"""
>>> say_whee_simple | say_whee_dynamic
<function my_decorator.<locals>.wrapper at 0x7f3c5dfd42f0>
<function not_during_the_night.<locals>.wrapper at 0x7fd62949f790>
"""


# 2 case: Decorating Functions With Arguments
def do_once(func):
    @functools.wraps(func)
    def wrapper_do_twice(*args, **kwargs):
        func(*args, **kwargs)
        return func(*args, **kwargs)

    return wrapper_do_twice


@do_once
def greet(name):
    print(f"Hello {name}")


# gree t('World!')
# greet = do_once(greet)


# print(greet)


# <function greet at 0x7f39d8a6e0d0>

@do_once
def return_greeting(name):
    print("Creating greeting")
    return f"Hi {name}"


# print(return_greeting("Adam"))

################################################################################
### Timing Functions # noqa
################################################################################
def timer(func):
    """Print the runtime of the decorated function"""

    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()  # 1
        func(*args, **kwargs)
        end_time = time.perf_counter()  # 2
        run_time = end_time - start_time  # 3
        print(f"Finished {func.__name__!r} in {run_time:.4f} secs")

    return wrapper_timer


@timer
def waste_some_time(num_times):
    for _ in range(num_times):
        return sum([i ** 2 for i in range(10000)])


# w aste_some_time(1)
# w aste_some_time(999)

################################################################################
### Debugging Code # noqa
################################################################################
def debug(func):
    """Print the function signature and return value"""

    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        args_repr = [repr(a) for a in args]  # 1
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]  # 2
        signature = ", ".join(args_repr + kwargs_repr)  # 3
        print(f"Calling {func.__name__}({signature})")
        value = func(*args, **kwargs)
        print(f"{func.__name__!r} returned {value!r}")  # 4
        return value

    return wrapper_debug


@debug
def make_greeting(name, age=None):
    if age is None:
        return f"Howdy {name}!"
    else:
        return f"Whoa {name}! {age} already, you are growing up!"


# m ake_greeting("Benjamin")
# make_greeting("Richard", age=112)
# make_greeting(name="Dorrisile", age=116)
"""
This example might not seem immediately useful since the @debug decorator just repeats what you just wrote. It’s
more powerful when applied to small convenience functions that you don’t call directly yourself.
"""


################################################################################
### Slowing Down Code # noqa
################################################################################
def slow_down(func):
    """Sleep 1 second before calling the function"""

    @functools.wraps(func)
    def wrapper_slow_down(*args, **kwargs):
        time.sleep(1)
        return func(*args, **kwargs)

    return wrapper_slow_down


@slow_down
def countdown(from_number):
    if from_number < 1:
        print("Liftoff!")
    else:
        print(from_number)
        countdown(from_number - 1)


# countdown(3)

################################################################################
### Registering Plugins # noqa
################################################################################
PLUGINS = dict()


# We do not have to write an inner function or use @functools.wraps in this example
# because we are returning the original function unmodified.
def register(func):
    """Register a function as a plug-in"""
    PLUGINS[func.__name__] = func
    return func


@register
def say_hello(name):
    return f"Hello {name}"


@register
def be_awesome(name):
    return f"Yo {name}, together we are the awesomest!"


def randomly_greet(name):
    # [
    #     ('say_hello', <function say_hello at 0x7f551a416430>),
    #     ('be_awesome', <function be_awesome at 0x7f551a4164c0>)
    # ]
    greeter, greeter_func = random.choice(list(PLUGINS.items()))
    print(f"Using {greeter!r}")
    return greeter_func(name)


# prin t('other:', randomly_greet('John'))
# print('PLUGINS:', PLUGINS)
# print('globals():', globals())


################################################################################
### Fancy Decorators # noqa
################################################################################
###     ↪ Decorating Classes # noqa
class TimeWaster:
    @debug
    def __init__(self, max_num):
        self.max_num = max_num

    @timer
    def waste_time(self, num_times):
        for _ in range(num_times):
            return sum([i ** 2 for i in range(self.max_num)])


# t w = TimeWaster(1000)
# tw.waste_time(999)
@dataclass
class PlayingCard:
    rank: str
    suit: str


# P layingCard = dataclass(PlayingCard)


###     ↪ Nesting Decorators # noqa
@debug
@do_once
def greet2(name):
    print(f"Hello {name}")


###     ↪ Decorators With Arguments # noqa
"""def_ repeat(num_times):
    def decorator_repeat(func):
        ...  # Create and return a wrapper function
    return decorator_repeat
"""


def repeat(num_times):
    def decorator_repeat(func):
        @functools.wraps(func)
        def wrapper_repeat(*args, **kwargs):
            for _ in range(num_times):
                value = func(*args, **kwargs)
            return value  # noqa

        return wrapper_repeat

    return decorator_repeat


@repeat(num_times=4)
def greet_again(name):
    print(f"Hello {name}")


greet_again('Bob')


### Both Please, But Never Mind the Bread # noqa
# PEP-3102
# 'single star' syntax for indicating the end of positional parameters ==
# which means that all following parameters are keyword-only.
def repeat_full_example(_func=None, *, num_times=2):
    def decorator_repeat(func):
        @functools.wraps(func)
        def wrapper_repeat(*args, **kwargs):
            for _ in range(num_times):
                value = func(*args, **kwargs)
            return value  # noqa

        return wrapper_repeat

    if _func is None:
        return decorator_repeat
    else:
        return decorator_repeat(_func)


@repeat
def say_whee2():
    print("Whee 2!")


@repeat(num_times=3)
def greet3(name):
    print(f"Hello {name}")


### Stateful Decorators # noqa
def count_calls(func):
    @functools.wraps(func)
    def wrapper_count_calls(*args, **kwargs):
        wrapper_count_calls.num_calls += 1
        print(f"Call {wrapper_count_calls.num_calls} of {func.__name__!r}")
        return func(*args, **kwargs)

    wrapper_count_calls.num_calls = 0
    return wrapper_count_calls


@count_calls
def say_whee3():
    print("Whee 3!")


# say_whee3()  # noqa

### Classes as Decorators # noqa
class CountCalls:
    def __init__(self, func):
        # instead of @functools.wraps
        functools.update_wrapper(self, func)
        self.func = func
        self.num_calls = 0

    def __call__(self, *args, **kwargs):
        self.num_calls += 1
        print(f"Call {self.num_calls} of {self.func.__name__!r}")
        return self.func(*args, **kwargs)


@CountCalls
def say_whee_class_decorator():
    print('Whee! with class decorator!')


say_whee_class_decorator()


################################################################################
### More Real World Examples # noqa
###############################################################################
### Slowing Down Code, Revisited # noqa
def slow_down_with_param(_func=None, *, rate=1):
    """Sleep given amount of seconds before calling the function"""

    def decorator_slow_down_with_param(func):
        @functools.wraps(func)
        def wrapper_slow_down_with_param(*args, **kwargs):
            time.sleep(rate)
            return func(*args, **kwargs)

        return wrapper_slow_down_with_param

    if _func is None:
        return decorator_slow_down_with_param
    else:
        return decorator_slow_down_with_param(_func)


### Creating Singletons # noqa
def singleton(cls):
    """Make a class a Singleton class (only one instance)"""

    @functools.wraps(cls)
    def wrapper_singleton(*args, **kwargs):
        if not wrapper_singleton.instance:
            wrapper_singleton.instance = cls(*args, **kwargs)
        return wrapper_singleton.instance

    wrapper_singleton.instance = None
    return wrapper_singleton


@singleton
class TheOne:
    pass


first_one = TheOne()
another_one = TheOne()

print(id(first_one))
print(id(another_one))
print(first_one is another_one)  # True


### Caching Return Values # noqa
@count_calls
def fibonacci(num):
    if num < 2:
        return num
    return fibonacci(num - 1) + fibonacci(num - 2)


# print(fibonacci(20))


# simple custom cache decorator
def cache(func):
    """Keep a cache of previous function calls"""

    @functools.wraps(func)
    def wrapper_cache(*args, **kwargs):
        cache_key = args + tuple(kwargs.items())
        if cache_key not in wrapper_cache.cache:
            wrapper_cache.cache[cache_key] = func(*args, **kwargs)
        return wrapper_cache.cache[cache_key]

    wrapper_cache.cache = dict()

    return wrapper_cache


@cache
@count_calls
def fibonacci2(num):
    if num < 2:
        return num
    return fibonacci2(num - 1) + fibonacci2(num - 2)


# In the STL, a Least Recently Used (LRU) cache is available as @functools.lru_cache
@functools.lru_cache(maxsize=4)
def fibonacci_improved(num):
    print(f"Calculating fibonacci_improved({num})")
    if num < 2:
        return num
    return fibonacci_improved(num - 1) + fibonacci_improved(num - 2)


# print(fibonacci_improved(10))
print()
# print(fibonacci_improved(8))
print()
print(fibonacci_improved(5))
print()
print(fibonacci_improved.cache_info())


# CacheInfo(hits=3, misses=6, maxsize=4, currsize=4)

### Adding Information About Units  # noqa
def set_unit(unit):
    """Register a unit on a function"""

    def decorator_set_unit(func):
        func.unit = unit
        return func

    return decorator_set_unit


@set_unit("cm^3")
def volume(radius, height):
    return math.pi * radius ** 2 * height


print(volume(3, 5))  # 141.3716694115407
print(volume.unit)  # cm^3
