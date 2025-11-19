import time
import random
import matplotlib.pyplot as plt

# Importar ambas versiones
from arreglos_cumple import satisfaccion_maxima        # versión arreglos
from tablas_hash_cumple import satisfaccion_maxima_hash  # versión diccionarios


# ------------------------------------------------------------
# FUNCION DE BENCHMARK
# ------------------------------------------------------------

def medir_tiempo(func, torta):
    """Mide el tiempo de ejecución de func(torta)."""
    inicio = time.perf_counter()
    _ = func(torta)
    fin = time.perf_counter()
    return fin - inicio


def generar_torta(n):
    """Genera una torta aleatoria de 2n porciones."""
    return [random.randint(-10, 20) for _ in range(2*n)]


# ------------------------------------------------------------
# EXPERIMENTO PRINCIPAL
# ------------------------------------------------------------

def benchmark():
    random.seed(42)

    # Valores de n para experimentar
    ns = [10, 20, 30, 40, 50]   # Puedes agregar más: 60, 70, etc.
    tiempos_array = []
    tiempos_hash = []

    for n in ns:
        print(f"\nProbando n = {n}  (torta de {2*n} porciones)...")

        torta = generar_torta(n)

        # Tiempo versión arreglo
        t_array = medir_tiempo(satisfaccion_maxima, torta)
        tiempos_array.append(t_array)

        # Tiempo versión hash
        t_hash = medir_tiempo(satisfaccion_maxima_hash, torta)
        tiempos_hash.append(t_hash)

        print(f"  Arreglos: {t_array:.6f} s")
        print(f"  Hash:     {t_hash:.6f} s")


    # ------------------------------------------------------------
    # GRAFICAR RESULTADOS
    # ------------------------------------------------------------

    plt.figure(figsize=(9,5))
    plt.plot(ns, tiempos_array, marker='o', label="Arreglos")
    plt.plot(ns, tiempos_hash, marker='o', label="Hash")
    plt.xlabel("Valor de n (torta con 2n porciones)")
    plt.ylabel("Tiempo de ejecución (segundos)")
    plt.title("Comparación de tiempos: Arreglos vs Tablas Hash")
    plt.grid(True)
    plt.legend()
    plt.savefig("tiempos.png", dpi=200)
    plt.close()

    print("\nGráfico guardado como tiempos.png")


if __name__ == "__main__":
    benchmark()
