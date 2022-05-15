from typing import Optional


class UnexpectedUrlFormat(ValueError):
    def __init__(
            self, *,  url: str=None, city_name: Optional[str]=None, path: Optional[str]=None, qs_param: Optional[str]=None
    ):
        super().__init__()
        self.url = url
        self.city_name = city_name
        self.path = path
        self.qs_param = qs_param

    def __str__(self):
        if self.city_name is not None:
            return f'Unexpected city in the url: {self.city_name}\nOriginal url: {self.url}'

        if self.path is not None:
            return f'Unexpected path: {self.path}\nOriginal url: {self.url}'

        if self.qs_param is not None:
            return f'Unexpected qs parameter: {self.qs_param}\nOriginal url: {self.url}'

        return f'Unexpected url: {self.url}'


class UnexpectedPath(ValueError):
    pass


class UnknownCity(ValueError):
    @property
    def city(self):
        return self.args[0]


class UnexpectedParam(ValueError):
    pass

