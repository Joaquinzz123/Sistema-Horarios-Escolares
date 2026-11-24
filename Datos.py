# CONFIGURACIÓN DEL PROBLEMA

dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
periodos = 6

secciones = [
    f"{grado}{letra}"
    for grado in range(1, 6)
    for letra in ["A", "B", "C"]
]

# Asignaturas y carga semanal por sección
materias = {
    "Matemática": 2,
    "Comunicación": 2,
    "Ciencia y Tecnología": 2,
    "Razonamiento Matemático": 2,
    "Razonamiento Verbal": 2,
    "Inglés": 2,
    "Ciencias Sociales": 2,
    "Educación para el Trabajo": 2,
    "Educación Física": 2,
    "Arte y Cultura": 2,
    "Música": 2,
    "Religión": 2,
    "Tutoría": 2,
    "Computación": 2,
    "Lectura": 2
}

# Asignaturas de mayor exigencia cognitiva
exigentes = {
    "Matemática",
    "Comunicación",
    "Ciencia y Tecnología",
    "Razonamiento Matemático",
    "Razonamiento Verbal"
}

# Docentes habilitados por asignatura
docentes = {
    "Matemática": [1, 16],
    "Comunicación": [2, 17],
    "Ciencia y Tecnología": [3, 18],
    "Razonamiento Matemático": [4, 19],
    "Razonamiento Verbal": [5, 20],
    "Inglés": [6, 16],
    "Ciencias Sociales": [7, 17],
    "Educación para el Trabajo": [8, 18],
    "Educación Física": [9, 19],
    "Arte y Cultura": [10, 20],
    "Música": [11, 16],
    "Religión": [12, 17],
    "Tutoría": [13, 18],
    "Computación": [14, 19],
    "Lectura": [15, 20]
}

# Orden de prioridad que alterna asignaturas
orden = [
    "Matemática", "Inglés", "Música",
    "Comunicación", "Ciencias Sociales", "Religión",
    "Ciencia y Tecnología", "Educación para el Trabajo",
    "Tutoría", "Razonamiento Matemático",
    "Educación Física", "Computación",
    "Razonamiento Verbal", "Arte y Cultura", "Lectura"
]


def inicializar():
    horario = {
        s: [None] * 30 for s in secciones
    }

    pendientes = {
        s: materias.copy() for s in secciones
    }

    carga = {
        d: 0 for d in range(1, 21)
    }

    ocupados = [set() for _ in range(30)]

    return horario, pendientes, carga, ocupados


# Obtener asignaciones que cumplen las restricciones
def obtener_opciones(seccion, turno, horario,
                     pendientes, carga, ocupados):

    opciones = []

    for materia in materias:

        # Verificar carga pendiente de la asignatura
        if pendientes[seccion][materia] == 0:
            continue

        # Evitar asignaturas exigentes consecutivas
        if turno % 6 != 0:
            anterior = horario[seccion][turno - 1]

            if (anterior is not None
                    and anterior[0] in exigentes
                    and materia in exigentes):
                continue

        for docente in docentes[materia]:

            # Evitar cruces entre docentes
            if docente in ocupados[turno]:
                continue

            # Respetar el máximo de 28 periodos
            if carga[docente] >= 28:
                continue

            opciones.append((materia, docente))

    # Priorizar materias pendientes y distribuir la carga
    objetivo = (secciones.index(seccion) + turno) % 15

    opciones.sort(
        key=lambda x: (
            -pendientes[seccion][x[0]],
            (orden.index(x[0]) - objetivo) % 15,
            carga[x[1]]
        )
    )

    return opciones


# Registrar una asignación
def asignar(seccion, turno, materia, docente,
            horario, pendientes, carga, ocupados):

    horario[seccion][turno] = (materia, docente)
    pendientes[seccion][materia] -= 1
    carga[docente] += 1
    ocupados[turno].add(docente)


# Deshacer una asignación
def deshacer(seccion, turno, materia, docente,
             horario, pendientes, carga, ocupados):

    horario[seccion][turno] = None
    pendientes[seccion][materia] += 1
    carga[docente] -= 1
    ocupados[turno].remove(docente)


# Mostrar los horarios generados
def mostrar_horarios(horario, carga):

    total = 0

    for seccion in secciones:

        print("\n" + "=" * 55)
        print("HORARIO DE LA SECCIÓN:", seccion)
        print("=" * 55)

        for dia in range(5):

            print("\n" + dias[dia])

            for periodo in range(6):

                turno = dia * 6 + periodo
                clase = horario[seccion][turno]

                if clase is not None:
                    materia, docente = clase

                    print(
                        f"Periodo {periodo + 1}: "
                        f"{materia} - Docente {docente}"
                    )

                    total += 1

                else:
                    print(f"Periodo {periodo + 1}: Sin asignar")

    print("\nCARGA HORARIA DE LOS DOCENTES")

    for docente, cantidad in carga.items():
        print(f"Docente {docente}: {cantidad} periodos")

    print(f"\nPeriodos asignados: {total}/450")
    print(f"Periodos pendientes: {450 - total}")
    print(f"Porcentaje completado: {total / 450 * 100:.2f}%")