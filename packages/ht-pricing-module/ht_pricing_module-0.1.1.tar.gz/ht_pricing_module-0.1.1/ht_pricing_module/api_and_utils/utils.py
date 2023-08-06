class Struct(dict):
    def __init__(self, *args, **kwargs) -> None:
        super(Struct, self).__init__(*args, **kwargs)

    def __getattr__(self, key):
        value = self[key]
        if isinstance(value, dict):
            value = Struct(value)
        return value
