import csv

ARCHIVO_EMPLEADOS = "empleados.csv"
ARCHIVO_TURNOS = "turnos.csv"
ARCHIVO_SOLICITUDES = "solicitudes.csv"


def cargar_empleados():
    empleados = {}

    with open(ARCHIVO_EMPLEADOS, encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)

        for fila in lector:
            empleados[int(fila["id"])] = {
                "nombre": fila["nombre"],
                "dias_libres": int(fila["dias_libres"])
            }

    return empleados


def validar_id(empleados):

    while True:

        try:
            id_empleado = int(input("Ingrese su ID: "))

            if id_empleado in empleados:
                return id_empleado

            print("ID no encontrado.")

        except ValueError:
            print("Error: debe ingresar un número.")


def ver_turno(id_empleado):

    print("\n--- TURNOS SEMANALES ---")

    with open(ARCHIVO_TURNOS, encoding="utf-8") as archivo:

        lector = csv.DictReader(archivo)

        for fila in lector:

            if int(fila["id_empleado"]) == id_empleado:

                print(f"{fila['dia']} - {fila['turno']}")


def registrar_solicitud(id_empleado, tipo, detalle):

    filas = []

    with open(ARCHIVO_SOLICITUDES, encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        filas = list(lector)

    nuevo_id = len(filas) + 1

    with open(ARCHIVO_SOLICITUDES, "a", newline="", encoding="utf-8") as archivo:

        campos = [
            "id_solicitud",
            "id_empleado",
            "tipo",
            "detalle",
            "estado"
        ]

        escritor = csv.DictWriter(archivo, fieldnames=campos)

        escritor.writerow({
            "id_solicitud": nuevo_id,
            "id_empleado": id_empleado,
            "tipo": tipo,
            "detalle": detalle,
            "estado": "Pendiente"
        })


def solicitar_cambio_turno(id_empleado):

    dia = input("Ingrese el día solicitado: ")
    turno = input("Ingrese el turno deseado: ")

    registrar_solicitud(
        id_empleado,
        "Cambio de turno",
        f"{dia} {turno}"
    )

    print("Solicitud registrada correctamente.")


def pedir_dia_libre(id_empleado, empleados):

    fecha = input("Ingrese la fecha solicitada: ")

    if empleados[id_empleado]["dias_libres"] > 0:

        registrar_solicitud(
            id_empleado,
            "Día libre",
            fecha
        )

        print("Solicitud registrada correctamente.")

    else:

        print("No posee días libres disponibles.")


empleados = cargar_empleados()

print("=" * 40)
print("CHATBOT DE GESTIÓN DE TURNOS - CASA 52")
print("=" * 40)

id_empleado = validar_id(empleados)

print(f"\nBienvenido/a {empleados[id_empleado]['nombre']}")

while True:

    print("\nMENÚ")
    print("1 - Ver turno semanal")
    print("2 - Solicitar cambio de turno")
    print("3 - Pedir día libre")
    print("4 - Salir")

    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        ver_turno(id_empleado)

    elif opcion == "2":
        solicitar_cambio_turno(id_empleado)

    elif opcion == "3":
        pedir_dia_libre(id_empleado, empleados)

    elif opcion == "4":
        print("Gracias por utilizar el sistema.")
        break

    else:
        print("Opción no válida.")
