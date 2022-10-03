from rest_framework.routers import Route, SimpleRouter


class ExtendedEndpointRouter(SimpleRouter):
    """Кастомный роутер.

    Используется для endpoint `избранное`, `подписки` и `список покупок`.
    Обрабатывает только три действия `list`, `create`, `destroy`"""
    routes = [
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={'get': 'list', 'post': 'create', 'delete': 'destroy'},
            name='{basename}-list',
            detail=False,
            initkwargs={}
        )
    ]