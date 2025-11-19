import random
from typing import List, Tuple
import time


# Constantes para identificar al jugador
PROFESOR = 0
HERMANA = 1

# ---------------------------------------------------
# Funciones auxiliares (las mismas que en FELIZCUMPLE.py)
# ---------------------------------------------------

def prefix_sums(arr: List[int]) -> List[int]:
    ps = [0]
    for x in arr:
        ps.append(ps[-1] + x)
    return ps

def range_sum(ps: List[int], i: int, j: int) -> int:
    if i > j:
        return 0
    return ps[j + 1] - ps[i]

def suma_bloque_circular(torta: List[int], start: int, length: int) -> int:
    total = 0
    n = len(torta)
    for t in range(length):
        total += torta[(start+t) % n]
    return total

def bloque_residual(torta: List[int], start: int, n: int) -> List[int]:
    m = len(torta)
    return [torta[(start + n + t) % m] for t in range(n)]

# ---------------------------------------------------
# VERSION HASH DE LA PROGRAMACIÓN DINÁMICA
# ---------------------------------------------------

def valor_residual_hash(bloque: List[int]) -> Tuple[int, dict, dict]:
    """
    DP lineal usando tablas hash (diccionarios).
    Retorna:
      - valor máximo para el profesor
      - eleccion_prof[(i,j)]
      - eleccion_hermana[(i,j)]
    """
    n = len(bloque)
    if n == 0:
        return 0, {}, {}

    ps = prefix_sums(bloque)

    # Tablas hash
    dp_prof = {}            # (i,j) -> valor
    dp_herm = {}            # (i,j) -> valor
    eleccion_prof = {}      # (i,j) -> k
    eleccion_hermana = {}   # (i,j) -> k

    def dp(i: int, j: int, turno: int) -> int:
        longitud = j - i + 1

        if longitud == 0:
            return 0

        # Caso base
        if longitud == 1:
            if turno == PROFESOR:
                eleccion_prof[(i,j)] = 1
                dp_prof[(i,j)] = bloque[i]
                return bloque[i]
            else:
                eleccion_hermana[(i,j)] = 1
                dp_herm[(i,j)] = 0
                return 0

        # Caso especial longitud 2
        if longitud == 2:
            if turno == PROFESOR:
                eleccion_prof[(i,j)] = 1
                dp_prof[(i,j)] = bloque[i]
                return bloque[i]
            else:
                eleccion_hermana[(i,j)] = 1
                val = dp(i+1, j, PROFESOR)
                dp_herm[(i,j)] = val
                return val

        # PROFESOR maximiza
        if turno == PROFESOR:
            if (i,j) in dp_prof:
                return dp_prof[(i,j)]

            mejor = -10**18
            mejor_k = 1
            for k in range(1, longitud):
                candidato = range_sum(ps, i, i+k-1) + dp(i+k, j, HERMANA)
                if candidato > mejor:
                    mejor = candidato
                    mejor_k = k

            dp_prof[(i,j)] = mejor
            eleccion_prof[(i,j)] = mejor_k
            return mejor

        # HERMANA minimiza
        else:
            if (i,j) in dp_herm:
                return dp_herm[(i,j)]

            peor = 10**18
            peor_k = 1
            for k in range(1, longitud):
                candidato = dp(i+k, j, PROFESOR)
                if candidato < peor:
                    peor = candidato
                    peor_k = k

            dp_herm[(i,j)] = peor
            eleccion_hermana[(i,j)] = peor_k
            return peor

    valor_max = dp(0, n-1, HERMANA)
    return valor_max, eleccion_prof, eleccion_hermana


# ---------------------------------------------------
# FUNCIÓN PRINCIPAL HASH
# ---------------------------------------------------

def satisfaccion_maxima_hash(torta: List[int]) -> Tuple[int, List[Tuple[int,int,int]]]:
    """
    Igual que satisfaccion_maxima, pero usando memoización hash.
    """
    assert len(torta) % 2 == 0 and len(torta) >= 2
    m = len(torta)
    n = m // 2

    mejor_total = -10**18
    mejor_inicio = 0
    mejor_eleccion_seq = []

    for start in range(m):
        primera_ganancia = suma_bloque_circular(torta, start, n)
        residual = bloque_residual(torta, start, n)

        valor_max, eleccion_prof, eleccion_hermana = valor_residual_hash(residual)
        total = primera_ganancia + valor_max

        if total > mejor_total:
            mejor_total = total
            mejor_inicio = start

            # Reconstrucción
            seq = []
            i, j = 0, n-1
            turno = HERMANA

            while i <= j:
                if turno == PROFESOR:
                    k = eleccion_prof.get((i,j), 0)
                    if k == 0: break
                    seq.append((PROFESOR, i, k))
                    i += k
                else:
                    k = eleccion_hermana.get((i,j), 0)
                    if k == 0: break
                    seq.append((HERMANA, i, k))
                    i += k

                turno = 1 - turno

            mejor_eleccion_seq = [(PROFESOR, start, n)] + seq

    # Conversión a índices globales
    secuencia_global = []
    for t, idx, k in mejor_eleccion_seq:
        if t == PROFESOR and idx == 0:
            secuencia_global.append((t, mejor_inicio % m, k))
        else:
            inicio_global = (mejor_inicio + n + idx) % m
            secuencia_global.append((t, inicio_global, k))

    return mejor_total, secuencia_global


# ---------------------------------------------------
# EJEMPLO DE USO
# ---------------------------------------------------
if __name__ == "__main__":
    random.seed(42)
    n = 3
    torta = [random.randint(-5, 10) for _ in range(2*n)]
    print("Valores de satisfacción de la torta:", torta)

    start = time.perf_counter()
    valor, sec = satisfaccion_maxima_hash(torta)
    end = time.perf_counter()

    print("Satisfacción máxima del profesor:", valor)
    print("Secuencia de jugadas (turno, inicio_global, k):")

    for t, idx, k in sec:
        turno_str = "Profesor" if t == PROFESOR else "Hermana"
        print(f"{turno_str} toma desde {idx} k={k}")

    print(f"Tiempo de ejecución (HASH): {end - start:.6f} s")
