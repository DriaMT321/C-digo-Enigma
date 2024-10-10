# Simulación de la Máquina Enigma

import string

# Definición de los rotores y reflectores originales
ROTORES = {
    'I':    {'wiring': 'EKMFLGDQVZNTOWYHXUSPAIBRCJ', 'notch': 'Q'},
    'II':   {'wiring': 'AJDKSIRUXBLHWTMCQGZNPYFVOE', 'notch': 'E'},
    'III':  {'wiring': 'BDFHJLCPRTXVZNYEIWGAKMUSQO', 'notch': 'V'},
    'IV':   {'wiring': 'ESOVPZJAYQUIRHXLNFTGKDCMWB', 'notch': 'J'},
    'V':    {'wiring': 'VZBRGITYUPSDNHLXAWMJQOFECK', 'notch': 'Z'},
}

REFLECTORES = {
    'B': 'YRUHQSLDPXNGOKMIEBFZCWVJAT',
    'C': 'FVPJIAOYEDRZXWGCTKUQSBNMHL',
}

# Función para crear el mapeo de un rotor o reflector
def crear_mapeo(cableado):
    letras = string.ascii_uppercase
    return dict(zip(letras, cableado))

# Clase que representa un rotor de la máquina Enigma
class Rotor:
    def __init__(self, nombre, posicion_inicial, anillo):
        self.nombre = nombre
        self.posicion = string.ascii_uppercase.index(posicion_inicial)
        self.anillo = int(anillo) - 1
        self.cableado = ROTORES[nombre]['wiring']
        self.notch = ROTORES[nombre]['notch']
        self.mapeo_adelante = crear_mapeo(self.cableado)
        self.mapeo_atras = {v: k for k, v in self.mapeo_adelante.items()}

    # Avanza el rotor y devuelve True si alcanza la muesca
    def step(self):
        self.posicion = (self.posicion + 1) % 26
        letra_actual = string.ascii_uppercase[self.posicion]
        return letra_actual == self.notch

    # Transforma una letra pasando por el rotor
    def forward(self, c):
        idx = (string.ascii_uppercase.index(c) + self.posicion - self.anillo) % 26
        letra = self.mapeo_adelante[string.ascii_uppercase[idx]]
        idx = (string.ascii_uppercase.index(letra) - self.posicion + self.anillo) % 26
        return string.ascii_uppercase[idx]

    # Transforma una letra pasando por el rotor en sentido inverso
    def backward(self, c):
        idx = (string.ascii_uppercase.index(c) + self.posicion - self.anillo) % 26
        letra = self.mapeo_atras[string.ascii_uppercase[idx]]
        idx = (string.ascii_uppercase.index(letra) - self.posicion + self.anillo) % 26
        return string.ascii_uppercase[idx]

# Clase principal de la máquina Enigma
class Enigma:
    def __init__(self, rotores, posiciones_iniciales, anillos, reflector, plugboard):
        self.rotores = [Rotor(rotor, pos, anillo) for rotor, pos, anillo in zip(rotores, posiciones_iniciales, anillos)]
        self.reflector = crear_mapeo(REFLECTORES[reflector])
        self.plugboard = self.crear_plugboard(plugboard)

    # Crea el mapeo del plugboard
    def crear_plugboard(self, configuracion):
        mapeo = {c: c for c in string.ascii_uppercase}
        pares = configuracion.upper().split()
        for par in pares:
            if len(par) == 2:
                a, b = par[0], par[1]
                mapeo[a], mapeo[b] = b, a
        return mapeo

    # Procesa una letra a través de la máquina Enigma
    def procesar_letra(self, c):
        if c not in string.ascii_uppercase:
            return c

        # Avance de los rotores (considerando el mecanismo de doble paso)
        rotar_siguiente = self.rotores[-1].step()
        for i in range(len(self.rotores) - 2, -1, -1):
            if rotar_siguiente:
                rotar_siguiente = self.rotores[i].step()
            else:
                break

        # Paso por el plugboard
        c = self.plugboard[c]

        # Paso adelante por los rotores
        for rotor in reversed(self.rotores):
            c = rotor.forward(c)

        # Reflexión
        c = self.reflector[c]

        # Paso atrás por los rotores
        for rotor in self.rotores:
            c = rotor.backward(c)

        # Paso final por el plugboard
        c = self.plugboard[c]

        return c

    # Procesa un mensaje completo
    def procesar_mensaje(self, mensaje):
        mensaje = mensaje.upper()
        resultado = ''
        for c in mensaje:
            resultado += self.procesar_letra(c)
        return resultado

# Solicitud de configuraciones al usuario
def configurar_enigma():
    print("Bienvenido a la simulación de la Máquina Enigma\n")

    # Selección de rotores
    print("Seleccione los tres rotores (ejemplo: I II III):")
    rotores_seleccionados = input().strip().split()
    while len(rotores_seleccionados) != 3 or not all(r in ROTORES for r in rotores_seleccionados):
        print("Entrada inválida. Por favor, seleccione tres rotores válidos:")
        rotores_seleccionados = input().strip().split()

    # Posiciones iniciales de los rotores
    print("Ingrese las posiciones iniciales de los rotores (ejemplo: A B C):")
    posiciones_iniciales = input().strip().split()
    while len(posiciones_iniciales) != 3 or not all(p in string.ascii_uppercase for p in posiciones_iniciales):
        print("Entrada inválida. Por favor, ingrese tres letras de A a Z:")
        posiciones_iniciales = input().strip().split()

    # Ajustes de anillo
    print("Ingrese los ajustes de anillo (1-26 para cada rotor, ejemplo: 1 1 1):")
    anillos = input().strip().split()
    while len(anillos) != 3 or not all(a.isdigit() and 1 <= int(a) <= 26 for a in anillos):
        print("Entrada inválida. Por favor, ingrese tres números entre 1 y 26:")
        anillos = input().strip().split()

    # Selección de reflector
    print("Seleccione el reflector (B o C):")
    reflector = input().strip().upper()
    while reflector not in REFLECTORES:
        print("Entrada inválida. Por favor, seleccione B o C:")
        reflector = input().strip().upper()

    # Configuración del plugboard
    print("Ingrese las conexiones del plugboard (pares de letras, ejemplo: AB CD EF):")
    plugboard = input().strip().upper()

    # Creación de la máquina Enigma con las configuraciones
    enigma = Enigma(rotores_seleccionados, posiciones_iniciales, anillos, reflector, plugboard)

    return enigma

def main():
    enigma = configurar_enigma()
    print("\nIngrese el mensaje a procesar:")
    mensaje = input().strip()
    resultado = enigma.procesar_mensaje(mensaje)
    print("\nEl mensaje procesado es:")
    print(resultado)

if __name__ == "__main__":
    main()
