---
title: "Corpus híbrido PM+técnica para RAG de videojuegos 8-bit"
scope: ["Amstrad CPC", "ZX Spectrum", "Commodore 64", "MSX"]
language: "es"
audience: ["pm", "producer", "designer", "technical-lead"]
version: "1.0"
date: "2026-06-30"
---

# Corpus híbrido PM+técnica para RAG de videojuegos 8-bit

Colección de documentos Markdown para alimentar un sistema RAG (Retrieval-Augmented
Generation) sobre producción y desarrollo de videojuegos para plataformas de 8 bits:
**Amstrad CPC**, **ZX Spectrum**, **Commodore 64** y **MSX**.

El enfoque es **híbrido**: combina restricciones técnicas de hardware con decisiones
de producción y gestión de proyecto (PM). Pensado para perfiles que necesitan entender
las limitaciones de la máquina para planificar, estimar y tomar decisiones de diseño.

## Estructura de ficheros

| Fichero | Contenido |
|---------|-----------|
| `00-README.md` | Este fichero: índice y guía de ingestión |
| `01-taxonomia-y-metadatos.md` | Esquema de clasificación y campos de metadatos |
| `02-preguntas-clave-pm.md` | Preguntas que el corpus debería poder responder |
| `03-fuentes-semillero.md` | Fuentes públicas para ampliar el corpus |
| `10-ficha-amstrad-cpc.md` | Ficha híbrida hardware+producción del Amstrad CPC |
| `11-ficha-zx-spectrum.md` | Ficha híbrida del ZX Spectrum |
| `12-ficha-commodore-64.md` | Ficha híbrida del Commodore 64 |
| `13-ficha-msx.md` | Ficha híbrida del MSX |
| `20-restricciones-amstrad-cpc.md` | Restricciones técnicas del CPC y sus implicaciones |
| `21-restricciones-zx-spectrum.md` | Restricciones técnicas del Spectrum |
| `22-restricciones-commodore-64.md` | Restricciones técnicas del C64 |
| `23-restricciones-msx.md` | Restricciones técnicas del MSX |
| `30-produccion-8bit.md` | Enfoque de producción para juegos 8-bit (transversal) |
| `40-glosario.md` | Vocabulario canónico técnico y de producción |

## Recomendación de ingestión para RAG

1. **Chunking semántico** por secciones `##` (cada sección es una unidad de conocimiento autocontenida).
2. **Preservar el frontmatter YAML** como metadatos del documento (se usa para filtrar por plataforma, categoría, audiencia).
3. **Embeddings** sobre título + resumen + cuerpo de cada chunk.
4. **Filtros recomendados**: `platform`, `category`, `audience`, `keywords`.
5. **Versionado**: los documentos llevan fecha; al sintetizar desde fuentes externas, añadir `source_date` y `source_url`.

## Convenciones

- Los documentos **sintetizan conocimiento útil para PM y perfiles híbridos**; no sustituyen documentación técnica primaria, la complementan.
- Cada ficha de plataforma sigue la misma estructura para facilitar comparaciones cruzadas.
- Las restricciones están redactadas en términos de **impacto en producción**, no solo como especificaciones secas.
- El glosario normaliza vocabulario para que las búsquedas semánticas funcionen bien.
