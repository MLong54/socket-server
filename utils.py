import time


def log(*args, **kwargs):
    # time.time() 返回 unix time
    time_format = '%Y/%m/%d %H:%M:%S'
    localtime = time.localtime(int(time.time()))
    formatted = time.strftime(time_format, localtime)
    with open('log.txt', 'a', encoding='utf-8') as f:
        print(formatted, *args, **kwargs)
        print(formatted, *args, file=f, **kwargs)


def format_time(models):
    if not hasattr(models, '__iter__'):
        models = [models]

    for model in models:
        model.created_time = change_time(model.created_time)
        model.updated_time = change_time(model.updated_time)


def change_time(_time):
    time_format = '%Y/%m/%d %H:%M:%S'
    localtime = time.localtime(_time)
    return time.strftime(time_format, localtime)
