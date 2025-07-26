#!/usr/bin/env python3
# @author   Markus Kösters

import ProjectLogging
import Runners
from BusTransactions.AbstractBus import AbstractBus
from BusTransactions.DefaultBusFactory import DefaultBusFactory
# Todo: This line will not be needed anymore, using the new frontend.
#       For now it will stay in, just to get the video-transmission done and get some progress for this project
#       For the long future, kotlin is going to be used as a frontend, since kotlin supports mobile development and web.
# Todo: For now this will not be used. Maybe some time, this is going to substitute The VideoGUI_Controller
# from Remote.MainGUI import MainGUI
from GUI.VideoGUI_Contoller import VideoGUI_Controller
from Runners import ThreadRunner
from SteeringInput import SteeringDeviceFactory, SteeringDevice


class Main:
    """
    Central class for managing asynchronous and threaded tasks, configuring
    controllers, and handling video reception.

    This class serves as the primary orchestrator for initializing task
    runners, setting up controllers, and receiving video streams from
    the robot. It includes initialization of asynchronous and threaded
    task runners, reading the controller, and managing communication ports.
    """

    __ports: dict = {
        # Dictionary defining the socket-assignment.
        'controllerPort': 2001,
        'APIPort': 3000,
        'videoPort': 2002,
        'internalVideoPort': 2003
    }

    __logger: ProjectLogging.Logger.getLogger = ProjectLogging.Logger('Main',
                                                                      'MainLog.log').getLogger
    def __init__(self):
        """
        Initializes the instance of the class and sets up required runners and configurations.

        The __init__ method is responsible for creating instances of AsyncRunner and
        ThreadRunner. It also invokes the setup method to initialize any necessary
        configurations or states for the instance.

        Attributes
        ----------
        __threadRunner : ThreadRunner
            The instance of ThreadRunner to handle multithreaded tasks.
        """
        # Initializing a logger. The loglevel can globally be set in 'ProjectLogging.Logger'.
        self.__logger.info('Initializing Remote-Program...')
        self.__threadRunner: Runners.AbstractRunner = ThreadRunner()
        self.videoController: VideoGUI_Controller | None = None
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
            """
            Add any setup-code here.
            """
            self.__setupReadController()
            self.__setupReceiveVideo()
            self.__threadRunner.runTasks()
            self.__logger.info('Setup completed!')
        except Exception as exceptionMessage:
            exceptionMessage: str = f'Exception occurred during setup: {exceptionMessage}'
            self.__logger.error(exceptionMessage)
            raise BaseException(exceptionMessage)
        # This is needed to run the tk-inter mainloop inside the main-thread.
        if self.videoController:
            self.videoController.runMainLoop()
        else:
            raise BaseException(f'The VideoController has not been initialized.')

    def __setupReadController(self) -> None:
        """
        Sets up a controller device and processes its data.

        This method initializes and starts the controller program by creating a UDP
        transceiver instance for communication, and a controller instance
        to read input data. The controller input is then asynchronously processed
        with a task added to the async runner for relaying messages to the UDP bus.
        """
        self.__logger.info('Starting controller-program...')
        udpBus: AbstractBus = DefaultBusFactory.produceUDP_Transceiver(port=self.__ports.get('controllerPort'))
        self.__logger.debug(f'UDPTransceiverObject: {udpBus}')
        controller: SteeringDevice = SteeringDeviceFactory.produceController()
        self.__logger.debug(f'SteeringDeviceObject: {controller}')
        self.__threadRunner.addTask(controller.readController, udpBus.writeSingleMessage)
        self.__logger.info('Controller-program started!')

    def __setupReceiveVideo(self) -> None:
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
        udpBus: AbstractBus = DefaultBusFactory.produceUDP_ImageDataTransceiver(port=self.__ports.get('videoPort'))
        self.videoController: VideoGUI_Controller = VideoGUI_Controller()
        self.__threadRunner.addTask(udpBus.readBusUntilStopFlag, self.videoController.updateRootView)
        self.__logger.info('Video-receiver started!')

if __name__ == '__main__':
    main = Main()
