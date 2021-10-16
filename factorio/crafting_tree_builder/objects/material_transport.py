from abc import abstractmethod


class AMaterialTransport:

    @abstractmethod
    def get_max_rate(self):
        pass


class ItemTransport(AMaterialTransport):
    def get_max_rate(self):
        # todo finish this
        return 10


class FluidTransport(AMaterialTransport):
    def get_max_rate(self):
        return float("inf")
