#include <stdint.h>

#define UART0_FIFO 0x3FF40000

int puts(const char *s) {
    volatile uint32_t *fifo = (volatile uint32_t*)UART0_FIFO;
    while (*s) {
        *fifo = *s++;    // envía cada carácter
    }
    *fifo = '\n';       // nueva línea
    return 1;
}

// Función principal del firmware (equivalente a main() en sistemas embebidos)
void app_main() {

    while (1) {
        puts("Loop infinito...\n");      // Envío periódico
        for (volatile int i = 0; i < 500000; i++);
    }
}

// Función de inicialización básica (llamada desde startup.S)
void hardware_init() {
    // Configurar el reloj del sistema (simplificado)
    volatile uint32_t *rtc_cntl = (volatile uint32_t*)0x3FF48000;
    *rtc_cntl |= (1 << 8);  // Habilitar reloj principal
}