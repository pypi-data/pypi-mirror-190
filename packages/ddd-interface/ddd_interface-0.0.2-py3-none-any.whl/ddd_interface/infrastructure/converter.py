class Converter:
    def to_entity(self, dto):
        raise NotImplementedError

    def to_do(self, x):
        raise NotImplementedError