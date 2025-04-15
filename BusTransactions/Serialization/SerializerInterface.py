from abc import abstractmethod, ABC


class SerializerInterface(ABC):

    @abstractmethod
    def serialize(self, data: any) -> bytes:
        pass

    @abstractmethod
    def deSerialize(self, serializedData: bytes) -> any:
        pass