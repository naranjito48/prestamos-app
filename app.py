import json
import os

# Nombre del archivo para guardar los datos
DATA_FILE = "prestamos.json"

def cargar_datos():
    """Carga los datos de los préstamos desde el archivo JSON."""
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def guardar_datos(data):
    """Guarda los datos de los préstamos en el archivo JSON."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def agregar_prestamo():
    """Agrega un nuevo préstamo."""
    print("\n--- Agregar Nuevo Préstamo ---")
    nombre = input("Nombre de la persona: ")
    while True:
        try:
            monto = float(input("Monto a prestar (sin interés): "))
            if monto > 0:
                break
            else:
                print("Por favor, ingresa un monto positivo.")
        except ValueError:
            print("Por favor, ingresa un número válido.")

    while True:
        try:
            cuotas = int(input("Número de cuotas: "))
            if cuotas > 0:
                break
            else:
                print("Por favor, ingresa un número de cuotas positivo.")
        except ValueError:
            print("Por favor, ingresa un número entero válido.")

    # Calcula el total a deber con un interés del 10%
    interes = 0.10
    total_a_deber = monto * (1 + interes)
    valor_cuota = total_a_deber / cuotas

    datos = cargar_datos()
    datos[nombre.lower()] = {
        "monto_prestado": monto,
        "total_a_deber": total_a_deber,
        "saldo_pendiente": total_a_deber,
        "numero_cuotas": cuotas,
        "valor_cuota": round(valor_cuota, 2)
    }
    guardar_datos(datos)
    print("\n¡Préstamo agregado con éxito!")
    print(f"{nombre} debe un total de ${total_a_deber:,.2f} en {cuotas} cuotas de ${valor_cuota:,.2f} cada una.")

def ver_prestamos():
    """Muestra todos los préstamos activos."""
    print("\n--- Lista de Préstamos ---")
    datos = cargar_datos()
    if not datos:
        print("No hay préstamos registrados.")
        return

    for nombre, info in datos.items():
        print(f"\nNombre: {nombre.title()}")
        print(f"  - Total Deuda: ${info['total_a_deber']:,.2f}")
        print(f"  - Saldo Pendiente: ${info['saldo_pendiente']:,.2f}")
        print(f"  - Número de Cuotas: {info['numero_cuotas']}")
        print(f"  - Valor por Cuota: ${info['valor_cuota']:,.2f}")

def registrar_pago():
    """Registra el pago a un préstamo existente."""
    print("\n--- Registrar un Pago ---")
    nombre = input("Nombre de la persona que realiza el pago: ").lower()
    datos = cargar_datos()

    if nombre not in datos:
        print(f"No se encontró un préstamo para '{nombre.title()}'.")
        return

    while True:
        try:
            monto_pago = float(input(f"Monto del pago para {nombre.title()}: "))
            if monto_pago > 0:
                break
            else:
                print("El monto del pago debe ser positivo.")
        except ValueError:
            print("Por favor, ingresa un número válido.")

    if monto_pago > datos[nombre]["saldo_pendiente"]:
        print("El monto del pago es mayor que el saldo pendiente. Ajustando al total de la deuda.")
        monto_pago = datos[nombre]["saldo_pendiente"]

    datos[nombre]["saldo_pendiente"] -= monto_pago
    guardar_datos(datos)
    
    nuevo_saldo = datos[nombre]["saldo_pendiente"]
    print("\n¡Pago registrado con éxito!")
    print(f"Nuevo saldo pendiente para {nombre.title()}: ${nuevo_saldo:,.2f}")

    if nuevo_saldo == 0:
        print(f"¡La deuda de {nombre.title()} ha sido saldada!")
        del datos[nombre]
        guardar_datos(datos)


def main():
    """Función principal del programa."""
    while True:
        print("\n===== MENÚ PRINCIPAL =====")
        print("1. Agregar un nuevo préstamo")
        print("2. Ver todos los préstamos")
        print("3. Registrar un pago")
        print("4. Salir")
        
        opcion = input("Elige una opción: ")

        if opcion == '1':
            agregar_prestamo()
        elif opcion == '2':
            ver_prestamos()
        elif opcion == '3':
            registrar_pago()
        elif opcion == '4':
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Por favor, intenta de nuevo.")

if __name__ == "__main__":
    main()
