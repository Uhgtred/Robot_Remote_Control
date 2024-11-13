//Todo: implement this and resolve the errors
//package org.frontend.robotfrontend
//
//class ImageStreamObserver(private val imageDirectoryPath: String, private val onImageUpdated: (Bitmap) -> Unit) :
//    android.os.FileObserver(imageDirectoryPath) {
//    override fun onEvent(event: Int, path: String?) {
//        if (event == android.os.FileObserver.CREATE && path != null && (path.endsWith(".jpg") || path.endsWith(".jpeg"))) {
//            val imagePath = "$imageDirectoryPath/$path"
//            val bitmap = android.graphics.BitmapFactory.decodeFile(imagePath)
//            onImageUpdated(bitmap)
//        }
//    }
//}