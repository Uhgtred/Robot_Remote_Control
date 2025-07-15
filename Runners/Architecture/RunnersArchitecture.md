# Architecture for Runners

## Component-View
```plantuml
hide empty members

abstract class AbstractRunner

class ThreadRunner
class AsyncRunner
class ProcessRunner

ThreadRunner --|> AbstractRunner: <<implement>>
AsyncRunner --|> AbstractRunner: <<implement>>
ProcessRunner --|> AbstractRunner: <<implement>>  
```

---
___

## Class-View

### ThreadRunner
```plantuml
hide empty members
abstract class AbstractRunner{
    addTask(task: callable, *args, **kwargs)
    runTask(...)
    runTaskPool(...)
    stopTask(...)
    stopTaskPool(...)
}
 
class ThreadRunner{
    - __activeThreads: set[threading.Thread]
    - __threadLock: threading.Lock
    - __createThreadFromTask(task: callable, *args, **kwargs)
    - __joinThread(thread: threading.Thread)
}

ThreadRunner --|> AbstractRunner: <<implement>>

```

### ProcessRunner

```plantuml
hide empty members 
abstract class AbstractRunner{
    addTask(task: callable, *args, **kwargs)
    runTask(...)
    runTaskPool(...)
    stopTask(...)
    stopTaskPool(...)
}

class ProcessRunner{
    - __activeProcesses: set[multiprocessing.Process]
    __createProcessFromTask(task: callable, *args, **kwargs)
    
}

ProcessRunner --|> AbstractRunner: <<implement>>
```

---
## Sequence View

```plantuml
actor client

participant TaskManager
participant ThreadRunner
participant ProcessRunner
participant AsyncRunner

client -> TaskManager: runTask(engine: AbstractRunner, task: callable, *args, **kwargs)
TaskManager -> ThreadRunner: runTask(task: callable, *args, **kwargs)
ThreadRunner --> TaskManager: thread
 
client -> TaskManager: runTask(engine: AbstractRunner, task: callable, *args, **kwargs)
TaskManager -> ProcessRunner: runTask(task: callable, *args, **kwargs)
ProcessRunner --> TaskManager: process

client -> TaskManager: runTask(engine: AbstractRunner, task: callable, *args, **kwargs)
TaskManager -> AsyncRunner: runTask(task: callable, *args, **kwargs)
AsyncRunner --> TaskManager: coroutine

```