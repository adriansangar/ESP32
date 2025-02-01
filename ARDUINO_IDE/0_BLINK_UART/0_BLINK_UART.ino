#include <stdio.h>
#include "driver/uart.h"
#include "esp_log.h"

#define UART_PORT UART_NUM_0  // UART0 
#define BAUD_RATE 115200      // Baudrate deseado
const int LED_BUILTIN = 2;    // Pin del LED

void setup() {
  pinMode(LED_BUILTIN, OUTPUT); // Configuracion del pin
  setup_serial();               // Seteo del baudrate en la UART
}

void loop() {
  digitalWrite(LED_BUILTIN, HIGH);  // Encendemos LED
  delay(1000);                      // Esperamos un segundo
  printf("Hello World!\n");         // Transmitimos que estamos vivos
  digitalWrite(LED_BUILTIN, LOW);   // Apagamos LED
  delay(1000);                      // Esperamos un segundo
}

void setup_serial() {
    // Configuración de los parámetros del UART
    uart_config_t uart_config = {
        .baud_rate = BAUD_RATE,
        .data_bits = UART_DATA_8_BITS,
        .parity = UART_PARITY_DISABLE,
        .stop_bits = UART_STOP_BITS_1,
        .flow_ctrl = UART_HW_FLOWCTRL_DISABLE
    };
    uart_param_config(UART_PORT, &uart_config);

    // Instala el driver del UART (sin buffer)
    uart_driver_install(UART_PORT, 1024, 0, 0, NULL, 0);
}
