
package com.minionsparadise.bootstrapper

import android.app.Activity
import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.LinearLayout
import android.widget.TextView
import java.net.HttpURLConnection
import java.net.URL
import java.util.concurrent.Executors

class BootstrapperActivity : Activity() {

    private val executor = Executors.newSingleThreadExecutor()
    private lateinit var serverUrl: EditText
    private lateinit var statusText: TextView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val layout = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(32, 32, 32, 32)
        }

        val title = TextView(this).apply {
            text = "Minions Paradise Bootstrapper"
            textSize = 22f
        }

        serverUrl = EditText(this).apply {
            hint = "Endereço do servidor"
            setSingleLine(true)
            setText("http://10.0.2.2:8000")
        }

        val checkButton = Button(this).apply {
            text = "Verificar servidor"
            setOnClickListener {
                checkServer()
            }
        }

        statusText = TextView(this).apply {
            text = "Aguardando verificação..."
            textSize = 16f
        }

        layout.addView(title)
        layout.addView(serverUrl)
        layout.addView(checkButton)
        layout.addView(statusText)

        setContentView(layout)
    }

    private fun checkServer() {
        val baseUrl = serverUrl.text.toString()
            .trim()
            .trimEnd('/')

        if (baseUrl.isEmpty()) {
            statusText.text = "Informe o endereço do servidor."
            return
        }

        statusText.text = "Verificando servidor..."

        executor.execute {
            val result = try {
                val health = request("$baseUrl/health")
                val config = request("$baseUrl/config")

                """
                Health: HTTP ${health.first}
                ${health.second}

                Config: HTTP ${config.first}
                ${config.second}
                """.trimIndent()
            } catch (error: Exception) {
                "Falha na conexão: ${error.message}"
            }

            runOnUiThread {
                statusText.text = result
            }
        }
    }

    private fun request(endpoint: String): Pair<Int, String> {
        val connection = URL(endpoint)
            .openConnection() as HttpURLConnection

        try {
            connection.requestMethod = "GET"
            connection.connectTimeout = 5000
            connection.readTimeout = 5000

            val responseCode = connection.responseCode

            val stream = if (responseCode in 200..299) {
                connection.inputStream
            } else {
                connection.errorStream
            }

            val body = stream?.bufferedReader()?.use {
                it.readText()
            } ?: ""

            return Pair(responseCode, body)
        } finally {
            connection.disconnect()
        }
    }

    override fun onDestroy() {
        executor.shutdown()
        super.onDestroy()
    }
}
