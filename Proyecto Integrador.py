import random
import os

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
    tablero = [['_' for i in range(len(palabra))] for i in range(len(palabra))]
    intentos = 0
    letras_palabra = list(palabra)
    discarded = []
    available = list('abcdefghijklmnopqrstuvwxyz')
    colors = {'green':'\033[42m','yellow':'\033[43m','red':'\033[41m','reset':'\033[0m'}

    while intentos<len(palabra):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f'Intentos restantes: {len(palabra)-intentos}')
        print(f'{colors["red"]}{", ".join(discarded).upper()}{colors["reset"]}')
        for fila in tablero:
            print('|'.join(fila))
        intento = input("").lower()

        if not intento or len(intento) != len(palabra):
            continue

        # Primer Intento: letras correctas en posición correcta
        pistas=[]
        for i,letra in enumerate(intento):
            if letra == palabra[i]:
                pistas.append(f"{colors['green']}{letra.capitalize()}{colors['reset']}")
                letras_palabra[i] = 0  # Marcar como usada para palabras con letras repetidas
            elif letra in palabra:
                pistas.append(f"{colors['yellow']}{letra.capitalize()}{colors['reset']}")
            else:
                pistas.append(f"{colors['red']}{letra.capitalize()}{colors['reset']}")
                if letra not in discarded:
                    discarded.append(letra)
                    discarded.sort()
                    available.remove(letra)
            tablero[intentos] = list(pistas)
        if intento == palabra:
            return tablero, intentos
        intentos += 1
        if intentos == len(palabra) and intento != palabra:
            intentos += 1
    os.system('cls' if os.name == 'nt' else 'clear')
    return tablero, intentos

# Función principal del juego
def main():
    file = open('words.txt','r')
    easy_list = file.readline().split()
    medium_list = file.readline().split()
    hard_list = file.readline().split()
    file.close()

    file = open('used.txt','r')
    usadas = [file.readline().split() for i in range(3)]

    # INSTRUCCION: Haz el archivo words.txt 

    while True:
        inicio = input("¿Quieres jugar Wordle? (si/no): ").lower()

        if inicio == "no":
            print("¡Muchas gracias por jugar! 😊")
            break
        elif inicio == "si":
            dificultad = input("Elige una dificultad (facil, medio, dificil): ").lower()

            if dificultad == "facil":
                palabras = easy_list
                category = 0
            elif dificultad == "medio":
                palabras = medium_list
                category = 1
            elif dificultad == "dificil":
                palabras = hard_list
                category = 2
            else:
                print("Por favor, elige una dificultad válida: ")
                continue

            palabra = palabra_aleatoria(palabras, usadas[category])

            if palabra == 0:
                print("¡Has descubierto todas las palabras en esta dificultad! 🎉")
                continue

            tablero, intentos = wordle(palabra)
            for fila in tablero:
                print('|'.join(fila),)
            if intentos <= len(palabra):
                print(f'Encontraste la palabra en {intentos} intentos! 🎉')
            else:
                print(f'La palabra era {palabra}, suerte a la próxima')
            if palabra_aleatoria(palabras, usadas[category]) == 0:
                print("¡Has descubierto todas las palabras en esta dificultad! 🎉")
                continue

            usadas[category].append(palabra)
            with open('used.txt','w') as file:
                for lista in usadas:
                    file.write(' '.join(lista)+'\n')
        else:
            print("Por favor responde con 'si' o 'no'.")
            continue
# Ejecutar el juego
main()