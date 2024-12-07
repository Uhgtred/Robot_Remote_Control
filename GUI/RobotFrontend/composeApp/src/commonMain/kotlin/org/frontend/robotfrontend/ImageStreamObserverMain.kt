package org.frontend.robotfrontend

// commonMain
expect class ImageStreamObserverMain(directoryPath: String, onImageUpdated: (Image) -> Unit) {
    fun startObserving()
    fun stopObserving()
}

// A common representation of an image, which could be platform-specific.
interface Image