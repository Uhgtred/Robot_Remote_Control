//package org.frontend.robotfrontend
//
//// androidMain
//actual class ImageStreamObserver actual constructor(directoryPath: String, onImageUpdated: (Image) -> Unit) :
//    FileObserver(directoryPath, CREATE) {
//
//    actual fun startObserving() {
//        startWatching()
//    }
//
//    actual fun stopObserving() {
//        stopWatching()
//    }
//
//    override fun onEvent(event: Int, path: String?) {
//        // Android-specific implementation
//    }
//}
//
//// Android-specific image implementation
//actual typealias Image = android.graphics.Bitmap