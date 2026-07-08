# adfilt-flattened

Versión aplanada (flattened) de la **AnnoyancesList** de
[DandelionSprout/adfilt](https://github.com/DandelionSprout/adfilt), con todas
las directivas `!#include` resueltas y fusionadas en un solo archivo.

Los adblockers (Brave, AdGuard, uBO) **no** resuelven `!#include` en listas
custom de terceros, solo en listas que el propio vendor empaqueta. Este repo
fusiona todos los includes en un único `.txt` plano y lo regenera solo vía
GitHub Actions (cron diario + disparo manual), sin servidor.

## Uso en Brave

`brave://settings/shields/filters` → *Add custom filter list*:

```
https://raw.githubusercontent.com/EmileBri/adfilt-flattened/main/AnnoyancesList_merged.txt
```

## Cómo funciona

- `scripts/merge.py` — fetch recursivo de la lista raíz y de cada `!#include`,
  normalizando encoding de URL (las rutas del repo fuente mezclan `%20` con
  caracteres unicode sin encodear).
- `.github/workflows/update-filterlist.yml` — cron 06:00 UTC + `workflow_dispatch`;
  regenera el archivo y hace commit + push solo si hubo cambios.
