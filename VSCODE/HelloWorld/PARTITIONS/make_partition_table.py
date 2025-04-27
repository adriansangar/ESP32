#!/usr/bin/env python3
"""
make_partition_table.py

Lee un CSV de tabla de particiones ESP32 y genera el binario "partition-table.bin".
Formato CSV: Name,Type,Subtype,Offset,Size,Flags
"""
import csv
import sys
import struct
import hashlib

# Constantes
MAX_PARTITION_LENGTH = 0xC00  # 3072 bytes: entries + checksum + padding
PARTITION_TABLE_SECTOR = 0x1000
DEFAULT_TABLE_OFFSET = 0x8000
MD5_MAGIC = b"\xEB\xEB" + b"\xFF" * 14  # Magic header para checksum

# Mapeos de tipos y subtipos
TYPE_MAP = {
    'app': 0x00,
    'data': 0x01,
}
SUBTYPE_MAP = {
    0x00: {  # app
        'factory': 0x00,
        **{f'ota_{i}': 0x10 + i for i in range(16)},
        'test': 0x20,
    },
    0x01: {  # data
        'ota': 0x00,
        'otadata': 0x00,  # alias común en CSV
        'phy': 0x01,
        'nvs': 0x02,
        'coredump': 0x03,
        'nvs_keys': 0x04,
        'spiffs': 0x82,
        'fat': 0x81,
    },
}
FLAGS_MAP = {
    'encrypt': 0,
    'encrypted': 0,
    'readonly': 1,
}

# Auxiliares

def error(msg):
    print(f"Error: {msg}", file=sys.stderr)
    sys.exit(1)

def parse_size(s):
    s = s.strip().lower()
    if s.endswith('k'):
        return int(s[:-1], 0) * 1024
    if s.endswith('m'):
        return int(s[:-1], 0) * 1024 * 1024
    return int(s, 0)

def align(value, alignment):
    return (value + alignment - 1) // alignment * alignment

# Generación de la tabla

def generate(csv_path, bin_path):
    # Leer y validar CSV
    try:
        f = open(csv_path, newline='')
    except FileNotFoundError:
        error(f"No existe el CSV '{csv_path}'")
    reader = csv.reader(f)
    headers = next(reader, None)
    if [h.strip() for h in headers] != ['Name', 'Type', 'Subtype', 'Offset', 'Size', 'Flags']:
        error(f"Encabezados inválidos: {headers}")

    entries = []
    for i, row in enumerate(reader, start=2):
        if len(row) != 6:
            error(f"Fila {i}: esperar 6 campos, encontré {len(row)}: {row}")
        name, ptype, subtype, off_str, size_str, flags_str = [c.strip() for c in row]
        if not name:
            error(f"Fila {i}: Name vacío")
        if ptype not in TYPE_MAP:
            error(f"Fila {i}: Type inválido '{ptype}'")
        ptype_val = TYPE_MAP[ptype]
        submap = SUBTYPE_MAP.get(ptype_val, {})
        if subtype not in submap:
            error(f"Fila {i}: Subtype inválido '{subtype}' para Type '{ptype}'")
        subtype_val = submap[subtype]
        try:
            size_val = parse_size(size_str)
        except Exception:
            error(f"Fila {i}: Size inválido '{size_str}'")
        off_val = None
        if off_str:
            try:
                off_val = int(off_str, 0)
            except Exception:
                error(f"Fila {i}: Offset inválido '{off_str}'")
        flags_val = 0
        if flags_str:
            for fl in flags_str.split(':'):
                if fl not in FLAGS_MAP:
                    error(f"Fila {i}: Flag desconocida '{fl}'")
                flags_val |= (1 << FLAGS_MAP[fl])
        entries.append({
            'name': name,
            'type': ptype_val,
            'subtype': subtype_val,
            'offset': off_val,
            'size': size_val,
            'flags': flags_val
        })
    f.close()

    # Rellenar offsets faltantes
    last_end = DEFAULT_TABLE_OFFSET + PARTITION_TABLE_SECTOR
    for e in entries:
        if e['offset'] is None:
            align_off = 0x10000 if e['type'] == TYPE_MAP['app'] else 0x1000
            last_end = align(last_end, align_off)
            e['offset'] = last_end
        last_end = e['offset'] + e['size']

    # Construir binario
    table = b''
    for e in entries:
        name_b = e['name'].encode('utf-8')[:16]
        name_b = name_b.ljust(16, b'\x00')
        entry = struct.pack(
            '<2sBBLL16sL',
            b'\xAA\x50',
            e['type'],
            e['subtype'],
            e['offset'],
            e['size'],
            name_b,
            e['flags']
        )
        table += entry

    # Checksum MD5
    md5 = hashlib.md5(table).digest()
    table += MD5_MAGIC + md5

    # Pad a MAX_PARTITION_LENGTH
    if len(table) > MAX_PARTITION_LENGTH:
        error(f"Tabla generada demasiado larga: {len(table)} bytes > {MAX_PARTITION_LENGTH}")
    table += b'\xFF' * (MAX_PARTITION_LENGTH - len(table))

    # Guardar
    with open(bin_path, 'wb') as bf:
        bf.write(table)
    print(f"Generado: {bin_path} ({len(table)} bytes)")

# CLI
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Uso: python make_partition_table.py partitions.csv partition-table.bin")
        sys.exit(1)
    generate(sys.argv[1], sys.argv[2])
