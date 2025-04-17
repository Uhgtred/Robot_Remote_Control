from typing import Protocol


class SerializationProtocol(Protocol):

    def serialize(self, data: any) -> bytes:
        pass

    def deSerialize(self, serializedData: bytes) -> any:
        pass