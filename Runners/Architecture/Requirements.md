# Requirements Runners

# Table of contents

<!-- TOC -->
* [ProcessRunner](#processrunner)
* [ThreadRunner](#threadrunner)
* [AsyncRunner](#asyncrunner)
<!-- TOC --> 

---
___
## ProcessRunner:

* For operations that only require CPU-bound operations rather than I/O operations it is necessary to implement a process-runner.
* The process-runner shall be able to:
  1. spawn new processes
  2. kill running processes, that have been spawned by the process-runner
  3. pass arguments to the operation that will be running in the newly spawned process
  4. provide the possibility of communication between the main-program and the running processes
  5. spawn new processes during runtime

---
## ThreadRunner:

* For operations that require mostly I/O operations it is necessary to implement a thread-runner
* The thread-runner shall be able to: 
  1. create and start a new thread 
  2. keep track of any running threads and wait for them to finish their job before closing the main-program
  3. send a flag to the running threads, that the current operation has to be cancelled in order to quit the program ordinary
  4. pass arguments to the operation that will be running in the newly created thread
  5. provide a possibility of communication between the main-program and the running threads 
  6. add new threads during runtime

---
## AsyncRunner

* For operations that are waiting on events or input-operations it is necessary to implement an async-runner.
* The async-runner shall be able to: 
  1. create and start coroutines
  2. keep track of running coroutines and wait for them to finish their job before closing the main-program
  3. send a flag to the running (or waiting) coroutines, that the current operation has to be cancelled in order to quit the program ordinary
  4. pass arguments to the operation that will be running in the newly created coroutine
  5. provide a possibility of communication between the main-program and the running (or waiting) coroutine
  6. add new coroutines at runtime