---
title: "Taxonomía y metadatos"
category: "meta"
audience: ["pm", "technical-lead"]
keywords: ["taxonomía", "metadatos", "clasificación", "RAG", "schema"]
---

# Taxonomía y metadatos del corpus

## Esquema de clasificación

Cada documento del corpus pertenece a una o más de estas dimensiones:

### Por plataforma (`platform`)

| Valor | Descripción |
|-------|-------------|
| `amstrad-cpc` | Amstrad CPC 464/6128 (Z80A, 64-128 KB) |
| `zx-spectrum` | ZX Spectrum 48K/128K (Z80A, 48-128 KB) |
| `commodore-64` | Commodore 64 (6510, 64 KB) |
| `msx` | MSX / MSX2 (Z80A, 64+ KB) |
| `cross-platform` | Aplicable a todas las plataformas |

### Por categoría (`category`)

| Valor | Descripción |
|-------|-------------|
| `hardware` | Especificaciones y arquitectura de la máquina |
| `graphics` | Modos de vídeo, paleta, sprites, tiles, scroll |
| `audio` | Chips de sonido, canales, limitaciones |
| `memory` | RAM, ROM, bancos, mapa de memoria |
| `storage` | Cintas, discos, cartuchos, tiempos de carga |
| `production` | Planificación, estimación, sprints, equipo |
| `design` | Decisiones de game design condicionadas por hardware |
| `tools` | Ensambladores, cross-compilers, editores, emuladores |
| `glossary` | Definiciones de términos |
| `meta` | Documentos sobre el propio corpus |

### Por audiencia (`audience`)

| Valor | Descripción |
|-------|-------------|
| `pm` | Project manager / producer |
| `designer` | Game designer |
| `programmer` | Programador (ASM, BASIC, C) |
| `artist` | Artista gráfico / pixel artist |
| `musician` | Compositor / sound designer |
| `technical-lead` | Perfil híbrido técnico + gestión |

## Campos de metadatos (frontmatter YAML)

Todos los documentos del corpus usan este frontmatter:

```yaml
---
title: "Nombre descriptivo del documento"
platform: "amstrad-cpc"          # o array: ["amstrad-cpc", "zx-spectrum"]
category: "hardware"             # o array: ["hardware", "graphics"]
audience: ["pm", "programmer"]
keywords: ["Z80", "memoria", "bancos"]
version: "1.0"
date: "2026-06-30"
source_url: ""                   # si sintetizado de fuente externa
source_date: ""                  # fecha de la fuente original
---
```

## Reglas de nombrado

- Ficheros: `NN-nombre-descriptivo.md` donde `NN` es el rango temático.
- Rangos: `00-09` meta, `10-19` fichas por plataforma, `20-29` restricciones, `30-39` producción, `40-49` glosario/referencia.
- Todo en minúsculas, guiones para separar palabras.

## Relaciones entre documentos

- Las **fichas** (`10-13`) dan el panorama general de cada plataforma.
- Las **restricciones** (`20-23`) profundizan en las limitaciones con impacto en producción.
- La **producción** (`30`) cruza las 4 plataformas con enfoque de gestión.
- El **glosario** (`40`) normaliza términos para que las búsquedas semánticas funcionen.
- Las **preguntas clave** (`02`) definen qué debe saber responder el RAG.
