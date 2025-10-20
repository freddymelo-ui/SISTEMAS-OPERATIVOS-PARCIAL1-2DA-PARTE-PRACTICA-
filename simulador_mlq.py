import collections
import os # Importamos 'os' para verificar si un archivo existe

# === 1. CLASE PROCESO: La Unidad de Trabajo ===
class Proceso:
    """
    Representa un proceso con todos sus atributos y métricas de rendimiento.
    """
    def __init__(self, etiqueta, bt, at, q, pr):
        # Atributos de Entrada
        self.etiqueta = etiqueta            # Identificación (p1, p2, etc.)
        self.burst_time = int(bt)           # Tiempo total requerido de CPU (BT)
        self.arrival_time = int(at)         # Momento de llegada al sistema (AT)
        self.cola = int(q)                  # Cola a la que pertenece (Q)
        self.prioridad = int(pr)            # Prioridad (5 > 1)

        # Atributos de Estado
        self.tiempo_restante = self.burst_time  # Tiempo que aún falta por ejecutar
        self.ha_iniciado = False                # Bandera para calcular el tiempo de respuesta (RT)

        # Atributos de Salida (Métricas)
        self.completion_time = 0
        self.response_time = -1
        self.waiting_time = 0
        self.turnaround_time = 0

    def ejecutar(self, tiempo_a_ejecutar, tiempo_actual):
        """ Reduce el tiempo restante y registra el momento de la primera ejecución. """
        if not self.ha_iniciado:
            # Cálculo del Response Time (RT)
            self.response_time = tiempo_actual - self.arrival_time
            self.ha_iniciado = True
        self.tiempo_restante -= tiempo_a_ejecutar

    def calcular_metricas_finales(self, tiempo_finalizacion):
        """ Calcula las métricas una vez que el proceso ha terminado. """
        self.completion_time = tiempo_finalizacion
        self.turnaround_time = self.completion_time - self.arrival_time
        self.waiting_time = self.turnaround_time - self.burst_time

    def esta_terminado(self):
        """ Verifica si el proceso ha completado su ejecución. """
        return self.tiempo_restante <= 0

    def obtener_datos_salida(self):
        """ Devuelve una tupla con todos los datos requeridos para el archivo de salida. """
        return (
            self.etiqueta, self.burst_time, self.arrival_time, self.cola, self.prioridad,
            self.waiting_time, self.completion_time, self.response_time, self.turnaround_time
        )

# === 2. CLASE COLA DE PLANIFICACIÓN: Define la Política ===
class ColaPlanificacion:
    """ Clase base para una cola de planificación. """
    def __init__(self, politica, quantum=0):
        self.politica = politica
        self.quantum = quantum
        self.procesos_listos = collections.deque()

    def agregar_proceso(self, proceso):
        self.procesos_listos.append(proceso)

    def tiene_procesos(self):
        return len(self.procesos_listos) > 0

    def devolver_proceso(self, proceso):
        self.procesos_listos.append(proceso)

# --- CLASES HIJAS (POLÍTICAS ESPECÍFICAS) ---
class ColaRR3(ColaPlanificacion):
    def __init__(self):
        super().__init__("RR(3)", quantum=3)

    def obtener_siguiente_ejecucion(self, tiempo_actual):
        if not self.tiene_procesos():
            return None, 0
        proceso = self.procesos_listos.popleft()
        tiempo_ejecutar = min(self.quantum, proceso.tiempo_restante)
        return proceso, tiempo_ejecutar

class ColaRR5(ColaPlanificacion):
    def __init__(self):
        super().__init__("RR(5)", quantum=5)

    def obtener_siguiente_ejecucion(self, tiempo_actual):
        if not self.tiene_procesos():
            return None, 0
        proceso = self.procesos_listos.popleft()
        tiempo_ejecutar = min(self.quantum, proceso.tiempo_restante)
        return proceso, tiempo_ejecutar

class ColaFCFS(ColaPlanificacion):
    def __init__(self):
        super().__init__("FCFS", quantum=0)

    def obtener_siguiente_ejecucion(self, tiempo_actual):
        if not self.tiene_procesos():
            return None, 0
        proceso = self.procesos_listos.popleft()
        tiempo_ejecutar = proceso.tiempo_restante
        return proceso, tiempo_ejecutar

