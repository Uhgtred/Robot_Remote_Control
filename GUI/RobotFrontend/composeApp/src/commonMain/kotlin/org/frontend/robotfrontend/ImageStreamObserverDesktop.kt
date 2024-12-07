package org.frontend.robotfrontend

// jvmMain
actual class ImageStreamObserver actual constructor(directoryPath: String, onImageUpdated: (Image) -> Unit) {
    actual fun startObserving() {
        // Implement using WatchService or similar
    }

    actual fun stopObserving() {
        // Stop logic for WatchService, if needed
    }
}

// JVM-specific image implementation
actual typealias Image = java.awt.image.BufferedImage