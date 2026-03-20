import socket
import subprocess
import re
import os


def abrir_consola_ipconfig():
    """
    Abre una nueva ventana de CMD y ejecuta ipconfig /all
    La ventana queda abierta para verificación manual
    """
    subprocess.Popen(
        'start cmd /k "ipconfig /all"',
        shell=True
    )


def obtener_info_equipo():
    # Hostname
    hostname = socket.gethostname()

    # Ejecutar ipconfig /all para análisis interno
    salida = subprocess.check_output(
        "ipconfig /all",
        shell=True,
        text=True,
        encoding="cp850"
    )

    # Abrir consola extra para comprobar los datos
    abrir_consola_ipconfig()

    # Separar por adaptadores (bloques)
    bloques = salida.split("\n\n")

    ip_encontrada = None
    mac_encontrada = None
    mascara_encontrada = None

    for bloque in bloques:
        bloque_lower = bloque.lower()

        # ❌ Ignorar adaptadores virtuales o no deseados
        if any(x in bloque_lower for x in [
            "virtualbox",
            "vmware",
            "host-only",
            "tunnel",
            "wi-fi direct",
            "bluetooth",
            "isatap",
            "teredo"
        ]):
            continue

        ip_match = re.search(r"IPv4.*?:\s*(\d+\.\d+\.\d+\.\d+)", bloque)
        mac_match = re.search(r"Dirección física.*?:\s*([0-9A-Fa-f\-]{17})", bloque)
        mask_match = re.search(r"Máscara de subred.*?:\s*(\d+\.\d+\.\d+\.\d+)", bloque)
        gateway_match = re.search(r"Puerta de enlace predeterminada.*?:\s*(\d+\.\d+\.\d+\.\d+)", bloque)

        # ✅ Tomar solo adaptador activo real
        if ip_match and gateway_match:
            ip_encontrada = ip_match.group(1)
            mac_encontrada = mac_match.group(1) if mac_match else None
            mascara_encontrada = mask_match.group(1) if mask_match else None
            break

    # Número de serie usando PowerShell
    try:
        ps_command = (
            'powershell -Command '
            '"Get-CimInstance Win32_BIOS | Select-Object -ExpandProperty SerialNumber"'
        )
        serial_number = subprocess.check_output(
            ps_command,
            shell=True,
            text=True,
            encoding="cp850"
        ).strip()

        if not serial_number:
            serial_number = "No disponible"

    except Exception as e:
        serial_number = f"No se pudo obtener: {e}"

    # Mostrar resultados
    print(f"Hostname: {hostname}")
    print(f"Dirección IP: {ip_encontrada}")
    print(f"Dirección MAC: {mac_encontrada}")
    print(f"Máscara de subred: {mascara_encontrada}")
    print(f"Número de serie: {serial_number}")

    # Guardar en archivo
    guardar_en_archivo(
        hostname,
        ip_encontrada,
        mac_encontrada,
        mascara_encontrada,
        serial_number
    )


def guardar_en_archivo(hostname, ip, mac, mascara, serial):
    archivo = "datos_pc.txt"

    ancho_hostname = 20
    ancho_ip = 15
    ancho_mac = 20
    ancho_mascara = 15
    ancho_serial = 25

    if not os.path.exists(archivo):
        with open(archivo, "w", encoding="utf-8") as f:
            f.write(
                f"{'Hostname'.ljust(ancho_hostname)}"
                f"{'IP'.ljust(ancho_ip)}"
                f"{'MAC'.ljust(ancho_mac)}"
                f"{'Máscara'.ljust(ancho_mascara)}"
                f"{'Serial'.ljust(ancho_serial)}\n"
            )
            f.write(
                "-" * (ancho_hostname + ancho_ip + ancho_mac + ancho_mascara + ancho_serial) + "\n"
            )

    with open(archivo, "a", encoding="utf-8") as f:
        f.write(
            f"{hostname.ljust(ancho_hostname)}"
            f"{(ip or 'N/A').ljust(ancho_ip)}"
            f"{(mac or 'N/A').ljust(ancho_mac)}"
            f"{(mascara or 'N/A').ljust(ancho_mascara)}"
            f"{(serial or 'N/A').ljust(ancho_serial)}\n"
        )


if __name__ == "__main__":
    obtener_info_equipo()
    input("\nPresiona ENTER para cerrar...")
