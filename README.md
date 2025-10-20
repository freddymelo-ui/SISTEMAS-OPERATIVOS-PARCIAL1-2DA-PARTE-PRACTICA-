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

A continuacion daré los puntos mas importantes para entender el codigo enfocado en programacion a objetos teniendo en cuenta la informacion anterior:

1. Para la creacion de un simulador MQL con la estructura RR(3), RR(5), FCFS se toma en cuenta las siguientes clases:
   -  CLASE PROCESO
   -  CLASE DE LOGICA: "ColaPlanificacion"
   -  CLASE DE CONTROL: "Simulador MQL"

2. CLASE PROCESO:
    - Encapsula toda la informacion de una tarea, inicializa el proceso con sus datos de entradas y metricas.
    - Actualiza el estado y reduce el tiempo restante y calcula el tiempo de respuesta.
    - Finalmente calcula el tiempo de respuesta.
  
3. CLASE DE LOGICA:
    - Aqui se usa la Herencia ya que se implementa el esquema seleccionado (RR(3), RR(5), FCFS)
    - La ColaPlanificacion (Base) define la estructura basica de una cola, las colas hijas tales como: RR(3), RR(5) y FCFS, devuelven el proceso y el tiempo restante.
   
4. CLASE DE CONTROL:
    - Usa la composicion y gestiona el reloj del sistema cargando los procesos, moviemdo y ejecutando la simulacion actualizando el estado si está terminado o nó.
  
  
