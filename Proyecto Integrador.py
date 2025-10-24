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
    available = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
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
                    available.remove(intento[i])

        if intento == palabra:
            return "".join(pistas), intentos
        else:
            print("".join(pistas),
                  '\nLetras descartadas:',
                  ", ".join(discarded),
                  "\nLetras disponibles:",
                  ', '.join(available))


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

            resultado, intentos = wordle(palabra)
            print(resultado)
            print(f"¡Correcto! ¡Encontraste la palabra en {intentos} intentos!")
            if palabra_aleatoria(palabras, usadas[category]) == 0:
                print("¡Has descubierto todas las palabras en esta dificultad! 🎉")
                usadas[category].clear()
                continue

            usadas[category].append(palabra)
            with open('used.txt','w') as file:
                for lista in usadas:
                    file.write(' '.join(lista)+'\n')
        else:
            print("Por favor responde con 'si' o 'no'.")
            continue
    return usadas
# Ejecutar el juego
main()
with open('used.txt') as file:
    print([line.strip() for line in file.readlines()])