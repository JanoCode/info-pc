# info-pc

Herramienta de inventario para computadores Windows. Obtiene automáticamente la información principal del equipo y la agrega a un archivo de texto, evitando recopilar los datos manualmente máquina por máquina.

## Datos recopilados

- Nombre del equipo (`hostname`)
- Dirección IPv4 del adaptador activo
- Dirección MAC
- Máscara de subred
- Número de serie del BIOS

El programa ignora adaptadores virtuales comunes y elige el adaptador que tiene una puerta de enlace activa. Cada ejecución agrega una nueva fila a `datos_pc.txt`.

## Caso de uso

Está pensado para inventariar rápidamente los computadores de una sala o laboratorio. Después de ejecutar la herramienta en cada equipo, el archivo generado puede renombrarse con el nombre de la sala y conservarse como registro.

> La salida contiene identificadores del equipo y datos de red. Trátala como información interna y no la publiques sin revisarla.

## Requisitos

- Windows
- Python 3.10 o superior

## Ejecutar con Python

```powershell
python infoEquipo.py
```

Al finalizar se crea o actualiza `datos_pc.txt` en la carpeta desde la que se ejecutó el programa.

## Crear un ejecutable

```powershell
python -m pip install pyinstaller
pyinstaller --onefile infoEquipo.py
```

El ejecutable resultante quedará en `dist/infoEquipo.exe`.

## Cómo funciona

1. Ejecuta `ipconfig /all` y separa la salida por adaptador.
2. Descarta adaptadores virtuales, túneles y conexiones no relevantes.
3. Selecciona el adaptador IPv4 activo.
4. Consulta el número de serie mediante `Get-CimInstance Win32_BIOS`.
5. Guarda los resultados en una tabla de texto acumulativa.

## Limitaciones actuales

- La lectura de `ipconfig` depende de que Windows esté configurado en español.
- Está diseñado específicamente para Windows.
- La salida es texto plano; no existe todavía exportación directa a CSV o Excel.

## Mejoras previstas

- Compatibilidad con Windows en distintos idiomas.
- Exportación a CSV.
- Selección más robusta del adaptador principal.
- Pruebas automatizadas para el análisis de la salida.

---

**English summary:** A Windows inventory utility that collects hostname, active IPv4, MAC address, subnet mask and BIOS serial number, then appends them to a local report.

