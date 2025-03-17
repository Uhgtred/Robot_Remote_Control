import androidx.compose.foundation.Image
import androidx.compose.runtime.*
import androidx.compose.ui.graphics.*
import androidx.compose.ui.window.*
import androidx.compose.ui.res.*
import kotlinx.coroutines.*
import java.awt.image.BufferedImage
import javax.imageio.ImageIO
import java.net.Socket


fun imageReceiver() {
    val frameState = remember { mutableStateOf<BufferedImage?>(null) }

    // Coroutine to simulate loading frames at 15 FPS
    LaunchedEffect(Unit) {
        val socket = Socket("192.168.178.32", 2003) // Todo: those variables should be given to this method by the api or socket (api probably better).
        val input = socket.getInputStream()

        while (true) {
            // Read frame size
            val sizeBytes = ByteArray(4)
            input.read(sizeBytes)
            val size = sizeBytes.fold(0) { acc, byte -> (acc shl 8) or (byte.toInt() and 0xFF) }

            // Read frame buffer
            val buffer = ByteArray(size)
            input.readFully(buffer)

            // Load BufferedImage for rendering
            val image = ImageIO.read(buffer.inputStream())
            frameState.value = image

            delay(1000L / 15L) // 15 FPS
        }
    }

    // Display the frame using Compose
    Window(onCloseRequest = ::exitApplication) {
        val image = frameState.value
        if (image != null) {
            Image(bitmap = image.toComposeImageBitmap(), contentDescription = "Video Frame")
        }
    }
}

// Extension to convert a BufferedImage to Compose's ImageBitmap
fun BufferedImage.toComposeImageBitmap(): ImageBitmap {
    return org.jetbrains.skia.Image.makeFromBitmap(this).toComposeImageBitmap()
}
