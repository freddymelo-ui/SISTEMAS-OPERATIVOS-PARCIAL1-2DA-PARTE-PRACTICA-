# SISTEMAS-OPERATIVOS-PARCIAL1-2DA-PARTE-PRACTICA-

El algoritmo de planificación de multinivel (MLQ) o colas Multinivel, es una técnica de planificación, la diferencia entre esta y otros modelos de planificación como RR, FIFO, SJF entre otros es que divide la cola de procesos listos en varias sub colas separadas para un tipo de proceso específico, es importante aclarar que cada sub cola tiene su propio algoritmo de planificación anteriormente vistos.

Para una implementación de este algoritmo en la programación se toma en cuenta los siguientes parámetros:

Número de colas
Algoritmo de planificación en cada cola.
Algoritmo de planificación entre colas.
Método de asignación de proceso.

Las razones por las cuales el algoritmo MQL se usa hoy en día en los sistemas operativos es con el fin de dar un trato más flexible a los procesos que se están ejecutando dando lugar a una mejor optimización del sistema dando lugar a la implementación de prioridades absolutas y bajo costo de conmutación.

También se consideran los tipos de procesos, dependiendo del tipo y su naturaleza, se le dará el nivel de prioridad y el algoritmo adecuado que mejor se adapte.

Procesos interactivos
Procesos por lotes
Procesos del sistema

A continuacion daré los puntos mas importantes para dar con el codigo enfocado en programacion a objetos teniendo en cuenta la informacion anterior:

