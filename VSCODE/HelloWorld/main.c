#include <stdint.h>

// Función principal del firmware (equivalente a main() en sistemas embebidos)
void app_main() {
    // Ejemplo: Parpadear un LED conectado al GPIO2
    volatile uint32_t *gpio_out = (volatile uint32_t*)0x3FF44004;  // Dirección de GPIO_OUT_REG
    *gpio_out |= (1 << 2);  // Configurar GPIO2 como salida

    while(1) {
        *gpio_out ^= (1 << 2);  // Alternar el estado del LED
        for(volatile int i=0; i<500000; i++);  // Delay aproximado
    }
}

// Función de inicialización básica (llamada desde startup.S)
void hardware_init() {
    // Configurar el reloj del sistema (simplificado)
    volatile uint32_t *rtc_cntl = (volatile uint32_t*)0x3FF48000;
    *rtc_cntl |= (1 << 8);  // Habilitar reloj principal
}