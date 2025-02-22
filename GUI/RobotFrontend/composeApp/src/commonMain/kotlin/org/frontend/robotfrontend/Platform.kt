package org.frontend.robotfrontend

interface Platform {
    val name: String
}

expect fun getPlatform(): Platform