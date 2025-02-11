#!/usr/bin/env python3
# @author   Markus Kösters

from BusTransactions import Bus
from BusTransactions.BusFactory import BusFactory
from ProjectLogging import Logger
from SteeringInput import SteeringDeviceFactory
#Todo: This line will not be needed anymore, using the new frontend.
from GUI.GUI_Contoller import GUI_Controller
from Runners import threadRunner


# from Remote.MainGUI import MainGUI


class Main:
    """
    Central class for managing asynchronous and threaded tasks, configuring
    controllers, and handling video reception.

    This class serves as the primary orchestrator for initializing task
    runners, setting up controllers, and receiving video streams from
    the robot. It includes initialization of asynchronous and threaded
    task runners, reading the controller, and managing communication ports.
    """

    __ports: dict = {'controllerPort': 2001, 'APIPort': 3000, 'videoPort': 2002}

    def __init__(self):
        """
        Initializes the instance of the class and sets up required runners and configurations.

        The __init__ method is responsible for creating instances of AsyncRunner and
        ThreadRunner. It also invokes the setup method to initialize any necessary
        configurations or states for the instance.

        Attributes
        ----------
        __threadRunner : threadRunner.ThreadRunner
            The instance of ThreadRunner to handle multithreaded tasks.
        """
        self.__logger: Logger.getLogger = Logger('Main', 'Mainlog.log').getLogger
        self.__logger.info('Initializing Remote-Program...')
        self.__threadRunner = threadRunner.ThreadRunner()
        self.videoController: GUI_Controller = None
        self.__setup()
        self.__logger.info('Remote-Program initialized!')

    def __setup(self) -> None:
        """
        Initializes and configures the remote program by performing setup operations.
        This method is used internally to execute the sequence of initialization steps
        required for proper execution of the program. It ensures that the controller
        is read, and all tasks provided by the asynchronous and threaded task runners
        are executed. Initialization begins and ends with log messages indicating the
        program's status.

        :raises RuntimeError: If initialization fails due to issues in the controller
            reading process or task execution in runners.
        """
        try:
            # Add any setup code here
            self.__readController()
            self.__recvVideo()
            self.__threadRunner.runTasks()
            self.__logger.info('Setup completed!')
        except Exception as exceptionMessage:
            exceptionMessage = f'Exception occurred during setup: {exceptionMessage}'
            self.__logger.error(exceptionMessage)
            raise BaseException(exceptionMessage)
        self.videoController.runMainLoop()

    def __readController(self) -> None:
        """
        Sets up a controller device and processes its data.

        This method initializes and starts the controller program by creating a UDP
        transceiver instance for communication, and a controller instance
        to read input data. The controller input is then asynchronously processed
        with a task added to the async runner for relaying messages to the UDP bus.
        """
        self.__logger.info('Starting controller-program...')
        udpBus = BusFactory.produceUDP_Transceiver(host=False, port=self.__ports.get('controllerPort'))
        controller = SteeringDeviceFactory.produceController()
        self.__threadRunner.addTask(controller.readController, udpBus.writeSingleMessage)
        self.__logger.info('Controller-program started!')

    def __recvVideo(self) -> None:
        """
        Receives video data through a UDP bus and updates the relevant GUI components.

        This method initializes a UDP transceiver bus for receiving video data by using the
        provided video port. It retrieves the video port from the instance's configuration. The
        method also utilizes a GUI controller to update the user interface with the received
        video data. The task is registered to the thread runner for execution until a stop flag
        is triggered.

        :raises KeyError: If the 'videoPort' key is not found in `self.__ports`.
        """
        self.__logger.info('Starting video-receiver...')
        udpBus: Bus = BusFactory.produceUDP_ImageDataReceiver(port=self.__ports.get('videoPort'), host=False)
        self.videoController: GUI_Controller = GUI_Controller()
        self.__threadRunner.addTask(udpBus.readBusUntilStopFlag, self.videoController.updateRootView)
        self.__logger.info('Video-receiver started!')

if __name__ == '__main__':
    main = Main()
