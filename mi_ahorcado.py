from random import choices, choice
from os import getenv
from ahorcado_palabras import *
from ahorcado_diagramas import vidas_diccionario_visual
from ahorcado_diagramas_pycharm import vidas_diccionario_visual_pycharm

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
    print(" ▶ ¡Bienvenid@ al juego El Ahorcado! ")
    print("=======================================")

def info_extra(palabra):
    # Muestra información adicional si la palabra contiene la letra "Ü".
    print("\nPresione Ctrl+C para salir.")
    print("Aquí los carácteres más extraños para copiarlos: Á É Í Ó Ú Ü")

def ejecutando_en_entorno():
    """
    Retorna True si el programa se está ejecutando en PyCharm o VSCode, y False si no se está ejecutando en ninguno de
    esos entornos
    """
    global pycharm
    pycharm = getenv("PYCHARM_HOSTED") == "1"
    vscode = getenv("VSCODE_PID") is not None or getenv("TERM_PROGRAM") == "vscode"
    return pycharm or vscode  # solo puede devolver uno de los dos

def palabra_oculta(letras_correctas, palabra):
    # Devuelve una lista, mostrando las letras correctas ingresadas y guiones para el resto.
    return [l if l in letras_correctas else '➖' for l in palabra]

def estado(vidas, letras_incorrectas, letras_correctas, palabra, final=False):
    """
    Muestra el estado actual del juego, incluyendo las vidas, letras incorrectas, diagrama del ahorcado y la palabra
    oculta.
    """
    if vidas > 0:
        hearts = "  ".join("❤️" for _ in range(vidas))
        if letras_incorrectas:
            hearts += " "
        sep = "" if ejecutando_en_entorno() else " "
    else:
        hearts = "💔"
        sep = " "

    msg = f"\nVidas: {vidas} {hearts}"

    if letras_incorrectas:
        if len(letras_incorrectas) == 1:
            msg += f"{sep}(Letra incorrecta: {letras_incorrectas[0]})"
        else:
            msg += f"{sep}(Letras incorrectas: {', '.join(letras_incorrectas)})"

    print(msg)

    if pycharm:
        print(vidas_diccionario_visual_pycharm[vidas])
    else:
        print(vidas_diccionario_visual[vidas])

    print(" ".join(palabra_oculta(letras_correctas, palabra)).center(35))

    if final:
        if vidas == 0:
            print("\n😵 ¡Lo siento! Has perdido el juego.")
        else:
            print("\n🎉 ¡Felicidades! Has ganado el juego.")

        print(f"🤫 La palabra era {palabra}.")

def obtener_letra():
    try:
        if ejecutando_en_entorno():
            letra = input("\n➡️ Elige una letra: ").upper()
        else:
            letra = input("\n➡️  Elige una letra: ").upper()
    except KeyboardInterrupt:
        print("\n\nSaliendo del programa ...")
        exit()

    return letra

def validar_letra(letra, letras_correctas, letras_incorrectas, palabra):
    """
    Se debe ingresar una letra que pertenezca al alfabeto español (Á, Ü, Ñ, ...) y no debe haber sido ingresada
    anteriormente. Si no, retorna False.
    Si la letra está en la palabra, se añade a letras_correctas y retorna True; si no, se añade a letras_incorrectas y
    retorna False.
    """
    letras_validas = "AÁBCDEÉFGHIÍJKLMNÑOÓPQRSTUÚÜVWXYZ"

    if (len(letra) != 1) or (letra not in letras_validas):
        if ejecutando_en_entorno():
            print("\n⚠️ Has ingresado algo inválido.")
        else:
            print("\n⚠️  Has ingresado algo inválido.")
        return False
    elif letra in (letras_correctas | set(letras_incorrectas)):
        print("\n🔄 Ya has ingresado esa letra.")
        return False
    elif letra in palabra:
        letras_correctas.add(letra)
        print(f"\n✅ ¡Correcto! '{letra}' está en la palabra.")
        return True
    else:
        letras_incorrectas.append(letra)
        print(f"\n❌ ¡Incorrecto! '{letra}' no está en la palabra.")
        return False

def jugar():
    # Función principal que ejecuta la lógica del juego del Ahorcado.
    palabra = seleccionar_palabra(palabras_faciles, palabras_intermedias, palabras_dificiles)
    vidas = 7
    letras_correctas = set()
    letras_incorrectas = []

    encabezado()
    info_extra(palabra)

    while '➖' in palabra_oculta(letras_correctas, palabra) and vidas > 0:
        estado(vidas, letras_incorrectas, letras_correctas, palabra)

        letra = obtener_letra()

        if not validar_letra(letra, letras_correctas, letras_incorrectas, palabra):
            vidas -= 1

    estado(vidas, letras_incorrectas, letras_correctas, palabra, final=True)

def main():
    # Llamar a la función principal.
    jugar()

if __name__ == "__main__":
    # Si el módulo se está ejecutando como programa principal, se inicia el juego.
    main()