# === 3. CLASE SIMULADOR MLQ: El Motor de Orquestación ===
class SimuladorMLQ:
    """
    Gestiona las múltiples colas, el reloj del sistema y la ejecución general.
    """
    def __init__(self):
        self.colas = {
            1: ColaRR3(), 2: ColaRR5(), 3: ColaFCFS()
        }
        self.tiempo_actual = 0
        self.procesos_iniciales = []
        self.procesos_finalizados = []
        self.procesos_por_llegar = collections.deque()

    def cargar_procesos(self, nombre_archivo):
        """ Lee el archivo de entrada, crea objetos Proceso y los prepara. """
        try:
            with open(nombre_archivo, 'r') as f:
                for linea in f:
                    if linea.strip() and not linea.startswith('#'):
                        partes = linea.strip().replace(':', ';').split(';')
                        if len(partes) >= 5:
                            etiqueta, bt, at, q, pr = [p.strip() for p in partes[:5]]
                            proceso = Proceso(etiqueta, bt, at, q, pr)
                            self.procesos_iniciales.append(proceso)

            self.procesos_iniciales.sort(key=lambda p: p.arrival_time)
            self.procesos_por_llegar = collections.deque(self.procesos_iniciales)
            print(f"✅ Procesos cargados desde '{nombre_archivo}'. Total: {len(self.procesos_iniciales)}")
            return True

        except FileNotFoundError:
            print(f"❌ Error: Archivo '{nombre_archivo}' no encontrado. Asegúrese de que existe.")
            return False
        except Exception as e:
            print(f"❌ Error al procesar el archivo: {e}")
            return False

    def _mover_procesos_al_sistema(self):
        """ Mueve los procesos listos a su cola de planificación. """
        while self.procesos_por_llegar and self.procesos_por_llegar[0].arrival_time <= self.tiempo_actual:
            proceso = self.procesos_por_llegar.popleft()
            cola_id = proceso.cola
            
            if cola_id in self.colas:
                self.colas[cola_id].agregar_proceso(proceso)

    def _hay_procesos_pendientes(self):
        """ Verifica si todavía hay trabajo por hacer. """
        colas_con_trabajo = any(cola.tiene_procesos() for cola in self.colas.values())
        return self.procesos_por_llegar or colas_con_trabajo

    def ejecutar_simulacion(self):
        """ Ciclo principal de la simulación de MLQ. Prioridad estricta. """
        print(f"⚙️ Iniciando Simulación en t={self.tiempo_actual}...")

        while self._hay_procesos_pendientes():
            
            self._mover_procesos_al_sistema()
            
            proceso_ejecutar = None
            tiempo_ejecutar = 0
            
            # 1. Búsqueda por estricta prioridad (Cola 1 > Cola 2 > Cola 3)
            if self.colas[1].tiene_procesos():
                proceso_ejecutar, tiempo_ejecutar = self.colas[1].obtener_siguiente_ejecucion(self.tiempo_actual)
            
            elif self.colas[2].tiene_procesos():
                proceso_ejecutar, tiempo_ejecutar = self.colas[2].obtener_siguiente_ejecucion(self.tiempo_actual)
            
            elif self.colas[3].tiene_procesos():
                proceso_ejecutar, tiempo_ejecutar = self.colas[3].obtener_siguiente_ejecucion(self.tiempo_actual)
            
            # 2. Ejecución y Actualización del Reloj
            if proceso_ejecutar and tiempo_ejecutar > 0:
                
                proceso_ejecutar.ejecutar(tiempo_ejecutar, self.tiempo_actual)
                self.tiempo_actual += tiempo_ejecutar
                
                # 3. Manejo del Estado Post-Ejecución
                if proceso_ejecutar.esta_terminado():
                    proceso_ejecutar.calcular_metricas_finales(self.tiempo_actual)
                    self.procesos_finalizados.append(proceso_ejecutar)
                else:
                    self.colas[proceso_ejecutar.cola].devolver_proceso(proceso_ejecutar)
            
            elif self.procesos_por_llegar:
                # IDLE: Avanzamos al tiempo de llegada del siguiente proceso.
                self.tiempo_actual = self.procesos_por_llegar[0].arrival_time
            else:
                break


        print(f"✅ Simulación finalizada en el tiempo: {self.tiempo_actual}")
        self.procesos_finalizados.sort(key=lambda p: p.etiqueta)

    def generar_resultados(self, nombre_archivo_entrada, nombre_archivo_salida):
        """ Escribe los resultados individuales y promedio en el archivo de salida. """
        if not self.procesos_finalizados:
            print("No hay procesos finalizados para generar resultados.")
            return

        total_procesos = len(self.procesos_finalizados)
        sum_wt = sum(p.waiting_time for p in self.procesos_finalizados)
        sum_ct = sum(p.completion_time for p in self.procesos_finalizados)
        sum_rt = sum(p.response_time for p in self.procesos_finalizados)
        sum_tat = sum(p.turnaround_time for p in self.procesos_finalizados)

        # Cálculo de promedios
        avg_wt = sum_wt / total_procesos
        avg_ct = sum_ct / total_procesos
        avg_rt = sum_rt / total_procesos
        avg_tat = sum_tat / total_procesos

        try:
            with open(nombre_archivo_salida, 'w') as f:
                f.write(f"#archivo: {nombre_archivo_entrada}\n")
                f.write("#etiqueta; BT; AT; Q; Pr; WT; CT; RT; TAT\n")

                for p in self.procesos_finalizados:
                    datos = p.obtener_datos_salida()
                    f.write(f"{datos[0]};{datos[1]}; {datos[2]}; {datos[3]}; {datos[4]}; {datos[5]}; {datos[6]}; {datos[7]}; {datos[8]}\n")

                f.write(f"\n$WT={avg_wt:.1f}$; $CT={avg_ct:.1f}$; $RT={avg_rt:.1f}$; $TAT={avg_tat:.1f}$;\n")

            print(f"📊 Resultados generados en '{nombre_archivo_salida}'.")

        except Exception as e:
            print(f"❌ Error al escribir el archivo de salida: {e}")

