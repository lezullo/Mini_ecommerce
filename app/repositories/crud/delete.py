import abc


class CRUDDelete(abc.ABC):

    @abc.abstractmethod
    def remove(self, model, id):
        pass
