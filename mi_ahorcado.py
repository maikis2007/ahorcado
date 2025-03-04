from random import choices, choice
from palabras import *
from ahorcado_diagramas import vidas_diccionario_visual

def seleccionar_palabra(palabras_faciles, palabras_intermedias, palabras_dificiles):
    """
    Selecciona una categoría, con mayor probabilidad de ser difícil e intermedia, y luego una palabra de esa categoría.
    """
    categorias = [palabras_faciles, palabras_intermedias, palabras_dificiles]
    pesos = [0.2, 0.3, 0.5]
    categoria_seleccionada = choices(categorias, weights=pesos, k=1)[0]
    return choice(categoria_seleccionada).upper()

def encabezado():
    # Muestra el encabezado del juego.
    print("\n=======================================")
    print(" ¡Bienvenido(a) al juego El Ahorcado! ")
    print("=======================================")

def info_extra(palabra):
    # Muestra información adicional si la palabra contiene la letra "Ü".
    if "Ü" in palabra:
        print("\nAquí la letra más extraña para copiarla: ü")
        print("(Para poder copiarla necesitas estar por lo menos fuera de PyCharm)")

def palabra_oculta(letras_correctas, palabra):
    # Devuelve una lista, mostrando las letras correctas ingresadas y guiones para el resto.
    return [l if l in letras_correctas else '-' for l in palabra]

def estado(letras_incorrectas, vidas, letras_correctas, palabra):
    """
    Muestra el estado actual del juego, incluyendo las vidas, letras incorrectas, diagrama del ahorcado y la palabra
    oculta.
    """
    if letras_incorrectas:
        print(f"\nVidas: {vidas} (Letras incorrectas: {', '.join(letras_incorrectas)})")
    else:
        print(f"\nVidas: {vidas}")

    print(vidas_diccionario_visual[vidas])
    print(" ".join(palabra_oculta(letras_correctas, palabra)))

def validar_letra(letra, letras_correctas, letras_incorrectas, palabra):
    """
    Se debe ingresar una letra que pertenezca al alfabeto español (Á, Ü, Ñ, ...) y no debe haber sido ingresada
    anteriormente. Si no, retorna False.
    Si la letra está en la palabra, se añade a letras_correctas y retorna True; si no, se añade a letras_incorrectas y
    retorna False.
    """
    letras_validas = "AÁBCDEÉFGHIÍJKLMNÑOÓPQRSTUÚÜVWXYZ"

    if (len(letra) != 1) or (letra not in letras_validas):
        print("\nHas ingresado algo inválido.")
        return False
    elif letra in (letras_correctas | set(letras_incorrectas)):
        print("\nYa has ingresado esa letra.")
        return False
    elif letra in palabra:
        letras_correctas.add(letra)
        return True
    else:
        letras_incorrectas.append(letra)
        return False

def jugar():
    # Función principal que ejecuta la lógica del juego del Ahorcado.
    palabra = seleccionar_palabra(palabras_faciles, palabras_intermedias, palabras_dificiles)
    vidas = 7
    letras_correctas = set()
    letras_incorrectas = []

    encabezado()
    info_extra(palabra)

    while '-' in palabra_oculta(letras_correctas, palabra) and vidas > 0:
        estado(letras_incorrectas, vidas, letras_correctas, palabra)

        try:
            letra = input("\nElige una letra: ").upper()
        except KeyboardInterrupt:
            print("\n\nSaliendo del programa ...")
            exit()

        if not validar_letra(letra, letras_correctas, letras_incorrectas, palabra):
            vidas -= 1

    estado(letras_incorrectas, vidas, letras_correctas, palabra)

    if vidas == 0:
        print("\n¡Lo siento! Has perdido el juego.")
    else:
        print("\n¡Felicidades! Has ganado el juego.")

    print(f"La palabra era {palabra}")

def main():
    # Llamar a la función principal.
    jugar()

if __name__ == "__main__":
    # Si el módulo se está ejecutando como programa principal, se inicia el juego.
    main()
