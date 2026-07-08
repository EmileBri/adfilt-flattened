import urllib.request, urllib.parse, re, sys

BASE = "https://raw.githubusercontent.com/DandelionSprout/adfilt/master/"
ENTRY_POINT = "AnnoyancesList"  # sin .txt, así vive en el repo
OUTPUT_FILE = "AnnoyancesList_merged.txt"

# Algunos includes en el repo fuente apuntan a rutas relativas a la raíz,
# pero el archivo real vive en una subcarpeta distinta (inconsistencia
# confirmada del propio repo, ej. "Dandelion Sprout's Anti-Malware List —
# AdGuardOnlyEntries.txt" en realidad vive en
# "Alternate versions Anti-Malware List/"). Por eso hay fallback de prefijos.
FALLBACK_PREFIXES = ["", "Alternate versions Anti-Malware List/",
                     "uBO list extensions/", "Sensitive lists/"]

visited = set()
output_lines = []

def normalize(path_encoded):
    decoded = urllib.parse.unquote(path_encoded)
    return urllib.parse.quote(decoded, safe='/')

def fetch(path_encoded):
    decoded = urllib.parse.unquote(path_encoded)
    for prefix in FALLBACK_PREFIXES:
        candidate = prefix + decoded if not decoded.startswith(prefix) else decoded
        url = BASE + urllib.parse.quote(candidate, safe='/')
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=20) as r:
                return r.read().decode('utf-8', errors='replace')
        except Exception:
            continue
    return None

def process(path_encoded):
    key = normalize(path_encoded)
    if key in visited:
        return
    visited.add(key)
    content = fetch(path_encoded)
    if content is None:
        output_lines.append(f"! [MERGE ERROR] Could not fetch: {path_encoded}")
        sys.stderr.write(f"FAILED: {path_encoded}\n")
        return
    output_lines.append(
        f"\n!------------------------------------------------------------\n"
        f"! BEGIN: {urllib.parse.unquote(path_encoded)}\n"
        f"!------------------------------------------------------------\n"
    )
    for line in content.splitlines():
        m = re.match(r'^!#include (.+)$', line)
        if m:
            process(m.group(1).strip())
        else:
            output_lines.append(line)
    output_lines.append(f"\n! END: {urllib.parse.unquote(path_encoded)}\n")

process(ENTRY_POINT)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(output_lines))

print(f"Files merged: {len(visited)}")
for v in sorted(visited):
    print(" -", urllib.parse.unquote(v))
