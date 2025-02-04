import timeit
def measure_time(func):
    def wrapper(*args, **kwargs):
        start_time = timeit.default_timer()
        result = func(*args, **kwargs)
        end_time = timeit.default_timer()
        execution_time = end_time - start_time
        # print(f"Время выполнения {func.__name__}={execution_time} секунд")
        return result

    return wrapper