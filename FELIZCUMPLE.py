import random
import time
from typing import List, Tuple, Optional

# Constantes para identificar al jugador
PROFESOR = 0
HERMANA = 1

# ---------------------------------------------------
# Funciones auxiliares
# ---------------------------------------------------

def prefix_sums(arr: List[int]) -> List[int]:
    """
    Calcula los prefijos acumulativos de un arreglo.
    Permite obtener sumas de subarreglos en O(1).
    """
    ps = [0]
    for x in arr:
        ps.append(ps[-1] + x)
    return ps

def range_sum(ps: List[int], i: int, j: int) -> int:
    """
    Retorna la suma de arr[i..j] usando la lista de prefijos ps.
    Devuelve 0 si el rango es inválido.
    """
    if i > j:
        return 0
    return ps[j + 1] - ps[i]

# ---------------------------------------------------
# DP lineal con memoización
# ---------------------------------------------------

def valor_residual_array(bloque: List[int]) -> Tuple[int, List[List[int]], List[List[int]]]:
    """
    Calcula la satisfacción máxima para el bloque residual lineal.
    Retorna:
      - valor máximo que puede obtener el profesor,
      - tabla de elecciones del profesor,
      - tabla de elecciones de la hermana.
    """
    n = len(bloque)
    if n == 0:
        return 0, [], []

    # Prefijos para obtener sumas rápidas
    ps = prefix_sums(bloque)

    # Tablas de memoización con None para detectar estados no calculados
    dp_prof: List[List[Optional[int]]] = [[None]*n for _ in range(n)]
    dp_herm: List[List[Optional[int]]] = [[None]*n for _ in range(n)]
    # Tablas para reconstruir las elecciones óptimas
    eleccion_prof: List[List[int]] = [[0]*n for _ in range(n)]
    eleccion_hermana: List[List[int]] = [[0]*n for _ in range(n)]

    def dp(i: int, j: int, turno: int) -> int:
        """
        Función recursiva para calcular la satisfacción máxima desde A[i..j].
        turno indica quién juega: PROFESOR maximiza, HERMANA minimiza.
        """
        longitud = j - i + 1
        if longitud == 0:
            return 0

        # Caso base: bloque de 1 porción
        if longitud == 1:
            if turno == PROFESOR:
                eleccion_prof[i][j] = 1
                dp_prof[i][j] = bloque[i]
                return dp_prof[i][j]
            else:
                eleccion_hermana[i][j] = 1
                dp_herm[i][j] = 0
                return dp_herm[i][j]

        # Caso especial: bloque de 2 porciones, micro-optimización
        if longitud == 2:
            if turno == PROFESOR:
                eleccion_prof[i][j] = 1
                dp_prof[i][j] = bloque[i]
                return dp_prof[i][j]
            else:
                eleccion_hermana[i][j] = 1
                dp_herm[i][j] = dp(i+1,j,PROFESOR)
                return dp_herm[i][j]

        # Turno del profesor: maximiza ganancia
        if turno == PROFESOR:
            if dp_prof[i][j] is not None:
                return dp_prof[i][j]
            mejor = -10**18
            for k in range(1, longitud):
                candidato = range_sum(ps,i,i+k-1) + dp(i+k,j,HERMANA)
                if candidato > mejor:
                    mejor = candidato
                    eleccion_prof[i][j] = k
            dp_prof[i][j] = mejor
            return mejor
        else:  # Turno de la hermana: minimiza ganancia del profesor
            if dp_herm[i][j] is not None:
                return dp_herm[i][j]
            peor = 10**18
            for k in range(1, longitud):
                candidato = dp(i+k,j,PROFESOR)
                if candidato < peor:
                    peor = candidato
                    eleccion_hermana[i][j] = k
            dp_herm[i][j] = peor
            return peor

    valor_max = dp(0,n-1,HERMANA)  # Tras la primera jugada, le toca a la hermana
    return valor_max, eleccion_prof, eleccion_hermana

# ---------------------------------------------------
# Funciones para el semicirculo inicial
# ---------------------------------------------------

def suma_bloque_circular(torta: List[int], start: int, length: int) -> int:
    """Suma las porciones de un semicirculo de longitud 'length' desde 'start' (circular)"""
    total = 0
    n = len(torta)
    for t in range(length):
        total += torta[(start+t)%n]
    return total

def bloque_residual(torta: List[int], start: int, n: int) -> List[int]:
    """
    Extrae el bloque lineal residual después de que el profesor come un semicirculo.
    Devuelve lista de longitud n.
    """
    m = len(torta)
    return [torta[(start+n+t)%m] for t in range(n)]

# ---------------------------------------------------
# Función principal
# ---------------------------------------------------

def satisfaccion_maxima(torta: List[int]) -> Tuple[int, List[Tuple[int,int,int]]]:
    """
    Calcula la máxima satisfacción total que puede obtener el profesor
    y la secuencia óptima de jugadas (turno, inicio_global, k).
    """
    assert len(torta)%2==0 and len(torta)>=2
    m = len(torta)
    n = m//2
    mejor_total = -10**18
    mejor_inicio = 0
    mejor_eleccion_seq: List[Tuple[int,int,int]] = []

    # Probamos todas las posiciones iniciales del semicirculo
    for start in range(m):
        primera_ganancia = suma_bloque_circular(torta,start,n)
        residual = bloque_residual(torta,start,n)
        valor_max, eleccion_prof, eleccion_herm = valor_residual_array(residual)
        total = primera_ganancia + valor_max
        if total > mejor_total:
            mejor_total = total
            mejor_inicio = start
            # Reconstrucción de la secuencia de jugadas del bloque residual
            seq = []
            i,j = 0,n-1
            turno = HERMANA
            while i<=j:
                if turno==PROFESOR:
                    k = eleccion_prof[i][j]
                    if k == 0:  # seguridad para evitar bucle infinito
                        break
                    seq.append((PROFESOR,i,k))
                    i += k
                else:
                    k = eleccion_herm[i][j]
                    if k == 0:
                        break
                    seq.append((HERMANA,i,k))
                    i += k
                turno = 1-turno
            # Primer movimiento del profesor + bloque residual
            mejor_eleccion_seq = [(PROFESOR,start,n)] + seq

    # Conversión a índices globales para todo el arreglo circular
    secuencia_global = []
    for t, idx, k in mejor_eleccion_seq:
        if t==PROFESOR and idx==0:
            secuencia_global.append((t,(mejor_inicio)%m,k))
        else:
            inicio_global = (mejor_inicio + n + idx)%m
            secuencia_global.append((t,inicio_global,k))

    return mejor_total, secuencia_global

# ---------------------------------------------------
# Ejecución ejemplo
# ---------------------------------------------------

if __name__=="__main__":
    random.seed(42)
    n = 3
    torta = [random.randint(-5,10) for _ in range(2*n)]
    print("Valores de satisfacción de la torta:", torta)

    start_time = time.perf_counter()
    valor, secuencia = satisfaccion_maxima(torta)
    end_time = time.perf_counter()

    print("Satisfacción máxima del profesor:", valor)
    print("Secuencia de jugadas (turno, inicio_global, k):")
    for t, idx, k in secuencia:
        turno_str = "Profesor" if t==PROFESOR else "Hermana"
        print(f"{turno_str} toma desde {idx} k={k}")
    print(f"Tiempo de ejecución: {end_time-start_time:.6f} s")
