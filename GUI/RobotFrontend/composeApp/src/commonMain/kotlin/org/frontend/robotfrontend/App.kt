package org.frontend.robotfrontend

import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material.Button
import androidx.compose.material.Icon
import androidx.compose.material.MaterialTheme
import androidx.compose.material.TopAppBar
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.Menu
import androidx.compose.material.icons.filled.Settings
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.unit.dp
import org.jetbrains.compose.ui.tooling.preview.Preview
import androidx.compose.ui.graphics.ImageBitmap
import androidx.compose.ui.graphics.asImageBitmap

@Composable
@Preview
fun App() {
    // Variable for the image to be stored in.
    var imageBitmap by remember { mutableStateOf<ImageBitmap?>(null) }

    // List of images that will be set as icons of buttons
    val topAppBarButtons: List<ImageVector> = remember { listOf(Icons.Default.Menu, Icons.Default.Home, Icons.Default.Settings) }
    // Placing the TopAppBar-Buttons
    MaterialTheme {
        TopAppBar() {
            Column(Modifier.fillMaxSize()) {
                Row(Modifier.align(Alignment.Start).fillMaxWidth()) {
                    topAppBarButtons.forEach { barButtons ->
                        Button(onClick = {}, modifier = Modifier.padding(10.dp)) {
                            Icon(barButtons, "")
                        }
                    }
                }
            }
        }
    }
    Box(modifier = Modifier.fillMaxSize()) {
        imageBitmap?.let { bitmap ->
            Image(
                bitmap = bitmap.asImageBitmap(),
                contentDescription = null,
                modifier = Modifier.fillMaxSize(),
                contentScale = ContentScale.Crop // Adjust contentScale as needed
            )
        }
    }
}
