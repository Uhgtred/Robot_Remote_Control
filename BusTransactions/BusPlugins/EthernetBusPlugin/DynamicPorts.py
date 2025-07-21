#!/usr/bin/env python3
# @author: Markus Kösters
import typing


class DynamicPorts:
    """
    This needs the information about the dynamic ports and also the ports that are already in use.

    """

    __openSocketPorts: set = ()
    __dynamicPorts: typing.Generator = (intPort for intPort in range(1000,5000,100))

    @classmethod
    def __getDynamicPort(cls) -> int:
        """
        Determines and returns an available port from the dynamic port range.

        This method checks the predefined list of dynamic ports and identifies the
        first port that is not currently in use. If all dynamic ports are in use,
        an exception will be raised.

        :return: The first available port from the dynamic port list.
        :rtype: int

        :raises RuntimeError: If no ports are available in the dynamic port range.
        """
        for port in cls.__dynamicPorts:
            if port not in cls.__openSocketPorts:
                return port
        raise RuntimeError("No available ports in the dynamic port range")

    def __selectPortDynamically(self) -> int:
        """
        Selects and dynamically assigns a port for use. The method internally calls a helper
        function to retrieve an available dynamic port and keeps track of the assigned port
        by adding it to a set of opened socket ports. This ensures that the port is reserved
        for future use.

        :return: Dynamically assigned port number
        :rtype: int
        """
        port = self.__getDynamicPort()
        self.__openSocketPorts.add(port)
        return port