"""
Juego de conecta 4

El estado se va a representar como una lista de 42 elementos, tal que


0  1  2  3  4  5  6
7  8  9 10 11 12 13
14 15 16 17 18 19 20
21 22 23 24 25 26 27
28 29 30 31 32 33 34
35 36 37 38 39 40 41

y cada elemento puede ser 0, 1 o -1, donde 0 es vacío, 1 es una ficha del
jugador 1 y -1 es una ficha del jugador 2.

Las acciones son poner una ficha en una columna, que se representa como un
número de 0 a 6.

Un estado terminal es aquel en el que un jugador ha conectado 4 fichas
horizontales, verticales o diagonales, o ya no hay espacios para colocar
fichas.

La ganancia es 1 si gana el jugador 1, -1 si gana el jugador 2 y 0 si es un
empate.

"""

import juegos_simplificado as js
import minimax

class Conecta4(js.JuegoZT2):
    def inicializa(self):
        return tuple([0 for _ in range(6 * 7)])
        
    def jugadas_legales(self, s, j):
        return (columna for columna in range(7) if s[columna] == 0)
    
    def sucesor(self, s, a, j):
        s = list(s[:])
        for i in range(5, -1, -1):
            if s[a + 7 * i] == 0:
                s[a + 7 * i] = j
                break
        return tuple(s)
    
    def ganancia(self, s):
        #Verticales
        for i in range(7):
            for j in range(3):
                if (s[i + 7 * j] == s[i + 7 * (j + 1)] == s[i + 7 * (j + 2)] == s[i + 7 * (j + 3)] != 0):
                    return s[i + 7 * j]
        #Horizontales
        for i in range(6):
            for j in range(4):
                if (s[7 * i + j] == s[7 * i + j + 1] == s[7 * i + j + 2] == s[7 * i + j + 3] != 0):
                    return s[7 * i + j]
        #Diagonales
        for i in range(4):
            for j in range(3):
                if (s[i + 7 * j] == s[i + 7 * j + 8] == s[i + 7 * j + 16] == s[i + 7 * j + 24] != 0):
                    return s[i + 7 * j]
                if (s[i + 7 * j + 3] == s[i + 7 * j + 9] == s[i + 7 * j + 15] == s[i + 7 * j + 21] != 0):
                    return s[i + 7 * j + 3]
        return 0
    
    def terminal(self, s):
        if 0 not in s:
            return True
        return self.ganancia(s) != 0
    
class InterfaceConecta4(js.JuegoInterface):
    def muestra_estado(self, s):
        """
        Muestra el estado del juego, se puede usar la función pprint_conecta4
        para mostrar el estado de forma más amigable

        """
        a = [' X ' if x == 1 else ' O ' if x == -1 else '   ' for x in s]
        print('\n 0 | 1 | 2 | 3 | 4 | 5 | 6')
        for i in range(6):
            print('|'.join(a[7 * i:7 * (i + 1)]))
            print('---+---+---+---+---+---+---\n')
    
    def muestra_ganador(self, g):
        """
        Muestra el ganador del juego, se puede usar " XO"[g] para mostrar el
        ganador de forma más amigable

        """
        if g != 0:
            print("Gana el jugador " + " XO"[g])
        else:
            print("Un asqueroso empate")

    def jugador_humano(self, s, j):
        print("Jugador", " XO"[j])
        jugadas = list(self.juego.jugadas_legales(s, j))
        print("Jugadas legales:", jugadas)
        jugada = None
        while jugada not in jugadas:
            jugada = int(input("Jugada: "))
        return jugada

def ordena_centro(jugadas, jugador):
    """
    Ordena las jugadas de acuerdo a la distancia al centro
    """
    return sorted(jugadas, key=lambda x: abs(x - 4))

def evalua_3con(s):
    """
    Evalua el estado s para el jugador 1
    """
    conect3 = sum(
        1 for i in range(7) for j in range(4) 
        if (s[i + 7 * j] == s[i + 7 * (j + 1)] 
            == s[i + 7 * (j + 2)] == 1)
    ) - sum(
        1 for i in range(7) for j in range(4) 
        if (s[i + 7 * j] == s[i + 7 * (j + 1)] 
            == s[i + 7 * (j + 2)] == -1)
    ) + sum(
        1 for i in range(6) for j in range(5) 
        if (s[7 * i + j] == s[7 * i + j + 1] 
            == s[7 * i + j + 2] == 1)
    ) - sum(
        1 for i in range(6) for j in range(5) 
        if (s[7 * i + j] == s[7 * i + j + 1] 
            == s[7 * i + j + 2] == -1)
    ) + sum(
        1 for i in range(5) for j in range(4) 
        if (s[i + 7 * j] == s[i + 7 * j + 8] 
            == s[i + 7 * j + 16] == 1)
    ) - sum(
        1 for i in range(5) for j in range(4) 
        if (s[i + 7 * j] == s[i + 7 * j + 8] 
            == s[i + 7 * j + 16] == -1)
    ) + sum(
        1 for i in range(5) for j in range(4) 
        if (s[i + 7 * j + 3] == s[i + 7 * j + 9] 
            == s[i + 7 * j + 15] == 1)
    ) - sum(
        1 for i in range(5) for j in range(4) 
        if (s[i + 7 * j + 3] == s[i + 7 * j + 9] 
            == s[i + 7 * j + 15] == -1)
    )
    promedio = conect3 / (7 * 4 + 6 * 5 + 5 * 4 + 5 * 4)
    if abs(promedio) >= 1:
        raise ValueError("Evaluación fuera de rango --> ", promedio)
    return promedio

