import os
import re
from datetime import datetime

CLIENTS_DIR = os.path.join(os.path.dirname(__file__), "clientes")

#Tabla hash (diccionario): nombre_normalizado -> ruta_archivo
CLIENT_INDEX: dict[str, str] = {}


def ensure_storage():
    os.makedirs(CLIENTS_DIR, exist_ok=True)


def now_str():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def normalize_key(name: str) -> str:   
   #Normaliza el nombre para usarlo como clave en la tabla hash.
   # - recorta
   # - colapsa espacios
   # - minúsculas    
    return " ".join(name.strip().split()).lower()


def sanitize_name(name: str) -> str:
    name = " ".join(name.strip().split())
    if not name:
        return ""
    safe = name.replace(" ", "_")
    safe = re.sub(r"[^A-Za-z0-9_\-]", "", safe)
    return safe


def client_path(client_name: str) -> str:
    safe = sanitize_name(client_name)
    return os.path.join(CLIENTS_DIR, f"{safe}.txt")


# ---------- Hash table / índice ----------
def load_index() -> None:    
    #Construye el diccionario (tabla hash) a partir de los archivos en /clientes.
    #key: nombre_normalizado (ej. 'juan perez')
    #value: ruta completa del archivo    
    ensure_storage()
    CLIENT_INDEX.clear()

    for fname in os.listdir(CLIENTS_DIR):
        if not fname.lower().endswith(".txt"):
            continue

        fpath = os.path.join(CLIENTS_DIR, fname)

        # Intentamos leer el nombre real desde la línea "Cliente: ..."
        client_name = None
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                for _ in range(10):  # buscamos en las primeras líneas
                    line = f.readline()
                    if not line:
                        break
                    if line.startswith("Cliente: "):
                        client_name = line.replace("Cliente: ", "").strip()
                        break
        except OSError:
            continue

        # Si no se encontró, usamos el nombre del archivo como fallback
        if not client_name:
            client_name = os.path.splitext(fname)[0].replace("_", " ")

        CLIENT_INDEX[normalize_key(client_name)] = fpath


def get_client_file(name: str) -> str | None:    
    #Busca en la tabla hash y retorna la ruta del archivo si existe.    
    return CLIENT_INDEX.get(normalize_key(name))


def add_to_index(name: str) -> None:    
    #Agrega/actualiza un cliente en el índice después de crearlo.    
    CLIENT_INDEX[normalize_key(name)] = client_path(name)


def remove_from_index(name: str) -> None:    
    #Elimina un cliente del índice después de borrarlo.    
    CLIENT_INDEX.pop(normalize_key(name), None)


def list_clients_from_index() -> list[str]:
    #Lista clientes usando el índice (tabla hash).
    # Convertimos claves normalizadas a forma "Title-ish" solo para mostrar    
    return sorted(CLIENT_INDEX.keys())


# ---------- Operaciones ----------
def create_client(name, contact, service, desc):
    fpath = get_client_file(name)
    if fpath and os.path.exists(fpath):
        return False, "El cliente ya existe."

    safe = sanitize_name(name)
    if not safe:
        return False, "Nombre invalido."

    if not service or not desc:
        return False, "Servicio y descripcion son obligatorios."

    ensure_storage()
    path = client_path(name)

    with open(path, "w", encoding="utf-8") as f:
        f.write("AXANET - EXPEDIENTE DE CLIENTE\n")
        f.write(f"Cliente: {name}\n")
        f.write(f"Archivo: {os.path.basename(path)}\n")
        f.write(f"Contacto: {contact if contact else 'N/A'}\n")
        f.write(f"Fecha de creación: {now_str()}\n")
        f.write("----------------------------------------\n")
        f.write("HISTORIAL DE SOLICITUDES:\n")
        f.write(f"- [{now_str()}] {service} | {desc}\n")

    add_to_index(name)
    return True, "Cliente creado correctamente."


def read_client(name):
    path = get_client_file(name)
    if not path or not os.path.exists(path):
        return False, "Cliente no encontrado."

    with open(path, "r", encoding="utf-8") as f:
        return True, f.read()


def update_contact(name, new_contact):
    path = get_client_file(name)
    if not path or not os.path.exists(path):
        return False, "Cliente no encontrado."

    if not new_contact:
        return False, "El contacto no puede estar vacío."

    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    updated = False
    new_lines = []

    for line in lines:
        if line.startswith("Contacto: "):
            new_lines.append(f"Contacto: {new_contact}\n")
            updated = True
        else:
            new_lines.append(line)

    if not updated:
        out = []
        inserted = False
        for line in new_lines:
            out.append(line)
            if line.startswith("Archivo: ") and not inserted:
                out.append(f"Contacto: {new_contact}\n")
                inserted = True
        new_lines = out

    with open(path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

    return True, "Contacto actualizado."


def delete_client(name):
    path = get_client_file(name)
    if not path or not os.path.exists(path):
        return False, "Cliente no encontrado."

    os.remove(path)
    remove_from_index(name)
    return True, "Cliente eliminado."


def add_request(name, service, desc):
    path = get_client_file(name)
    if not path or not os.path.exists(path):
        return False, "Cliente no encontrado."

    if not service or not desc:
        return False, "Servicio y descripcion son obligatorios."

    with open(path, "a", encoding="utf-8") as f:
        f.write(f"- [{now_str()}] {service} | {desc}\n")

    return True, "Solicitud agregada."