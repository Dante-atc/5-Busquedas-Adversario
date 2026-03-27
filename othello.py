"""
Othello

El estado se representa como una tupla de 64 elementos, indexados como:

 0  1  2  3  4  5  6  7
 8  9 10 11 12 13 14 15
16 17 18 19 20 21 22 23
24 25 26 27 28 29 30 31
32 33 34 35 36 37 38 39
40 41 42 43 44 45 46 47
48 49 50 51 52 53 54 55
56 57 58 59 60 61 62 63

Cada elemento puede ser 0 (vacío), 1 (jugador 1) o -1 (jugador 2).
Las acciones son índices de 0 a 63, o None si el jugador no tiene jugadas legales.
La ganancia es 1 si gana jugador 1, -1 si gana jugador 2, 0 si empate.
"""

import juegos_simplificado as js
import minimax

# Las 8 direcciones posibles en el tablero (fila, columna)
_DIRS = [(-1,-1), (-1, 0), (-1, 1),
         ( 0,-1),          ( 0, 1),
         ( 1,-1), ( 1, 0), ( 1, 1)]


def _voltea(s, a, j):
    """
    Devuelve la lista de índices a voltear si jugador j pone ficha en celda a.
    Regresa lista vacía si la jugada no voltea nada (jugada ilegal).
    """
    fila, col = divmod(a, 8)
    a_voltear = []
    for df, dc in _DIRS:
        f, c = fila + df, col + dc
        candidatos = []
        while 0 <= f < 8 and 0 <= c < 8 and s[f * 8 + c] == -j:
            candidatos.append(f * 8 + c)
            f += df
            c += dc
        if candidatos and 0 <= f < 8 and 0 <= c < 8 and s[f * 8 + c] == j:
            a_voltear.extend(candidatos)
    return a_voltear


class Othello(js.JuegoZT2):

    def inicializa(self):
        """Estado inicial con las 4 fichas centrales."""
        s = [0] * 64
        s[27], s[36] = -1, -1
        s[28], s[35] =  1,  1
        return tuple(s)

    def jugadas_legales(self, s, j):
        """
        Devuelve lista de celdas vacías donde j voltea al menos una ficha rival.
        Si no hay ninguna, devuelve [None] para indicar pase de turno.
        """
        jugadas = [a for a in range(64) if s[a] == 0 and _voltea(s, a, j)]
        return jugadas if jugadas else [None]

    def sucesor(self, s, a, j):
        """
        Coloca ficha de j en a y voltea todas las fichas rivales atrapadas.
        Si a es None (pase de turno) devuelve s sin cambios.
        """
        if a is None:
            return s
        s = list(s)
        s[a] = j
        for idx in _voltea(s, a, j):
            s[idx] = j
        return tuple(s)

    def terminal(self, s):
        """Terminal si el tablero está lleno o ambos jugadores deben pasar."""
        if 0 not in s:
            return True
        return (
            self.jugadas_legales(s,  1) == [None] and
            self.jugadas_legales(s, -1) == [None]
        )

    def ganancia(self, s):
        """1 si gana jugador 1, -1 si gana jugador 2, 0 si empate."""
        diff = sum(s)
        return 0 if diff == 0 else (1 if diff > 0 else -1)
    
    
    
# Función de ordenamiento


_ESQUINAS  = {0, 7, 56, 63}
_PELIGROSAS = {1, 6, 8, 9, 14, 15, 48, 49, 54, 55, 57, 62}
_BORDES = {
    i for i in range(64)
    if i // 8 == 0 or i // 8 == 7 or i % 8 == 0 or i % 8 == 7
} - _ESQUINAS - _PELIGROSAS
 
# Checa estado actual para contar volteos
_estado_actual_othello = [None]
 
_sucesor_original_othello = Othello.sucesor
 
def _sucesor_con_estado_othello(self, s, a, j):
    _estado_actual_othello[0] = s
    return _sucesor_original_othello(self, s, a, j)
 
