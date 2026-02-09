import client_manager as cm


def show_menu():
    print("\n========================================")
    print(" AXANET - Gestion de Clientes (Python)")
    print("========================================")
    print("1) Crear cliente nuevo")
    print("2) Consultar cliente")
    print("3) Modificar contacto")
    print("4) Borrar cliente")
    print("5) Agregar solicitud a cliente existente")
    print("6) Listar clientes")
    print("0) Salir")


def main():
    cm.ensure_storage()
    cm.load_index()
    
    while True:
        show_menu()
        option = input("Selecciona una opcion: ").strip()

        if option == "1":
            name = input("Nombre del cliente: ")
            contact = input("Contacto (opcional): ")
            service = input("Servicio: ")
            desc = input("Descripción: ")
            ok, msg = cm.create_client(name, contact, service, desc)
            print(msg)

        elif option == "2":
            name = input("Nombre del cliente: ")
            ok, result = cm.read_client(name)
            print(result)

        elif option == "3":
            name = input("Nombre del cliente: ")
            contact = input("Nuevo contacto: ")
            ok, msg = cm.update_contact(name, contact)
            print(msg)

        elif option == "4":
            name = input("Nombre del cliente a borrar: ")
            confirm = input("¿Seguro? (SI/NO): ").upper()
            if confirm == "SI":
                ok, msg = cm.delete_client(name)
                print(msg)
            else:
                print("Operacion cancelada.")

        elif option == "5":
            name = input("Nombre del cliente: ")
            service = input("Nuevo servicio: ")
            desc = input("Descripcion: ")
            ok, msg = cm.add_request(name, service, desc)
            print(msg)

        elif option == "6":
            keys = cm.list_clients_from_index()
            
            if not keys:
                print("No hay clientes registrados.")
            else:
                 print("\nClientes (desde tabla hash):")
                 for k in keys:
                    print(f" - {k}")

        elif option == "0":
            print("Saliendo...")
            break

        else:
            print("Opcion invalida.")


if __name__ == "__main__":
    main()