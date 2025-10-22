import random

# Selecciona una palabra aleatoria que no se haya usado antes
def palabra_aleatoria(palabras, usadas):

    if len(usadas) == len(palabras):  # Si ya se usaron todas las palabras
        return 0  

    palabra = random.choice(palabras)

    while palabra in usadas:  # Elegir otra si ya fue usada
        palabra = random.choice(palabras)

    return palabra.lower()  # Convertir a minúsculas


# Lógica principal del juego Wordle
def wordle(palabra):
    print("_ "*len(palabra), f'({len(palabra)})')
    intentos = 0
    letras_palabra = list(palabra)
    pistas = [""] * len(palabra)
    discarded = []
    colors = {'green':'\033[42m','yellow':'\033[43m','red':'\033[41m','reset':'\033[0m'}

    while True:
        intentos += 1
        intento = input("Escribe una palabra: ").lower()

        if not intento or len(intento) != len(palabra):
            print("Por favor, escribe una palabra válida: ")
            continue


        # Primer Intento: letras correctas en posición correcta
        for i in range(len(palabra)):
            if i < len(intento) and intento[i] == palabra[i]:
                pistas[i] = f"{colors['green']}{intento[i].capitalize()}{colors['reset']}"
                letras_palabra[i] = 0  # Marcar como usada para palabras con letras repetidas
            elif i<len(intento) and intento[i] in palabra:
                pistas[i] = f"{colors['yellow']}{intento[i].capitalize()}{colors['reset']}"
            else:
                pistas[i] = f"{colors['red']}{intento[i].capitalize()}{colors['reset']}"
                if intento[i] not in discarded:
                    discarded.append(intento[i])
                    discarded.sort()

        if intento == palabra:
            return "".join(pistas), intentos
        else:
            print("".join(pistas), 'Letras descartadas:', ", ".join(discarded))


# Función principal del juego
def main():
    lista_dificultad = [
        ['gato', 'perro', 'sol', 'llave', 'rata'],
        ['manzana', 'uva', 'mango', 'camino', 'piedra'],
        ['imagen', 'pais', 'balance', 'diamante', 'realidad']
    ]
    
    palabras = []
    usadas = []

    while True:
        inicio = input("¿Quieres jugar Wordle? (si/no): ").lower()

        if inicio == "no":
            print("¡Muchas gracias por jugar! 😊")
            break
        elif inicio == "si":
            dificultad = input("Elige una dificultad (facil, medio, dificil): ").lower()

            if dificultad == "facil":
                palabras = lista_dificultad[0]
            elif dificultad == "medio":
                palabras = lista_dificultad[1]
            elif dificultad == "dificil":
                palabras = lista_dificultad[2]
            else:
                print("Por favor, elige una dificultad válida: ")
                continue

            palabra = palabra_aleatoria(palabras, usadas)
            usadas.append(palabra)

            if palabra == 0:
                print("¡Has descubierto todas las palabras en esta dificultad! 🎉")
                continue

            resultado, intentos = wordle(palabra)
            print(resultado)
            print(f"¡Correcto! ¡Encontraste la palabra en {intentos} intentos!")

        else:
            print("Por favor responde con 'si' o 'no'.")
            continue

# Ejecutar el juego
main()
