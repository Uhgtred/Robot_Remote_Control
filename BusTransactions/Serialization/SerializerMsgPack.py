import msgpack

from BusTransactions.Serialization.SerializationProtocol import SerializationProtocol


class SerializerMsgPack(SerializationProtocol):

    def serialize(self, data: any) -> bytes:
        serializedData: bytes = msgpack.packb(data)
        return serializedData

    def deSerialize(self, serializedData: bytes) -> any:
        deserializedData: any = msgpack.unpackb(serializedData)
        return deserializedData