Othello.sucesor = _sucesor_con_estado_othello
 
 
def ordena_othello(jugadas, jugador):
    """
    Ordena jugadas priorizando:
      1. Esquinas  — nunca se voltean, máximo valor estratégico
      2. Bordes    — estables una vez ocupados
      3. Centro    — desempate por cuántas fichas voltea (más es mejor)
      4. Peligrosas — adyacentes a esquinas vacías, van al fondo
    """
    s = _estado_actual_othello[0]
 
    def prioridad(a):
        if a in _ESQUINAS:
            return (0, 0)
        if a in _BORDES:
            return (1, 0)
        if a in _PELIGROSAS:
            # Si la esquina adyacente ya está ocupada, la celda peligrosa deja de serlo
            esquina_adyacente = {
                1: 0, 8: 0, 9: 0,
                6: 7, 14: 7, 15: 7,
                48: 56, 49: 56, 57: 56,
                54: 63, 55: 63, 62: 63
            }.get(a)
            if esquina_adyacente is not None and s is not None and s[esquina_adyacente] == jugador:
                volteos = len(_voltea(s, a, jugador)) if s else 0
                return (2, -volteos)
            return (3, 0)
        volteos = len(_voltea(s, a, jugador)) if s else 0
        return (2, -volteos)
 
    return sorted(jugadas, key=prioridad)



# Interfaz CLI

class InterfaceOthello(js.JuegoInterface):
 
    def muestra_estado(self, s):
        x = sum(1 for c in s if c ==  1)
        o = sum(1 for c in s if c == -1)
        print(f"\n  X: {x}   O: {o}")
        print("  " + " ".join(str(c) for c in range(8)))
        print("  " + "--" * 8)
        for fila in range(8):
            fila_str = []
            for col in range(8):
                c = s[fila * 8 + col]
                fila_str.append(' X' if c == 1 else ' O' if c == -1 else ' .')
            print(f"{fila}|{''.join(fila_str)}")
        print()
 
    def muestra_ganador(self, g):
        if g == 1:
            print("Gana el jugador X")
        elif g == -1:
            print("Gana el jugador O")
        else:
            print("Empate")
 
    def jugador_humano(self, s, j):
        print(f"Jugador {'X' if j == 1 else 'O'}")
        jugadas = list(self.juego.jugadas_legales(s, j))
        print("Jugadas legales:", jugadas)
        jugada = None
        while jugada not in jugadas:
            try:
                jugada = int(input("Jugada: "))
            except ValueError:
                pass
        return jugada
    
    
    
# Script principal

if __name__ == '__main__':
 
    cfg = {
        "Jugador 1": "Humano",      # "Humano", "Aleatorio", "Negamax", "Tiempo"
        "Jugador 2": "Aleatorio",   # "Humano", "Aleatorio", "Negamax", "Tiempo"
        "profundidad máxima": 5,
        "tiempo": 10,
        "ordena": ordena_othello,
        "evalua": None              # se agrega en la parte 3
    }
 
    def jugador_cfg(cadena):
        if cadena == "Humano":
            return "Humano"
        elif cadena == "Aleatorio":
            return js.JugadorAleatorio()
        elif cadena == "Negamax":
            return minimax.JugadorNegamax(
                ordena=cfg["ordena"], d=cfg["profundidad máxima"], evalua=cfg["evalua"]
            )
        elif cadena == "Tiempo":
            return minimax.JugadorNegamaxIterativo(
                tiempo=cfg["tiempo"], ordena=cfg["ordena"], evalua=cfg["evalua"]
            )
        else:
            raise ValueError("Jugador no reconocido")
 
    interfaz = InterfaceOthello(
        Othello(),
        jugador1=jugador_cfg(cfg["Jugador 1"]),
        jugador2=jugador_cfg(cfg["Jugador 2"])
    )
 
    print("Othello")
    print("Jugador 1 (X):", cfg["Jugador 1"])
    print("Jugador 2 (O):", cfg["Jugador 2"])
    print()
 
    interfaz.juega()