from abc import ABC, abstractmethod
"""Abstract class for getting to data"""
class DataConnect(ABC):

    @abstractmethod
    def get_data(self, conf_dic):
        pass

