from abc import ABCMeta, abstractmethod
from common.discount import Discount


class Scrapper(metaclass=ABCMeta):

    @property
    @abstractmethod
    def source(self) -> str:
        pass

    @abstractmethod
    def get_discounts(self) -> list[Discount]:
        pass
