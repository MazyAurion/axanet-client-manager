import argparse
import os
import sys

import client_manager as cm


def main():
    parser = argparse.ArgumentParser(description="CLI para GitHub Actions (Axanet)")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_create = sub.add_parser("crear", help="Crear cliente nuevo")
    p_create.add_argument("--nombre", required=True)
    p_create.add_argument("--contacto", default="")
    p_create.add_argument("--servicio", required=True)
    p_create.add_argument("--descripcion", required=True)

    p_update = sub.add_parser("actualizar", help="Actualizar cliente recurrente (agregar solicitud)")
    p_update.add_argument("--nombre", required=True)
    p_update.add_argument("--servicio", required=True)
    p_update.add_argument("--descripcion", required=True)

    p_query = sub.add_parser("consultar", help="Consultar cliente (imprimir expediente)")
    p_query.add_argument("--nombre", required=True)
    p_query.add_argument("--out", default="consulta_cliente.txt")

    args = parser.parse_args()

    cm.ensure_storage()
    cm.load_index()

    if args.cmd == "crear":
        ok, msg = cm.create_client(args.nombre, args.contacto, args.servicio, args.descripcion)
        print(msg)
        sys.exit(0 if ok else 1)

    if args.cmd == "actualizar":
        ok, msg = cm.add_request(args.nombre, args.servicio, args.descripcion)
        print(msg)
        sys.exit(0 if ok else 1)

    if args.cmd == "consultar":
        ok, content = cm.read_client(args.nombre)
        if not ok:
            print(content)
            sys.exit(1)
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Consulta guardada en: {args.out}")
        sys.exit(0)


if __name__ == "__main__":
    main()