# SRTBOT (Estado, Recurrencia, Transiciones, Base, Orden, Total)

## Problema
Torta circular con 2n porciones con satisfacciones enteras `s[0..2n-1]`. Dos jugadores alternan.  
El profesor (PROF) empieza y desea maximizar su satisfacción total.

## Reducción clave
- **Primer movimiento**: el profesor come exactamente n porciones contiguas (un semicirculo).  
- **Juego residual**: bloque lineal de n porciones. Cada jugador en su turno puede comer un prefijo de longitud `k` con `1 ≤ k ≤ m-1` (si `m > 1`).  
  Si queda una sola porción (`m = 1`), quien juega se la come.

## Estado (S)
Sub-arreglo lineal `A[0..m-1]` con `m ≤ n`.  
`F(i, j, turno)` = ganancia total que obtendrá el profesor desde `A[i..j]`, dado que `turno ∈ {PROF, OPP}`.

## Recurrencia (R)
Sea `sum(i, t)` la suma de `A[i..t]` (usando prefijos `PS[t+1] − PS[i]` para O(1)).

- **Caso m = 1 (j-i+1 = 1)**:
  - `F(i,i,PROF) = A[i]`
  - `F(i,i,OPP) = 0`
- **Caso m ≥ 2 (prefijos 1 ≤ k ≤ m-1)**:
  - `F(i,j,PROF) = max_{k=1..m-1} ( sum(i,i+k-1) + F(i+k,j,OPP) )`
  - `F(i,j,OPP) = min_{k=1..m-1} ( F(i+k,j,PROF) )`

## Transiciones (T)
Avanzar el índice izquierdo `i` a `i+k` y alternar el turno.

## Base (B)
- `m = 1`: PROF toma la porción `A[i]`, OPP aporta `0`.

## Orden (O)
- Implementación top-down con memoización (tablas o hash).  
- Para el problema completo:
  1. Para cada `t ∈ {0..2n-1}`, PROF escoge semicirculo `B_t = s[t..t+n-1] (mod 2n)`. Ganancia inicial `S_B = sum(B_t)`.
  2. Bloque residual lineal `A_t = s[t+n .. t-1] (mod 2n)` de longitud n.
  3. Ganancia adicional del profesor: `F_t = F(0, n-1, OPP)` (porque tras la primera jugada, le toca a OPP).
  4. Respuesta final: `max_t (S_B + F_t)`.

## Total (T)
- Estados del sub-juego lineal: `O(n^2)` por turno.
- Cada estado prueba `O(n)` opciones de `k` → `O(n^3)` por bloque residual.
- Considerando los `2n` semicirculos iniciales: `O(n^4)` total.
- Con técnicas de reuso de prefijos circulares, se puede reducir a `O(n^3)` total.

## Memoización
- Tablas (listas de listas) indexadas por `(i,j,turno)`.
- Tablas de hash (diccionarios) con llave `(i,j,turno)`.
