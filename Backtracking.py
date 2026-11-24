from Datos import *
import time

retrocesos = 0
intentos = 0


def algoritmo_backtracking(posicion, horario,
                           pendientes, carga, ocupados):

    global retrocesos, intentos

    # Caso base: se completaron los 450 espacios
    if posicion == 450:
        return True

    # Determinar periodo y sección correspondiente
    turno = posicion // len(secciones)
    seccion = secciones[posicion % len(secciones)]

    opciones = obtener_opciones(
        seccion, turno, horario,
        pendientes, carga, ocupados
    )

    # Explorar las alternativas disponibles
    for materia, docente in opciones:

        intentos += 1

        # Realizar una asignación
        asignar(
            seccion, turno, materia, docente,
            horario, pendientes, carga, ocupados
        )

        # Continuar mediante recursividad
        if algoritmo_backtracking(
            posicion + 1, horario,
            pendientes, carga, ocupados
        ):
            return True

        # Deshacer la asignación si genera un conflicto
        deshacer(
            seccion, turno, materia, docente,
            horario, pendientes, carga, ocupados
        )

        retrocesos += 1

    return False


# EJECUCIÓN DEL ALGORITMO

horario, pendientes, carga, ocupados = inicializar()

inicio = time.perf_counter()

resultado = algoritmo_backtracking(
    0, horario, pendientes, carga, ocupados
)

fin = time.perf_counter()

print("\nALGORITMO BACKTRACKING")

if resultado:
    print("Se encontró un horario válido.")
    mostrar_horarios(horario, carga)
else:
    print("No se encontró una solución válida.")

print(f"\nIntentos realizados: {intentos}")
print(f"Retrocesos realizados: {retrocesos}")
print(f"Tiempo de ejecución: {(fin - inicio) * 1000:.4f} ms")