# Heurísticas mejoradas

# Todas las ventanas de 4 celdas contiguas posibles en el tablero,
def _genera_ventanas():
    ventanas = []
    for col in range(7):          # verticales
        for fila in range(3):
            ventanas.append([col + 7 * (fila + k) for k in range(4)])
    for fila in range(6):         # horizontales
        for col in range(4):
            ventanas.append([7 * fila + col + k for k in range(4)])
    for fila in range(3):         # diagonal bajando-derecha
        for col in range(4):
            ventanas.append([col + 7 * fila + k * 8 for k in range(4)])
    for fila in range(3):         # diagonal bajando-izquierda
        for col in range(3, 7):
            ventanas.append([col + 7 * fila + k * 6 for k in range(4)])
    return ventanas

_VENTANAS  = _genera_ventanas()
_PESOS     = {3: 5, 2: 2, 1: 0}   # puntos por ventana según fichas propias
_CENTRO    = {0: 0, 1: 1, 2: 2, 3: 3, 4: 2, 5: 1, 6: 0}  # bonus por columna
_MAX_SCORE = 2000                  # normalizador empírico


def _celda_libre(col, s):
    """Índice de la celda donde caería una ficha en la columna col."""
    for fila in range(5, -1, -1):
        if s[col + 7 * fila] == 0:
            return col + 7 * fila
    return -1


def _gana_en(col, jugador, s):
    """True si poner una ficha de jugador en col completa un cuatro en raya."""
    idx = _celda_libre(col, s)
    if idx == -1:
        return False
    s2 = list(s); s2[idx] = jugador; s2 = tuple(s2)
    return any(all(s2[i] == jugador for i in v) for v in _VENTANAS)


# Variable global para pasar el estado a ordena_centro_m
_estado_actual = [tuple([0] * 42)]

_sucesor_original = Conecta4.sucesor

def _sucesor_con_estado(self, s, a, j):
    _estado_actual[0] = s
    return _sucesor_original(self, s, a, j)

Conecta4.sucesor = _sucesor_con_estado


def ordena_centro_m(jugadas, jugador):
    """
    Ordena las jugadas priorizando:
      1. Jugadas que ganan el juego inmediatamente
      2. Jugadas que bloquean una victoria inmediata del rival
      3. Distancia al centro como desempate (corrige el bug de ordena_centro)
    """
    jugadas = list(jugadas)
    s = _estado_actual[0]

    ganadoras = [c for c in jugadas if _gana_en(c,  jugador, s)]
    if ganadoras:
        return ganadoras + [c for c in jugadas if c not in ganadoras]

    bloqueos = [c for c in jugadas if _gana_en(c, -jugador, s)]
    resto    = [c for c in jugadas if c not in bloqueos]

    return (
        sorted(bloqueos, key=lambda c: -_CENTRO[c]) +
        sorted(resto,    key=lambda c: -_CENTRO[c])
    )


def _puntua_ventana(ventana, s, jugador):
    """
    Puntúa una ventana de 4 celdas para jugador.
    Devuelve 0 si la ventana está bloqueada (tiene fichas de ambos jugadores).
    """
    propias = sum(1 for i in ventana if s[i] == jugador)
    rivales = sum(1 for i in ventana if s[i] == -jugador)
    if propias > 0 and rivales > 0:
        return 0
    if rivales > 0:
        return 0
    return _PESOS.get(propias, 0)


def evalua_posicion(s):
    """
    Evalúa el estado s para el jugador 1 considerando:
      - Todas las ventanas de 4 celdas con pesos por cantidad de fichas propias
      - Bonus por control de columnas centrales
    Devuelve un valor en (-1, 1).
    """
    score = sum(
        _puntua_ventana(v, s,  1) - _puntua_ventana(v, s, -1)
        for v in _VENTANAS
    )
    score += sum(
        _CENTRO[col] * (
            sum(1 for fila in range(6) if s[col + 7 * fila] ==  1) -
            sum(1 for fila in range(6) if s[col + 7 * fila] == -1)
        )
        for col in range(7)
    )
    return max(-0.99, min(0.99, score / _MAX_SCORE))


if __name__ == '__main__':

    cfg = {
    "Jugador 1": "Humano",      #Puede ser "Humano", "Aleatorio", "Negamax", "Tiempo"
    "Jugador 2": "Negamax",     #Puede ser "Humano", "Aleatorio", "Negamax", "Tiempo"
    "profundidad máxima": 6,
    "tiempo": 10,
    "ordena": ordena_centro_m,  
    "evalua": evalua_posicion    
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

    interfaz = InterfaceConecta4(
        Conecta4(),
        jugador1=jugador_cfg(cfg["Jugador 1"]),
        jugador2=jugador_cfg(cfg["Jugador 2"])
    )

    print("El Juego del Conecta 4 ")
    print("Jugador 1:", cfg["Jugador 1"])
    print("Jugador 2:", cfg["Jugador 2"])
    print()

    interfaz.juega()