# === UTILITY: Crea el mlq001.txt de prueba si no existe ===
def crear_mlq001_si_no_existe(nombre_archivo):
    """ Crea el archivo mlq001.txt si no se encuentra en la carpeta. """
    if not os.path.exists(nombre_archivo):
        try:
            with open(nombre_archivo, 'w') as f:
                f.write("# Archivo: mlq001.txt\n")
                f.write("#etiqueta; burst time (BT); arrival time (AT); Queue (Q): Priority(5>1)\n")
                f.write("A;6; 0; 1; 5\n") # Cola 1: RR(3)
                f.write("B;9; 0; 1; 4\n") # Cola 1: RR(3)
                f.write("C;10; 0; 2; 3\n") # Cola 2: RR(5)
                f.write("D;15; 0; 2; 3\n") # Cola 2: RR(5)
                f.write("E;8; 0; 3; 2\n") # Cola 3: FCFS
            print(f"📝 Archivo de entrada de prueba '{nombre_archivo}' creado automáticamente.")
        except Exception as e:
            print(f"Error al crear {nombre_archivo}: {e}")

# === EJECUCIÓN MÚLTIPLE AUTOMÁTICA ===
if __name__ == '__main__':
    
    # Lista de archivos que se deben ejecutar
    ARCHIVOS_A_EJECUTAR = [
        "mlq001.txt", 
        "mlq002.txt", 
        "mlq003.txt"
    ]
    
    # Aseguramos que el archivo de prueba básico (mlq001.txt) exista
    crear_mlq001_si_no_existe("mlq001.txt")
    
    print("--- INICIANDO EJECUCIÓN AUTOMÁTICA PARA MLQ001, MLQ002 Y MLQ003 ---")

    for archivo_entrada in ARCHIVOS_A_EJECUTAR:
        print(f"\n====================== Procesando: {archivo_entrada} ======================")
        
        # Generamos el nombre del archivo de salida
        archivo_salida = f"resultados_{archivo_entrada.replace('.txt', '')}.txt"
        
        # 1. Crear nueva instancia del simulador
        simulador = SimuladorMLQ()

        # 2. Cargar procesos del archivo actual
        if simulador.cargar_procesos(archivo_entrada):
            
            # 3. Ejecutar la simulación
            simulador.ejecutar_simulacion()

            # 4. Generar y guardar los resultados
            simulador.generar_resultados(archivo_entrada, archivo_salida)
        
        print("==================================================================")
    
    print("\nPROCESO FINALIZADO. Revise los archivos 'resultados_mlqXXX.txt'")
    