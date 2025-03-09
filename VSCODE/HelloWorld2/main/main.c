#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"

#define LED_GPIO GPIO_NUM_2  // Pin del LED integrado en la placa ESP32

void app_main(void) {
    gpio_set_direction(LED_GPIO, GPIO_MODE_OUTPUT);
    while (1) {
        gpio_set_level(LED_GPIO, 1);  // Encender LED
        vTaskDelay(1000 / portTICK_PERIOD_MS);  // Esperar 1 segundo
        gpio_set_level(LED_GPIO, 0);  // Apagar LED
        vTaskDelay(1000 / portTICK_PERIOD_MS);  // Esperar 1 segundo
    }
}