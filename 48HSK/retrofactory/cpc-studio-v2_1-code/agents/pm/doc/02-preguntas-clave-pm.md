---
title: "Preguntas clave que el corpus debe poder responder"
category: "meta"
audience: ["pm", "technical-lead", "designer"]
keywords: ["preguntas", "requisitos", "cobertura", "RAG"]
---

# Preguntas clave PM+técnica

El corpus debería poder responder estas preguntas. Si alguna no tiene cobertura,
es una laguna que rellenar.

## Hardware y restricciones

- ¿Cuánta RAM libre tiene un juego típico en cada plataforma después de que el sistema operativo / ROM ocupe la suya?
- ¿Cuántos sprites por hardware soporta cada máquina y cuáles son los trucos para superar ese límite?
- ¿Qué modos gráficos tiene el Amstrad CPC y cuál es el más usado para juegos?
- ¿Qué es el "color clash" del Spectrum y cómo afecta al diseño visual?
- ¿Cuántos canales de sonido tiene el SID del C64 frente al AY del CPC/Spectrum/MSX?
- ¿Qué diferencia práctica hay entre el TMS9918A del MSX y el VIC-II del C64 para sprites?
- ¿Cuánto tarda en cargar un juego desde cinta en cada plataforma?
- ¿Qué supone desarrollar para cinta vs. disco vs. cartucho en términos de tiempos de carga y tamaño?
- ¿Cuál es el mapa de memoria típico de cada plataforma y dónde colocar código, datos y buffers de pantalla?

## Diseño condicionado por hardware

- ¿Cómo afectan las limitaciones de sprites a la elección entre plataformas vs. shoot'em ups?
- ¿Es viable un RPG con scroll suave en Spectrum 48K? ¿Y en CPC?
- ¿Cuántos enemigos simultáneos en pantalla son razonables en cada plataforma?
- ¿Qué géneros de juego se adaptan mejor a cada máquina y por qué?
- ¿Cómo diseñar pantallas que respeten las limitaciones de color del Spectrum (atributos 8x8)?
- ¿Cuánto ocupa típicamente un nivel/mapa y cómo comprimir datos en máquinas con 48-64 KB?

## Producción y gestión de proyecto

- ¿Cuánto duraba típicamente el desarrollo de un juego comercial 8-bit en los años 80?
- ¿Cuál era el tamaño de equipo habitual? ¿Cómo se dividían los roles?
- ¿Cómo estimar el esfuerzo de un port entre plataformas (p.ej. Spectrum → CPC)?
- ¿Qué dependencias críticas tiene un proyecto 8-bit (herramientas, hardware de desarrollo, testing)?
- ¿Cómo planificar sprints/hitos para un juego retro moderno?
- ¿Qué riesgos técnicos son los más frecuentes (quedarse sin RAM, rendimiento, bugs de timing)?
- ¿Cómo se distribuía un juego en los 80 y cómo se distribuye uno retro hoy?
- ¿Qué coste tiene hacer un juego multiplataforma 8-bit hoy vs. mono-plataforma?

## Herramientas y flujo de trabajo

- ¿Qué cross-assemblers y cross-compilers se usan hoy para cada plataforma?
- ¿Qué emuladores son fiables para testing y cuáles tienen debugger integrado?
- ¿Qué editores de sprites/tiles existen para cada plataforma?
- ¿Cómo se monta un pipeline de build moderno (CI/CD) para un juego 8-bit?
- ¿Qué trackers de música se usan para el AY y para el SID?

## Comparativas cruzadas

- ¿Cuál de las 4 plataformas tiene mejor soporte de scroll por hardware?
- ¿Cuál tiene más RAM libre para el programador?
- ¿Cuál es la más fácil/difícil para un primer proyecto retro?
- ¿Cuál tiene la comunidad homebrew más activa hoy?
- ¿Qué plataforma ofrece mejor relación esfuerzo/resultado visual?
