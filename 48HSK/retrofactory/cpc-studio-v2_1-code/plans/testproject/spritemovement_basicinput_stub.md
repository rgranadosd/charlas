# Stub slice: spritemovement_basicinput

## Objective
Lograr que un punto o pequeño sprite se mueva en respuesta a las teclas de flecha (o WASD) presionadas, demostrando la lectura de entrada y la modificación de coordenadas gráficas.

## Implementation notes
- Inicializar CPCtelera con cpct_disableFirmware antes del dibujo.
- Mantener la slice sin entrada ni movimiento.
- Dibujar un bloque visible en una posición fija usando memoria de vídeo.
- Usar un bucle final simple para mantener la imagen visible en pantalla.

## Validation checks
- Existe src/main.c en el proyecto.
- El main.c contiene inicialización básica CPCtelera.
- El main.c contiene dibujo estático visible.
- El main.c no depende de lectura de teclado.
- Se genera un manifest JSON de artefactos.
- Se genera un documento markdown con resumen de la slice.
