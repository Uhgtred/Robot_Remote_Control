// Assuming necessary imports
import android.graphics.Bitmap
import android.os.FileObserver
import android.graphics.BitmapFactory

// TODO: make sure the package is correct for your project
// package org.frontend.robotfrontend

class ImageStreamObserver(
    private val imageDirectoryPath: String,
    private val onImageUpdated: (Bitmap) -> Unit
) : FileObserver(imageDirectoryPath, CREATE) {

    override fun onEvent(event: Int, path: String?) {
        if (event == CREATE && path != null && (path.endsWith(".jpg") || path.endsWith(".jpeg"))) {
            val imagePath = "$imageDirectoryPath/$path"
            val bitmap = BitmapFactory.decodeFile(imagePath)
            if (bitmap != null) {
                onImageUpdated(bitmap)
            } else {
                // Handle the error case where decodeFile might return null
                println("Error decoding image at $imagePath")
            }
        }
    }
}