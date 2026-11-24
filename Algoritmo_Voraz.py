from Datos import *
import time


def algoritmo_voraz():

    horario, pendientes, carga, ocupados = inicializar()

    # Recorrer los 30 periodos semanales
    for turno in range(30):

        # Recorrer las 15 secciones
        for seccion in secciones:

            opciones = obtener_opciones(
                seccion, turno, horario,
                pendientes, carga, ocupados
            )

            # Seleccionar la mejor opción disponible
            if opciones:

                materia, docente = opciones[0]

                asignar(
                    seccion, turno, materia, docente,
                    horario, pendientes, carga, ocupados
                )

    return horario, carga


# EJECUCIÓN DEL ALGORITMO

inicio = time.perf_counter()

horario, carga = algoritmo_voraz()

fin = time.perf_counter()

print("\nALGORITMO VORAZ")

mostrar_horarios(horario, carga)

print(f"\nTiempo de ejecución: {(fin - inicio) * 1000:.4f} ms")