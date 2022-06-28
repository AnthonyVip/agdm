# -*- coding: UTF-8 -*


def singleton(class_):
    """Definos el decorador del patron
    de diseño singleton. """
    instances = {}

    def get_instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return get_instance
