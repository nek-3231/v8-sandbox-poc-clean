import re
import sys

def extract_v8_offsets(header_path):
    with open(header_path, 'r', encoding='utf-8') as f:
        src = f.read()

    targets = [
        'kWasmTableObjectTrustedDispatchTableOffset',
        'kMemory0StartOffset',
        'kWasmImportDataSigOffset'
    ]

    found = {}
    for t in targets:
        match = re.search(rf'(?:static\s+)?constexpr\s+int\s+{t}\s*=\s*(0x[0-9a-fA-F]+|\d+);', src)
        if match:
            found[t] = match.group(1)
        else:
            m_field = re.search(rf'DECL_GETTER\([^)]+,\s*{t}[^)]*\)', src)
            found[t] = "MANUAL_CHECK" if not m_field else "DECL_FOUND"

    return found

def patch_poc_offsets(poc_path, offsets):
    with open(poc_path, 'r', encoding='utf-8') as f:
        code = f.read()

    for k, v in offsets.items():
        if v.startswith('0x'):
            print(f"[*] Pat_patch: {k} -> {v}")
            code = re.sub(rf'(const\s+{k}\s*=\s*)0x[0-9a-fA-F]+;', rf'\1{v};', code)

    with open(poc_path, 'w', encoding='utf-8') as f:
        f.write(code)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("[-] Uso: python3 v8_autotune.py <ruta/a/wasm-objects.h> <ruta/a/poc.js>")
        sys.exit(1)

    offsets = extract_v8_offsets(sys.argv[1])
    print(f"[+] Offsets detectados: {offsets}")
    patch_poc_offsets(sys.argv[2], offsets)
