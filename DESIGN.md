# Nota de diseno: Triage Queue

## Estructura de datos elegida

Se implementa `TriageQueue` con **tres colas FIFO independientes** (`collections.deque`), una por nivel de triaje:

- Nivel 1 (critico)
- Nivel 2 (urgente)
- Nivel 3 (estandar)

### Por que esta estructura

1. Garantiza prioridad global sin reordenar toda la cola en cada insercion.
2. Mantiene FIFO estricto dentro de cada nivel de forma natural (`append` + `popleft`).
3. Permite operaciones simples y eficientes:
- `enqueue`: O(1)
- `dequeue`: O(1) amortizado (revisa maximo 3 colas)
- `peek`: O(1) amortizado
- `list_queue`: O(n)
- `stats`: O(1)

## Alternativas consideradas

- Una sola `deque`: no permite prioridad por nivel sin reordenar/manualmente insertar en posiciones.
- Lista ordenada: insercion O(n) y mas compleja para conservar estabilidad FIFO.
- `heapq`: valida, pero agrega complejidad para FIFO estricto (desempates y snapshot para listar).

## Escenario de mutacion concurrente (conceptual)

Si un worker hace `dequeue()` mientras otro hace `enqueue()` de un paciente critico, se evita doble procesamiento definiendo orden de mutacion atomico en cada operacion:

1. `enqueue`: validar paciente -> insertar en la cola de su nivel -> operacion termina.
2. `dequeue`: elegir primera cola no vacia por prioridad (1,2,3) -> extraer con `popleft` exactamente una vez -> operacion termina.

En un entorno real multi-thread o multi-proceso, estas secciones criticas deben protegerse con sincronizacion (por ejemplo `threading.Lock`) o mediante una cola transaccional externa para asegurar exclusiones mutuas.
