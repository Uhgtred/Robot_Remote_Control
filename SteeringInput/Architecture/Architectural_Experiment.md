# Strategy-pattern with an additional abstraction-layer.

```plantuml
@startuml
package InputControl{
    abstract class InputDevice{
        -callbackMethod: callable
        -delay: float
        --
        +readInputContinuously(delay: float) -> any
        +writeOutput(message: bytes) -> None
        +setDelay(delay: Delay) -> None
    }
    
    class Delay{
        -delay: float
        --
        +setDelay(time: float) -> None
        +getDelay() -> float
    }
    
    class InputController{
        -inputDevice: InputDevice
        --
        +readInputContinuously(inputDevice: InputDevice) -> None
        +writeOutput(output: ?) -> None
        +setInputDevice(inputDevice: InputDevice)
    }
    
    abstract class AbstractTouchScreen{
        -touchScreenConfig: TouchScreenConfig
        --
    '    overrides readInputContinuously with readTouchScreenInput(touchScreen)
    }
    
    abstract class AbstractController{
        -buttons: ControllerElements
        --
        +readInputContinuously() -> ControllerElementsData 
        +writeOutput(message: bytes) -> None
        +setControllerElements(elements: ControllerElements) -> None
    }
    
    class XboxController{
        -xboxControllerElements: ControllerElements
        --
    }
    
    class PlaystationController{
        -playstationControllerElements: ControllerElements
        --
    }
    
    class xboxControllerElements{
        """
        Probably a data-class
        """
    }
    
    abstract class ControllerElements{
        -vendorID: int 
        -controllerElementsData: ControllerElementsData
        -controllerElements: set   
        ---
        readData() -> ControllerElementsData
        getVendorID() -> vendorID
    }
    
    class ControllerElementsData{
    }
    
    class Button{
        + value: int
        + maxValue: int 
        + minValue: int 
        + defaultValue: int
        ---
    }
    
    abstract class AbstractButton{
        + value: int
        + maxValue: int 
        + minValue: int 
        + defaultValue: int
        ---
    }
    
    class Trigger{
        + value: int 
        + maxValue: int 
        + minValue: int 
        + defaultValue: int
        + deadZone: list[int] 
        ---
    }
    
    abstract class AbstractTrigger{
        + value: int 
        + maxValue: int 
        + minValue: int 
        + defaultValue: int
        + deadZone: list[int] 
        ---
    }
    
    class AnalogStick{
        + value: list[int] 
        + maxValue: list[int] 
        + minValue: list[int]
        + defaultValue: list[int]
        + deadZone: list[int]
        ---
    }
    
    abstract class AbstractAnalogStick{
        + value: list[int] 
        + maxValue: list[int] 
        + minValue: list[int]
        + defaultValue: list[int]
        + deadZone: list[int]
        ---
    }
    
    InputController -d- InputDevice
    InputDevice -l-> Delay
    AbstractTouchScreen .l.|> InputDevice
    AbstractController -u-|> InputDevice
    XboxController -u-|> AbstractController
    XboxController "1" *-d- "1" ControllerElements
    PlaystationController -u-|> AbstractController
    PlaystationController "1" *-d- "1" ControllerElements
    ControllerElements "1" *-r- "1" ControllerElementsData
    ControllerElements "1" *-d- "n" AbstractButton
    AbstractButton <|-d- Button
    ControllerElements "1" *-d- "n" AbstractTrigger
    AbstractTrigger <|-d- Trigger
    ControllerElements "1" *-d- "n" AbstractAnalogStick
    xboxControllerElements --|> ControllerElements
    AbstractAnalogStick <|-d- AnalogStick
}
@enduml
```