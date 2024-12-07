package org.frontend.robotfrontend

import androidx.compose.foundation.Image
import androidx.compose.foundation.content.MediaType.Companion.Image
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material.Button
import androidx.compose.material.Colors
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
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.ImageBitmap
import androidx.compose.ui.graphics.luminance
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.semantics.Role.Companion.Image
import androidx.compose.ui.unit.dp
import org.jetbrains.compose.ui.tooling.preview.Preview


@Composable
@Preview
fun App() {
    // Variable for the image to be stored in.
    val imageBitmap by remember { mutableStateOf<ImageBitmap?>(null) } // Todo: implement this
    // value that has an instance of the dataclass defining the colors of the main-theme
    val myColors = MyColors() // Create an instance of MyColors
    // List of images that will be set as icons of buttons
    val topAppBarButtons: List<ImageVector> = remember { listOf(Icons.Default.Menu, Icons.Default.Home, Icons.Default.Settings) }
    // Placing the TopAppBar-Buttons

    MaterialTheme(colors = myColors.toMaterialColors()) {
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
    // Todo: implement this
    Box(modifier = Modifier.fillMaxSize()) {
        imageBitmap?.let { bitmap ->
            Image(
                bitmap = bitmap,
                contentDescription = null,
                modifier = Modifier.fillMaxSize(),
                contentScale = ContentScale.Crop // Adjust contentScale as needed
            )
        }
    }
}

data class MyColors(
    val primary: Color = Color(0xFF6200EE),
    val primaryVariant: Color = Color(0xFF3700B3),
    val secondary: Color = Color(0xFF03DAC5),
    val secondaryVariant: Color = Color.DarkGray,
    val background: Color = Color.DarkGray,
    val surface: Color = Color.DarkGray,
    val error: Color = Color.Red,
    val onPrimary: Color = Color.DarkGray,
    val onSecondary: Color = Color.DarkGray,
    val onBackground: Color = Color.DarkGray,
    val onSurface: Color = Color.DarkGray,
    val onError: Color = Color.DarkGray,
    val isLight: Boolean = false
    // ... other color properties ...
){
    // Extension function to convert MyColors to Material Colors
    fun toMaterialColors(): Colors {
        return Colors(
            primary = this.primary,
            primaryVariant = this.primaryVariant,
            secondary = this.secondary,
            secondaryVariant = this.secondaryVariant,
            background = this.background,
            surface = this.surface,
            error = this.error,
            onPrimary = this.onPrimary,
            onSecondary = this.onSecondary,
            onBackground = this.onBackground,
            onSurface = this.onSurface,
            onError = this.onError,
            isLight = this.isLight
        )
    }
}