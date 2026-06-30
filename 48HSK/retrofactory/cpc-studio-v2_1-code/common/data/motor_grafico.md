##### 1

# Desarrollo de un

# motor de render 3D

# para Amstrad CPC

# 464

Grado en IngenierÃ­a Multimedia

Trabajo Fin de Grado

#### Autor:

#### Joan Albert Sirvent Jerez

#### Tutor/es:

#### Francisco JosÃ© Gallego DurÃ¡n

#### Septiembre 2017



## 1. MotivaciÃ³n y Objetivos

Cursar este grado y hacer el itinerario de videojuegos me ha reafirmado lo mucho que me gustan

los videojuegos y programar.

He aprendido que actualmente se pueden desarrollar videojuegos de forma relativamente

sencilla con herramientas muy avanzadas y potentes como Unity o Unreal Engine, pero tambiÃ©n

he aprendido cÃ³mo funcionan dichas herramientas por detrÃ¡s durante el desarrollo del proyecto

de 4Âº. De entre todos los aspectos que tocamos durante el desarrollo, uno de los que mÃ¡s

complejo me pareciÃ³ y mÃ¡s me fascinÃ³ fue el del renderizado 3D.

AdemÃ¡s, la participaciÃ³n en el concurso CPCRetroDev fue muy estimulante y me enseÃ±Ã³ la

complejidad y la dificultad que existÃ­a para desarrollar videojuegos en mÃ¡quinas tan limitadas

como el Amstrad CPC 464, aunque el tiempo para el desarrollo del proyecto para dicho

concurso fue bastante limitado y me quedÃ© con ganas de realizar algo mÃ¡s complejo y

desarrollado.

Es por todo ello que tras acabar el proyecto de 4Âº decidÃ­ proponerme un reto que, en caso de

lograrlo, serÃ­a una buena manera de demostrar los conocimientos durante la carrera y mis

capacidades como ingeniero.

El reto que me propuse, y que utilizo como proyecto final del grado, se trata del desarrollo de un

motor de renderizado 3D para Amstrad CPC 464 y su integraciÃ³n en algÃºn proyecto para

mostrar su funcionamiento.

En general, el objetivo de este proyecto es el estudio de los motores 3D primitivos y el

desarrollo de uno para Amstrad CPC 464 usando C y la librerÃ­a CPCtelera, asÃ­ como el

desarrollo de un videojuego de ejemplo usando el motor de renderizado desarrollado.

En detalle, estos serÃ¡n los objetivos a alcanzar en este proyecto:

```
ï‚· El estudio de las limitaciones del Amstrad CPC 464, para poder decidir y planificar
como desarrollar el motor de renderizado.
ï‚· El estudio de las tÃ©cnicas de renderizado usadas en distintos videojuegos 3D,
seleccionando videojuegos desarrollados para mÃ¡quinas con caracterÃ­sticas similares al
Amstrad CPC 464, resaltando los puntos fuertes y sus puntos dÃ©biles de cada tÃ©cnica,
asÃ­ como la viabilidad de usarlas en una mÃ¡quina como el Amstrad.
ï‚· Implementar un motor de renderizado 3D en 8 bits para Amstrad CPC 464,
aplicando las tÃ©cnicas y conocimientos obtenidos en el punto anterior para llevarlo a
cabo.
```

ï‚· Desarrollar un prototipo de videojuego que muestre las capacidades del motor de

```
renderizado desarrollado.
```

## 2. Agradecimientos................................................................................................................

Agradezco en primer lugar a mi familia por el apoyo que me han dado y sobretodo a mi padre,
que sin su apoyo y su dedicaciÃ³n durante todos estos aÃ±os (y no han sido pocos) no me habrÃ­a
sido posible cursar y terminar esta carrera.

A mi tutor Fran, gracias a Ã©l descubrÃ­ el Amstrad y el concurso CPCRetroDev, y con Ã©l aprendÃ­
que para poder avanzar y aprender, primero hay que fallar. AdemÃ¡s, compartimos la pasiÃ³n por
ese oscuro arte de la programaciÃ³n a bajo nivel.

A Miguel Ãngel, por todo su apoyo, tanto durante este proyecto como durante los cursos
anteriores.

A la Universidad de Alicante, por darme la oportunidad de estudiar esta carrera con un
profesorado tan bueno.

Por Ãºltimo, agradecer a todos los amigos que he ido haciendo a lo largo de la carrera, por la
ayuda prestada cuando ha hecho falta, por los buenos ratos que hemos tenido durante estos aÃ±os
y por todo el apoyo que me han prestado.


## 3. Ãndices

## 3. Ãndices

### 3.1. Ãndice de contenidos


### 3.2. Ãndice de figuras


- 1. MotivaciÃ³n y Objetivos 3.1.Ãndice de contenidos
- 2. Agradecimientos................................................................................................................
- 3. Ãndices
   - 3.1. Ãndice de contenidos
   - 3.2. Ãndice de figuras
- 4. IntroducciÃ³n
   - 4.1. TerminologÃ­a
   - 4.2. Estructura del documento
- 5. MetodologÃ­a
- 6. Amstrad CPC 464............................................................................................................
   - 6.1. Hardware
      - 6.1.1. Procesador
      - 6.1.2. Memoria
      - 6.1.3. Video
- 7. TÃ©cnicas de renderizado 3D
   - 7.1. 3D simulado
      - 7.1.1. GrÃ¡ficos vectoriales
      - 7.1.2. GrÃ¡ficos rasterizados
   - 7.2. 3D real
- 8. Desarrollo del motor de renderizado
   - 8.1. MaquetaciÃ³n inicial del algoritmo
   - 8.2. Primera implementaciÃ³n
   - 8.3. RediseÃ±o del algoritmo y maquetaciÃ³n
   - 8.4. Segunda implementaciÃ³n
   - 8.5. Texturizado
   - 8.6. InclusiÃ³n de entidades
   - 8.7. Resultado final del renderer
      - 8.7.1. CaracterÃ­sticas
      - 8.7.2. Limitaciones
- 9. Juego de ejemplo
   - 9.1. DiseÃ±o
   - 9.2. Estructura del motor del juego
   - 9.3. Algoritmo de generaciÃ³n de mapas
   - 9.4. Objetos
      - 9.4.1. Pociones
      - 9.4.2. Pergaminos
      - 9.4.3. Espadas
      - 9.4.4. Armaduras
      - 9.4.5. Llaves
   - 9.5. NPCs
      - 9.5.1. Comportamientos
   - 9.6. Interfaz
      - 9.6.1. MenÃºs
      - 9.6.2. Interfaz de partida
- 10. Conclusiones
- 11. BibliografÃ­a y referencias
- 12. Anexos
- Figura 5-1. Extreme Programming : en.wikipedia.org 3.2.Ãndice de figuras
- Figura 6-1. InterpretaciÃ³n de pÃ­xeles en modo 0 : http://www.cpcmania.com
- Figura 6-2. InterpretaciÃ³n de pÃ­xeles en modo 1 : http://www.cpcmania.com
- Figura 7-1. Captura del videojuego Battlezone : en.wikipedia.org
- Figura 7-2. Captura del videojuego Wayout : en.wikipedia.org
- Figura 7-3. Captura del videojuego Wolfenstein 3D : en.wikipedia.org
- Figura 7-4. Captura del videojuego Doom : doom.wikia.com
- Figura 7-5. Captura del videojuego Quake : quake.wikia.com
- Figura 8-1. Captura del algoritmo de raycasting en Unity
- Figura 8-2. DescripciÃ³n grÃ¡fica del raycast y las distancias entre celdas. : lodev.org
- Figura 8-3. Captura del renderer de raycasting funcionando en Amstrad
- Figura 8-4. MaquetaciÃ³n en GeoGebra
- Figura 8-5. Resultado final del maquetado en GeoGebra
- Figura 8-6. Ejemplo de transparencia con el renderer realizado
- Figura 8-7. Paredes laterales
- Figura 8-2. Esquema del funcionamiento del renderer
- Figura 8-8. Captura del renderer con texturizado de paredes.
- Figura 8-9. Ejemplos de entidades
- Figura 9-1. Diagrama del funcionamiento del generador de mapas
- Figura 9-2. Conjunto de texturas de la primera zona
- Figura 9-3. Conjunto de texturas de la segunda zona
- Figura 9-4. Conjunto de texturas de la tercera zona
- Figura 9-5. Conjunto de texturas de la Ãºltima zona
- Figura 9-6. PociÃ³n
- Figura 9-7. Pergamino
- Figura 9-8. Espada
- Figura 9-9. Armadura
- Figura 9-10. Llave
- Figura 9-11. Rata (enemigo)
- Figura 9-12. Limo (enemigo de la primera zona)
- Figura 9-13. Guardia (enemigo de la segunda zona)
- Figura 9-14. Calavera (enemigo de la tercera zona)
- Figura 9-15. Caballero (enemigo de la cuarta zona)
- Figura 9-16. Rey (enemigo final del juego)
- Figura 9-17. MenÃº principal
- Figura 9-18. MenÃº de cargar partida
- Figura 9-19. MenÃº de opciones
- Figura 9-20. Pantalla de crÃ©ditos
- Figura 9-21. MenÃº de partida
- Figura 9-22. MenÃº de inventario
- Figura 9-23. MenÃº de pausa
- Figura 9-24. MenÃº de guardar partida
- Figura 9-25. MenÃº de opciones
- Figura 9-26. Interfaz de partida
- Figura 9-27. Minimapa
- Figura 9-28. EstadÃ­sticas del jugador
- Figura 9-29. Registro de acciones
- Figura 9-30. BrÃºjula
- Figura 9-31. Ventana 3D


## 4. IntroducciÃ³n

### 4.1. TerminologÃ­a

En el documento se van a usar distintos tÃ©rminos, muchos de ellos abreviados para facilitar la

lectura del documento.

```
ï‚· Amstrad: Amstrad CPC 464, ordenador de 8 bits comercializado a partir de 1984 y
plataforma para la que se va a desarrollar el proyecto.
ï‚· HW o Hardware: componentes fÃ­sicos del ordenador.
ï‚· SW o Software: procesos que se ejecutan en el ordenador.
ï‚· CPU: Central Processing Unit, hardware encargado de interpretar las instrucciones
programadas.
ï‚· RAM: Random Access Memory, memoria sobre la que la CPU trabaja.
ï‚· Frame: Imagen mostrada por el ordenador en un momento dado.
ï‚· FPS: Frames per second, cantidad de imÃ¡genes que es capaz de mostrar el ordenador
por segundo.
ï‚· Bit: Binary Digit, unidad mÃ­nima de informaciÃ³n.
ï‚· Byte: Conjunto de 8 bits, conjunto mÃ­nimo de bits que se suele usar en programaciÃ³n.
ï‚· Buffer: Segmento de la RAM destinado a guardar datos para posterior uso.
ï‚· Render o renderizado: proceso de generaciÃ³n de una imagen a partir de datos
interpretados por el ordenador.
```
AdemÃ¡s, debido a la estructura de la CPU, se mostrarÃ¡n valores y nÃºmeros en base 2 y en base

16, la simbologÃ­a es la siguiente:

```
ï‚· 0x o #: Los nÃºmeros que empiecen con 0x o # se interpretarÃ¡n en base 16, ademÃ¡s la
cantidad de dÃ­gitos serÃ¡ mÃºltiplo de 2 (0x0F, 0x010F, 0x1F00).
ï‚· 0 b: Los nÃºmeros que empiecen con 0b se interpretarÃ¡n en base 2, ademÃ¡s la cantidad de
dÃ­gitos serÃ¡ generalmente 8 o mÃºltiplo de 8 (0b00010000, 0b10101111).
ï‚· El resto de nÃºmeros se interpretarÃ¡n en base 10.
```
Por ejemplo, 15 = 0x0F = 0b0000 1111.

### 4.2. Estructura del documento

El cuerpo del documento estÃ¡ dividido en 4 bloques diferenciados:

```
ï‚· Amstrad CPC 464: en este bloque se describen en detalle las caracterÃ­sticas del
ordenador para el que se va a desarrollar el proyecto y se enfatiza en aquellas que
puedan beneficiar o lastrar el desarrollo del renderer.
```

ï‚· TÃ©cnicas de renderizado 3D: aquÃ­ se listan y describen distintas tÃ©cnicas usadas para

```
renderizado de imÃ¡genes 3D en mÃ¡quinas de caracterÃ­sticas similares al Amstrad y se
nombran varios ejemplos reales de cada tÃ©cnica.
```
ï‚· Desarrollo del motor de renderizado: este bloque describe el proceso de desarrollo

```
del motor de renderizado, con las distintas iteraciones del desarrollo, los problemas
encontrados y las soluciones aplicadas.
```
ï‚· Desarrollo del juego: por Ãºltimo, en este bloque se describe el proceso de desarrollo

```
del juego de ejemplo y sus caracterÃ­sticas.
```

## 5. MetodologÃ­a

Puesto que se trata de un proyecto individual, no resulta necesario aplicar completamente una

metodologÃ­a de desarrollo, ya que Ã©stas estÃ¡n enfocadas al desarrollo en equipo. No obstante, el

uso de pautas seguidas por las metodologÃ­as Ã¡giles sigue siendo Ãºtil a pesar de trabajar solo.

Concretamente la metodologÃ­a en la que me he basado ha sido Extreme Programming, ya que

permite ciclos muy cortos de desarrollo y pruebas, lo cual es necesario para poder probar los

algoritmos implementados y modificarlos o sustituirlos completamente en caso de no ser

factibles en ejecuciÃ³n.

De esta manera, el desarrollo se hace en ciclos muy cortos de implementaciÃ³n y testeo para

poder comprobar que el algoritmo en desarrollo funciona correctamente o requiere de una

remodelaciÃ³n o cambio total.

```
Figura 5 - 1. Extreme Programming
: en.wikipedia.org
```
AdemÃ¡s, tambiÃ©n se usarÃ¡ un sistema de control de versiones para evitar la pÃ©rdida de datos y

para poder deshacer cambios en caso de ser necesario, en este caso se usarÃ¡ Git, ya que permite

un buen manejo de ficheros de texto y comprobar el historial de ediciones, asÃ­ como compara

los cambios de manera sencilla.


Durante el desarrollo se van a utilizar las siguientes herramientas:

```
ï‚· Notepad++: Editor de texto con resaltado de sintaxis en C.
```
```
ï‚· CPCtelera: LibrerÃ­a de funciones en ensamblador y C para desarrollar en Amstrad.
```
```
ï‚· Linux subsystem for Windows: Subsistema de Linux en Windows 10, incluye el
software necesario para compilar el proyecto.
```
```
ï‚· Arkos Tracker: Software de composiciÃ³n que permite exportar archivos de audio
compatibles con Amstrad.
```
```
ï‚· Gimp: Herramienta open source de ediciÃ³n de imÃ¡genes, se usarÃ¡ para la creaciÃ³n de
texturas del videojuego.
```
```
ï‚· WinAPE: Emulador de Amstrad, permite ejecutar software de Amstrad en los
ordenadores actuales.
```
```
ï‚· GeoGebra: Herramienta matemÃ¡tica grÃ¡fica que permite visualizar funciones y
geometrÃ­a 2D.
```

## 6. Amstrad CPC 464............................................................................................................

Para poner en contexto al lector y poder describir adecuadamente las caracterÃ­sticas del Amstrad

CPC 464, primero describirÃ© de forma breve la situaciÃ³n de los ordenadores domÃ©sticos de la

Ã©poca.

A principios de la dÃ©cada de los 80 muchas compaÃ±Ã­as entraron en el negocio de la

computaciÃ³n, esto llevÃ³ a una gran oferta de mÃ¡quinas asequibles que empezaron a entrar en el

Ã¡mbito domÃ©stico. Los ordenadores domÃ©sticos habÃ­an llegado.

En esta primera oleada de ordenadores domÃ©sticos se encontraban mÃ¡quinas como el Sinclair

ZX en 1880, el ZX Spectrum y el Commodore 64 en 1982 o el Amstrad CPC 464 en 1984.

Todos estos ordenadores tenÃ­an en comÃºn que utilizaban el procesador Z80, un procesador de 8

bits muy extendido en la dÃ©cada de los 80 debido a su bajo precio y la facilidad de replicarlo,

esto hizo que fuese el procesador por excelencia de la mayorÃ­a de ordenadores de la Ã©poca.

El Amstrad CPC 464 se trata de un ordenador domÃ©stico de 8 bits, con capacidad para mostrar

16 colores distintos de forma simultÃ¡nea en pantalla. Cuenta con un lector de casetes para la

carga de software y con una resoluciÃ³n mÃ¡xima de 64 0 pÃ­xeles de ancho por 200 de alto.

### 6.1. Hardware

#### 6.1.1. Procesador

El procesador del Amstrad, como se ha mencionado anteriormente, es un Zilog Z80 con una

frecuencia de 4 MHz. Pero debido a que comparte memoria con el circuito de video, su

frecuencia aproximada equivale a 3.3Mhz, ya que requiere sincronizarse con el reloj del chip

grÃ¡fico para evitar conflictos.

Debido a que se trata de un procesador de 8 bits, trabajar con tipos de datos mayores a un byte,

como enteros de 16 bits o nÃºmeros con coma flotante (32 bits), harÃ¡ que reduzca

considerablemente el rendimiento de renderer, por lo que se deben evitar el mÃ¡ximo posible.

#### 6.1.2. Memoria

La memoria RAM del Amstrad consta de 4 bloques de 16 kilobytes cada uno y es compartida

entre la CPU y el chip grÃ¡fico. Esto implica que de los 64 KB totales, una parte se debe reservar

para lo que se va a mostrar en pantalla.

Por defecto, la distribuciÃ³n de la memoria es la siguiente:

```
ï‚· Primer bloque: En los primeros 16 KB es donde se posiciona la ROM del firmware de
Amstrad, una vez ha iniciado se puede elegir entre leer de la ROM o de la RAM, pero
```

```
no se puede leer del primer bloque de la RAM si estÃ¡ activa la ROM. Esto trae
limitaciones como que si se estÃ¡ ejecutando cÃ³digo alojado en el primer bloque y se
invoca la ROM no tendremos acceso al cÃ³digo que se estaba ejecutando y la aplicaciÃ³n
tendrÃ¡ un comportamiento no deseado.
```
```
ï‚· Segundo bloque: Este bloque por defecto estÃ¡ vacÃ­o, por lo que se puede usar
libremente para almacenar datos y cÃ³digo.
```
```
ï‚· Tercer bloque: Este bloque contiene variables y funciones que utiliza el firmware de
Amstrad para funcionar, se puede sobrescribir si se deshabilita el firmware. TambiÃ©n se
almacena en este bloque la pila de llamadas, que crece desde la posiciÃ³n mÃ¡s alta hacia
la mÃ¡s baja.
```
```
ï‚· Cuarto bloque: Es el bloque usado por el chip de video para leer los datos que tiene
que mostrar en pantalla. Desde la posiciÃ³n #C000 hasta la #FE80 son datos que se verÃ¡n
en pantalla, tras la memoria de video quedan 384 bytes sobrantes debido a que el chip
grÃ¡fico usa un total de 16000 bytes.
```
#### 6.1.3. Video

El chip grÃ¡fico de Amstrad permite distintas configuraciones y modos grÃ¡ficos. Dispone de una

paleta de 27 colores, de los que se pueden escoger una cantidad distinta dependiendo del modo

grÃ¡fico.

_6.1.3.1.Modos de texto_

El Amstrad se puede usar en modo texto, en este modo permite 3 modos de texto distintos:

```
ï‚· 20x25 caracteres.
ï‚· 40x25 caracteres.
ï‚· 80x25 caracteres.
```
_6.1.3.2.Modos grÃ¡ficos_

```
ï‚· Modo 0: Tiene una resoluciÃ³n de 160 pÃ­xeles de ancho por 200 de alto, la relaciÃ³n de
aspecto de cada pÃ­xel es de 2:1 (coloquialmente conocido como pÃ­xel ladrillo por la
forma que tiene al ser el doble de ancho que de alto). Este modo permite utilizar hasta
16 colores simultÃ¡neamente.
ï‚· Modo 1: Tiene una resoluciÃ³n de 320 pÃ­xeles de ancho por 200 de alto, la relaciÃ³n de
aspecto es de 1:1. Permite usar hasta 4 colores simultÃ¡neos.
```

```
ï‚· Modo 2: Con una resoluciÃ³n de 640 pixeles de ancho por 200 de alto, este modo es el
que mÃ¡s resoluciÃ³n permite, su relaciÃ³n de aspecto es 1:2. Permite utilizar Ãºnicamente 2
colores simultÃ¡neos.
```
Es importante destacar que todos los modos utilizan la misma cantidad de memoria, lo que

cambia entre ellos es la forma de distribuirla, por lo que el tiempo que llevarÃ­a dibujar una

pantalla completa es el mismo. El modo 0 sacrifica resoluciÃ³n para obtener una mayor gama de

colores y el modo 2 hace lo contrario.

Teniendo en cuenta las caracterÃ­sticas de cada modo, el modo que se va a utilizar en el

proyecto es el modo 0, ya que permite mayor gama de colores y permitirÃ¡ diferenciar mayor

cantidad de elementos distintos en pantalla.

_6.1.3.3.InterpretaciÃ³n de la RAM_

El chip grÃ¡fico de Amstrad tiene una peculiar manera de interpretar los datos existentes en su

zona de la memoria RAM. En lugar de dibujar lÃ­neas consecutivas, que correspondan a la

memoria leÃ­da, dibuja la octava lÃ­nea posterior a la que acaba de dibujar. Es por esto que

cuando se escriba en la memoria de video hay que tener en cuenta que las imÃ¡genes se tienen

que modificar para seguir dicho patrÃ³n, no se pueden escribir de forma lineal en la memoria de

video.

AdemÃ¡s de cÃ³mo se interpretan las lÃ­neas de video tambiÃ©n hay que tener en cuenta cÃ³mo

interpreta Amstrad los pixeles en cada modo grÃ¡fico y como se reparten en cada byte.

Para el modo 0, un byte almacena la informaciÃ³n de 2 pixeles, 4 bits para cada pixel, y se

interpreta de la siguiente manera:

## Figura 6-1. InterpretaciÃ³n de pÃ­xeles en modo 0 : http://www.cpcmania.com

Para el modo 1, un byte almacena la informaciÃ³n de 4 pixeles, 2 bits para cada pixel, y se

interpreta de la siguiente manera:

## Figura 6-2. InterpretaciÃ³n de pÃ­xeles en modo 1 : http://www.cpcmania.com


Para el modo 2, un byte almacena la informaciÃ³n de 8 pÃ­xeles, 1 bit para cada pixel, en este

modo cada bit del byte corresponde con el pixel del grupo de 8 pixeles de forma lineal.


## 7. TÃ©cnicas de renderizado 3D

Las primeras tÃ©cnicas para mostrar imÃ¡genes 3D en videojuegos usaban pequeÃ±os trucos y
engaÃ±os para simular mundos 3D. A continuaciÃ³n, hay listados algunos videojuegos que
mostraban imÃ¡genes 3D del mundo que contenÃ­an y se van a comparar las caracterÃ­sticas de la
mÃ¡quina sobre la que se ejecutaban con las caracterÃ­sticas del Amstrad.

EstÃ¡n categorizados en funciÃ³n de si calculaban 3D real o simulaban el 3D.

### 7.1. 3D simulado

Los primeros juegos que mostraron mundos 3D se ejecutaban en mÃ¡quinas con poca potencia y
cuyas caracterÃ­sticas no permitÃ­an calcular la complejidad de un mundo 3D en tiempo real. Por
ello se usaron trucos y tÃ©cnicas que simulaban 3D.

#### 7.1.1. GrÃ¡ficos vectoriales

Los grÃ¡ficos vectoriales tenÃ­an la ventaja de que solo requerÃ­an dibujar las lÃ­neas de los
polÃ­gonos, esto permitÃ­a ahorrar muchos ciclos de cÃ¡lculo a la hora de mostrar una escena. Sin
embargo, la principal desventaja de este tipo de grÃ¡ficos es que no permite dibujar superficies
sÃ³lidas, Ãºnicamente las aristas de los objetos.

7.1.1.1.1.Battlezone (1980)

## Figura 7-1. Captura del videojuego Battlezone : en.wikipedia.org

Un ejemplo claro de este tipo de grÃ¡ficos es el Battlezone, como se puede observar en la captura
anterior, sus grÃ¡ficos son muy bÃ¡sicos y consisten Ãºnicamente en lÃ­neas.


#### 7.1.2. GrÃ¡ficos rasterizados

Los grÃ¡ficos rasterizados utilizan un rÃ¡ster, o matriz de pÃ­xeles, para mostrar las imÃ¡genes, este
es el mÃ©todo de dibujado que utiliza el Amstrad.

_7.1.2.1.Raycasting_

La tÃ©cnica de raycasting consiste en lanzar un rayo desde la posiciÃ³n del observador para cada
pixel de la pantalla y obtener la informaciÃ³n de la colisiÃ³n del rayo para determinar el color de
dicho pixel. Los mapas se basan en una matriz de celdas 2D. Es por ello que no se considera 3D
real, ya que no existen distintas alturas en los mundos de los juegos que usan esta tÃ©cnica, sÃ³lo
pueden recorrerse mapas planos.

7.1.2.1.1.Wayout (1982)

## Figura 7-2. Captura del videojuego Wayout : en.wikipedia.org

Se trata de un videojuego en primera persona desarrollado por Sirius Software y publicado para
la Atari 8-bit, el Apple II y el Commodore 64.

En este juego el jugador debe recorrer uno de los 27 laberintos que contiene el juego y encontrar
la salida con la ayuda de una brÃºjula y un minimapa.

Este es un buen ejemplo de renderer, ya que las especificaciones de las plataformas para las que
se publicÃ³ son similares a las del Amstrad.

Como se puede observar en la captura, los grÃ¡ficos son muy rudimentarios, la vista 3D ocupa
una fracciÃ³n de la pantalla y no cuenta con ningÃºn tipo de textura para los planos dibujados.


7.1.2.1.2.Wolfenstein 3D (1992)

## Figura 7-3. Captura del videojuego Wolfenstein 3D : en.wikipedia.org

Se trata de un juego de disparos en primera persona desarrollado por id Software para el sistema
operativo MSDOS.

AquÃ­ se puede observar la gran cantidad de elementos que estÃ¡ renderizando el juego en cada
frame, ademÃ¡s del texturizado de los elementos que aparecen.

Los requerimientos de este renderer estÃ¡n por encima de las capacidades del Amstrad, que por
las fechas en las que se publicÃ³ este juego ya llevaba 8 aÃ±os en el mercado.

_7.1.2.2.BSP_

Los BSP o ParticiÃ³n binaria del espacio es un mÃ©todo que subdivide de forma recursiva un
espacio en elementos convexos. Esta subdivisiÃ³n devuelve una estructura de datos que sirve
para representar la escena y el mundo virtual del videojuego.

Con esta tÃ©cnica se pueden calcular las salas y paredes que se van a renderizar, a diferencia del
raycasting, permite tener distintas alturas en el mapa y no requiere que las paredes se posicionen
en Ã¡ngulos rectos entre ellas (ya que los mapas no se basan en matrices de celdas), no obstante,
todavÃ­a no permite superposiciÃ³n de habitaciones y los mapas se siguen basando en informaciÃ³n
2D.


7.1.2.2.1.Doom (1993)

## Figura 7-4. Captura del videojuego Doom : doom.wikia.com

Es un juego de disparos en primera persona desarrollado por id Software para el sistema
operativo MSDOS.

Como se puede observar en la captura, muchas de las limitaciones que se tenÃ­an en los juegos
que usaban la tÃ©cnica de raycasting se han eliminado, como por ejemplo poder darle distintos
Ã¡ngulos a las paredes y distintas alturas al terreno.

Esta tÃ©cnica de renderizado tiene unos requerimientos muy superiores a las capacidades del
Amstrad.

### 7.2. 3D real

A partir de 1996 las capacidades de los ordenadores domÃ©sticos y personales habÃ­an avanzado
lo suficiente como para poder generar y calcular mundos 3D reales. Ya no se trataba de mapas
2D que se interpretaban como mundos 3D.

De esta manera se pudo avanzar considerablemente en el diseÃ±o de videojuegos, ya no se tenÃ­an
las limitaciones de superposicionamiento de salas y se podÃ­an utilizar mallas poligonales para
los objetos y entidades que saliesen en pantalla.


_7.2.1.1.Quake (1996)_

## Figura 7-5. Captura del videojuego Quake : quake.wikia.com

Desarrollado por id Software y publicado para MSDOS y Microsoft Windows.

Quake fue el primer videojuego con 3D real que se publicÃ³.


## 8. Desarrollo del motor de renderizado

Para el desarrollo del motor de renderizado usÃ© como base el algoritmo de raycasting utilizado
en videojuegos como Wolfenstein 3D. Este algoritmo permitirÃ­a crear mapas con paredes
sÃ³lidas y texturizadas.

El principal problema a abordar fue que el algoritmo estÃ¡ diseÃ±ado para ordenadores con una
capacidad de cÃ³mputo mucho mayor que el Amstrad, por lo que tuve que realizar
optimizaciones y recortes en sus caracterÃ­sticas.

### 8.1. MaquetaciÃ³n inicial del algoritmo

Para empezar, decidÃ­ implementar de forma rÃ¡pida el algoritmo en un motor de videojuegos
actual (Unity), esto me permitirÃ­a comprobar que el algoritmo inicial da los resultados esperados
y tambiÃ©n me permitirÃ­a hacer modificaciones rÃ¡pidas y comprobar resultados de manera mÃ¡s
eficiente.

## Figura 8-1. Captura del algoritmo de raycasting en Unity

Las bases y las referencias del algoritmo las obtuve de un tutorial escrito por Lode Vandevenne,
en este tutorial explica las bases del renderer y su implementaciÃ³n.

Con ello hice la primera implementaciÃ³n en Unity, creando un renderer de raycast sin texturas.

El algoritmo funciona de la siguiente manera:

Para cada pixel de la pantalla, el algoritmo lanza un rayo desde la posiciÃ³n del jugador. La
direcciÃ³n del rayo se calcula en funciÃ³n de la obertura de la cÃ¡mara y de la columna de pÃ­xeles
que se estÃ© dibujando.

rayDir.x = camera.transform.forward.x - ((camera.transform.forward.z *
camPlaneMag) * currCamScale);


rayDir.y = camera.transform.forward.z + ((camera.transform.forward.x *
camPlaneMag) * currCamScale);

#### En esta secciÃ³n de cÃ³digo, la variable camPlaneMag corresponde con la obertura de la cÃ¡mara,

y currCamScale es la posiciÃ³n normalizada de la columna que se estÃ¡ dibujando actualmente.
El resultado es la direcciÃ³n del rayo en el plano XY, ya que no es necesario calcular en el eje Z

#### porque el mapa es una matriz bidimensional.

A continuaciÃ³n, se calcula la distancia que recorre el rayo para alcanzar la siguiente celda, tanto
en vertical como en horizontal.

float deltaDistX = Mathf.Sqrt( 1 + (rayDir.y * rayDir.y) / (rayDir.y *
rayDir.x));
float deltaDistY = Mathf.Sqrt( 1 + (rayDir.x * rayDir.x) / (rayDir.y *
rayDir.y));

## Figura 8-2. DescripciÃ³n grÃ¡fica del raycast y las distancias entre celdas. : lodev.org

Con esas distancias se va recorriendo la matriz paso a paso desde el punto de origen y
comprobando en cada paso el valor de la celda.

En caso de que la celda contenga un valor correspondiente a una pared, se dibuja la columna
actual con el color de la pared, teniendo en cuenta su distancia al origen.

Para calcular la altura en pixeles de la pared en la columna que se estÃ¡ dibujando se divide la
altura del renderer (en pixeles) entre la distancia a la que estÃ¡ la pared y se centra en altura.

float lineHeight = wallDist < 1? h : h / (wallDist);
float startY = h / 2 - lineHeight / (2.0f);

Una vez calculada la altura y el color, se dibuja la columna de pixeles.


void verLine(int x, int y0, int y1, Color c)
{
for (int j = 0 ; j < y0; j++)
{
texture.SetPixel(x, j, Color.gray);
}
for (int j = y0; j < y1; j++)
{
texture.SetPixel(x, j, c);
}

for (int j = y1; j < h; j++)
{
texture.SetPixel(x, j, Color.black);
}
}
En este caso se estÃ¡ usando gris para el suelo y negro para el cielo, el parÃ¡metro de color que se
pasa es el recogido por el rayo al colisionar con una celda de pared.

Como se puede observar, este algoritmo lanza Ãºnicamente un rayo por columna del renderizado,
por lo que aumentar la resoluciÃ³n en horizontal harÃ¡ que el renderizado sea mucho mÃ¡s costoso.

Una vez probado e implementado en Unity, adaptÃ© el algoritmo a C para probarlo en Amstrad.

### 8.2. Primera implementaciÃ³n

## Figura 8-3. Captura del renderer de raycasting funcionando en Amstrad

La primera implementaciÃ³n del renderer fue una adaptaciÃ³n directa del cÃ³digo escrito para las
pruebas de Unity.

Para mostrarlo en pantalla, el frame resultante del renderer se guardaba en un buffer en la
posiciÃ³n de memoria 0x0040.

Con una resoluciÃ³n de 80 pÃ­xeles de ancho por 100 de alto en modo 0, la imagen resultante del
renderer era de 4000 bytes.


Para mostrar ese resultado en pantalla implementÃ© una funciÃ³n que leÃ­a 4000 bytes a partir de la
posiciÃ³n 0x0040 y los copiaba en la memoria de video adaptÃ¡ndolos para que el chip grÃ¡fico los
interpretara de forma correcta.

void Render(){
u8 x ,y;
u8* lineMem;
u8* linePos = (u8*)SCREEN_TEXTURE_BUFFER;
for(y=0;y<SCREEN_TEXTURE_HEIGHT;++y){
lineMem = CPCT_VMEM_START + ((y&7) *0x0800) + ((y>>3)*0x0050);
for(x=0;x<SCREEN_TEXTURE_WIDTH_BYTES;++x){

*(u8*)lineMem = *(u8*)linePos;
++lineMem;
++linePos;
}
}
cpct_drawCharM0(CPCT_VMEM_START,
5,1,directionsChar[directionIndex>>1]);
}
La funciÃ³n calcula la posiciÃ³n de memoria inicial de cada fila en la memoria de video y copia de
forma secuencia los bytes.

Como se puede observar en la imagen que encabeza esta secciÃ³n, el algoritmo funciona y
renderiza mediante raytracing el mapa de ejemplo usado.

Sin embargo, existen varios problemas importantes con este algoritmo:

```
ï‚· El uso de tipos de datos mayores a 1 byte: el algoritmo usa muchas variables de 16 bits
y de coma flotante de 32 bits, esto hace que el rendimiento caiga drÃ¡sticamente en el
Amstrad, ya que el procesador es de 8 bits.
ï‚· El rendimiento general del renderer es pÃ©simo, consigue dibujar 1 frame cada 10
segundos. Por lo que es totalmente inviable para usar en un videojuego.
ï‚· Por Ãºltimo, se trata del renderer mÃ¡s bÃ¡sico, solo renderiza con colores planos, por lo
que no se pueden meter detalles en las paredes como se podrÃ­a hacer con texturas.
```
Debido a estos problemas decidÃ­ rediseÃ±ar el algoritmo manteniendo algunas caracterÃ­sticas que
tenÃ­a este.

### 8.3. RediseÃ±o del algoritmo y maquetaciÃ³n

Para el rediseÃ±o del algoritmo decidÃ­ fijar que limitaciones le iba a imponer al renderer y que
requisitos deberÃ­a tener.

Para empezar, el renderer deberÃ­a funcionar a una velocidad suficiente como para que el juego
no se volviera aburrido. No deberÃ­a ser necesario que renderizase para juegos a tiempo real, con
que sirviera para juegos por turnos serÃ­a suficiente.

Segundo, el renderer deberÃ­a poder dibujar texturas en las paredes para poder darle mÃ¡s
calidad a los escenarios. Esto implica que ademÃ¡s de calcular la distancia para cada columna de
render, tambiÃ©n se debe calcular la altura para la textura.

Tercero, para mejorar el rendimiento y poder optimizar, el renderer deberÃ­a estar fijado a 4
direcciones correspondientes con los puntos cardinales, asÃ­ como a una posiciÃ³n por celda del


mapa. De esta manera no es necesario usar nÃºmeros con coma flotante y se pueden hacer los
cÃ¡lculos con enteros.

Con estos requisitos y limitaciones me di cuenta de que se podÃ­a calcular las paredes que tenÃ­a
delante y dibujarlas sin necesidad de lanzar rayos.

Ãšnicamente necesitaba listar de forma ordenada las celdas que habÃ­a en el cono de visiÃ³n del
personaje y fijar un valor de reducciÃ³n del tamaÃ±o por distancia.

Para maquetar el renderer utilicÃ© GeoGebra debido a que permite crear geometrÃ­a 2D y
visualizarla de forma sencilla y realizar cÃ¡lculos geomÃ©tricos rÃ¡pidamente.

## Figura 8-4. MaquetaciÃ³n en GeoGebra

Usando GeoGebra visualicÃ© rÃ¡pidamente las proporciones de las filas de celdas y la profundidad
mÃ¡xima de filas que deberÃ­an aparecer en el renderer.

FijÃ© la profundidad mÃ¡xima en 5 filas desde la posiciÃ³n del personaje hacia el horizonte y la
reducciÃ³n en tamaÃ±o de una fila a la siguiente en Â½ (cada fila consecutiva se ve Â½ de alta que la
anterior).


## Figura 8-5. Resultado final del maquetado en GeoGebra

El resultado final del maquetado permite observar una simulaciÃ³n del renderer y comprobar que
las proporciones son adecuadas.

Cada â€œbloqueâ€ de paredes en el maquetado corresponde a unas coordenadas (X y Z en la
captura) que corresponden a su posiciÃ³n horizontal en la pantalla y su profundidad en filas.

### 8.4. Segunda implementaciÃ³n

BasÃ¡ndome en la maquetaciÃ³n realizada en GeoGebra, iniciÃ© la implementaciÃ³n en C del
renderer.

El renderer funcionarÃ­a sobre un mapa plano, basado en una matriz bidimensional de celdas
donde cada celda tiene un identificador de suelo o pared.

Lo primero que necesitaba era una funciÃ³n que me crease un array de las celdas que hay dentro
del cono de visiÃ³n del personaje.

El cono de visiÃ³n del personaje es estÃ¡tico en tamaÃ±o, Ãºnicamente cambia la orientaciÃ³n en
Ã¡ngulos de 90Âº, por lo que es sencillo obtener las celdas que entran dentro.

Usando la maquetaciÃ³n realizada anteriormente se pueden obtener las medidas del cono de
visiÃ³n, siendo las siguientes en cantidad de celdas por fila y de mÃ¡s lejos a mÃ¡s cerca:
33,17,9,5,3,1.

Como se puede observar, la cantidad de celdas por fila sigue un patrÃ³n:

nActual = (nAnterior-1)/2 + 1;
AdemÃ¡s, a esos valores hay que sumar 2, por las celdas que, a pesar de quedar fuera por cada
extremo, se les puede ver la pared lateral. TambiÃ©n se debe tener en cuenta que las celdas estÃ¡n


centradas en el cono de visiÃ³n, por lo que al seleccionarlas de la matriz del mapa hay que tener
en cuenta el offset que tienen delante.

Es por ello que para implementar la funciÃ³n que devuelve el array de celdas en el cono de
visiÃ³n, he usado una lista de offsets que sirven a la vez para calcular la cantidad de celdas de
cada fila que hay en el cono de visiÃ³n.

const u8 offsets_cells_in_view[5]={
8,12,14,15,16
};
Ese offset se usa en un bucle que se encarga de aÃ±adir las celdas de cada fila al array:

for(i=offset;i<35-offset;++i)
Con esta implementaciÃ³n el valor i va a recorrer la cantidad necesaria con el offset necesario en
cada fila produciendo el siguiente cono de visiÃ³n:

*********************************** * = celdas dentro de visiÃ³n
Â·Â·Â·Â·Â·Â·Â·Â·*******************Â·Â·Â·Â·Â·Â·Â·Â· Â· = celdas fuera de visiÃ³n
Â·Â·Â·Â·Â·Â·Â·Â·Â·Â·Â·Â·***********Â·Â·Â·Â·Â·Â·Â·Â·Â·Â·Â·Â·
Â·Â·Â·Â·Â·Â·Â·Â·Â·Â·Â·Â·Â·Â·*******Â·Â·Â·Â·Â·Â·Â·Â·Â·Â·Â·Â·Â·Â·
Â·Â·Â·Â·Â·Â·Â·Â·Â·Â·Â·Â·Â·Â·Â·*****Â·Â·Â·Â·Â·Â·Â·Â·Â·Â·Â·Â·Â·Â·Â·
Â·Â·Â·Â·Â·Â·Â·Â·Â·Â·Â·Â·Â·Â·Â·Â·***Â·Â·Â·Â·Â·Â·Â·Â·Â·Â·Â·Â·Â·Â·Â·Â·
P
Esa misma funciÃ³n ya se encarga de tener en cuenta la direcciÃ³n en la que estÃ¡ mirando el
personaje y rotar el cono de visiÃ³n hacia dicha direcciÃ³n.

Una vez obtenido el array de celdas a dibujar, el dibujado es sencillo. Se recorre el array y se
dibujan las celdas de lejos a cerca teniendo en cuenta las proporciones obtenidas durante la
maquetaciÃ³n.

Dibujar de lejos a cerca permite incluir una caracterÃ­stica al renderer que con la tÃ©cnica de
raycasting no era posible incluir: se pueden usar transparencias en las paredes para poder ver
que hay detrÃ¡s de ellas.


## Figura 8-6. Ejemplo de transparencia con el renderer realizado

TambiÃ©n el hecho de dibujar de lejos a cerca conlleva que el renderer tenga que dibujar 6
veces para generar un frame, una vez por cada fila dibujada. Pero a pesar de ello, el rendimiento
respecto al raycast es mayor, debido principalmente a la ausencia de tipos de datos mayores a
un byte. La funciÃ³n de renderizado funciona completamente con enteros de 1 byte, por lo que el
procesador solo necesita un ciclo para cada operaciÃ³n que realice.

El funcionamiento del renderer es el siguiente:

Empieza por la fila mÃ¡s alejada del personaje y calcula la cantidad de pixeles en ancho que
ocupa una celda.

A continuaciÃ³n, empieza a dibujar usando el array de celdas que existen en dentro del cono de
visiÃ³n previamente calculado.

Siempre tiene en cuenta si la celda anterior tenia pared o estaba vacÃ­a para tener en cuenta si
tiene que dibujar alguna pared lateral en los laterales de la celda actual.


## Figura 8-7. Paredes laterales

La imagen anterior ilustra la situaciÃ³n, en el centro se puede observar una celda vacÃ­a rodeada
de celdas con paredes. El renderer va de izquierda a derecha dibujando y siempre tiene en
cuenta si la anterior celda fue pared para dibujar los laterales, que en este caso son azules.

Cuando ha acabado de dibujar una fila, recalcula el tamaÃ±o en pixeles de cada celda para la
nueva fila y vuelve a empezar de izquierda a derecha. Lo repite hasta acabar la fila que el
personaje tiene delante.

Para cada columna de pixeles utiliza el ancho de cada celda para la altura. Y para dibujar la
columna se usa la misma funciÃ³n que con el renderer de raycasting, se dibujan el suelo y el cielo
y se dibuja de arriba hacia abajo la parte que corresponde a la celda.


```
Inicio
```
```
Pintar el suelo y el cielo que hay en el cono Obtener las celdas
de visiÃ³n
```
```
profundidad Fijar la
en filas a 6
```
```
Comprobar si la
celda anterior a la primera de la fila
actual es pared
```
```
cantidad de Fijar la
celdas en la
fila actual
```
```
Se ha acabado
de dibujar la celda que
estamos
dibujando?
```
```
No
```
```
La celda anterior era pared? No La celda es una pared?
```
```
Si siguiente celdaObtenemos la
```
```
Obtenemos la
primera celda de la fila
```
```
Si
Calcular la altura de
la pared de la celda en funciÃ³n de la
profundidad
```
```
Si
```
```
la pared lateral de la Calcular la altura de
celda anterior
```
```
Dibujar columna de pixeles del frame
```
```
Era la ultima columna de
pixeles del frame?
```
```
Si
```
```
Era la fila mÃ¡s
cercana al jugador?
```
```
Si
```
```
Fin del renderizado
```
```
No siguiente columna Avanzar a la de pixeles
```
Avanzar una fila No

## Figura 8-2. Esquema del funcionamiento del renderer


### 8.5. Texturizado

El siguiente paso fue incluir texturizado a las paredes.

Para ello decidÃ­ usar texturas de 32x32 pixeles, puesto que con esa resoluciÃ³n ya se pueden
conseguir detalles interesantes en las paredes.

Para el texturizado, modifiquÃ© la funciÃ³n encargada de dibujar cada columna del frame para que
dibujase un color extraÃ­do de la textura asociada a la pared en lugar de dibujar un color plano en
la zona correspondiente de dicha la pared.

El mapeado de texturas es muy sencillo, cada celda tiene un ID asociado a una textura, por lo
que todas las paredes de dicha celda tendrÃ¡n la misma textura asociada.

Para obtener el color durante el renderizado, la funciÃ³n de dibujado de columna obtiene un
parÃ¡metro que le indica la columna de la textura actual y la fila la calcula usando la altura en
pixeles de la pared para esta columna del frame. Sabiendo la altura de la pared y de la textura se
calcula para cada pixel del frame que color de la textura usar.

Para evitar usar nÃºmeros con coma flotante, en lugar de calcular la nueva posiciÃ³n en cada
pixel, se calcula la diferencia que hay que sumar y se hace un cÃ¡lculo acumulativo, de manera
que cada vez que se dibuja un pixel se suma una cantidad entera a la posiciÃ³n anterior.

Para la transparencia se usa un color especial, el magenta. Todos los pixeles de color magenta
se tratan como transparentes y, por lo tanto, no se dibujan.

## Figura 8-8. Captura del renderer con texturizado de paredes.


El siguiente paso es incluir entidades distintas a paredes y que el renderer pueda dibujarlas.

### 8.6. InclusiÃ³n de entidades

Para la inclusiÃ³n de entidades distintas a paredes en el renderer simplemente se tiene que aÃ±adir
mÃ¡s identificadores que pueda interpretar el renderer.

La principal diferencia entre las entidades y las celdas con paredes, es que las entidades no
tienen profundidad, por lo que el renderer no necesita tener en cuenta si la celda anterior tenÃ­a
una entidad para dibujar el lateral.

AdemÃ¡s de eso, implementÃ© 2 funciones distintas para los distintos tipos de entidades debido a
que sus texturas tienen un tamaÃ±o distinto al de las paredes. Esto se podrÃ­a haber hecho
modificando la funciÃ³n original de dibujado para que admitiera distintos tamaÃ±os, pero eso
acarrearÃ­a un mayor coste computacional para el dibujado, y siendo una funciÃ³n que se ejecuta
mÃºltiples veces durante el dibujado de un frame es conveniente reducir el coste computacional a
costa de mayor tamaÃ±o en memoria.

Las entidades se dividen en 2 tipos, objetos y enemigos, cada tipo tiene un tamaÃ±o de textura
distinto:

```
ï‚· Los objetos usan texturas de 16x16 pixeles.
ï‚· Los enemigos usan texturas de 24x24 pixeles.
```
A pesar de tener un tamaÃ±o de textura menor, la funciÃ³n de dibujado sigue considerando el
ancho de la celda de 32 pixeles, por lo que no empezarÃ¡ a dibujar a la entidad hasta pasados
unos pixeles. De esta manera se consigue que las entidades sean mÃ¡s pequeÃ±as que las paredes y
no ocupen todo el ancho de la celda.


## Figura 8-9. Ejemplos de entidades

### 8.7. Resultado final del renderer

El resultado final del renderer es bastante satisfactorio. La velocidad de renderizado final estÃ¡
entre 1 y 2 FPS, suficiente como para poder usarlo en videojuegos por turnos.

#### 8.7.1. CaracterÃ­sticas

La implementaciÃ³n final del renderer tiene caracterÃ­sticas interesantes que no se podÃ­an
conseguir usando un renderer de raycasting en una mÃ¡quina con estas caracterÃ­sticas, como la
transparencia o la texturizaciÃ³n de las paredes.

#### 8.7.2. Limitaciones

Las limitaciones del renderer son notorias, no permite tener libertad de movimiento ni de
rotaciÃ³n, el personaje estÃ¡ limitado a moverse de celda en celda y rotar en intervalos de 90Âº.
AdemÃ¡s, debido al limitado framerate, limita el tipo de juegos que lo pueden usar a ser por
turnos.


## 9. Juego de ejemplo

Para demostrar el funcionamiento del renderer creado, desarrollÃ© un videojuego que usase todas
sus caracterÃ­sticas.

### 9.1. DiseÃ±o

Teniendo en cuenta las caracterÃ­sticas y limitaciones del renderer, debÃ­a hacer un juego por
turnos y hacer uso de objetos y enemigos.

Un dungeon crawler es perfecto para las caracterÃ­sticas del renderer. Los dungeon crawler son
un tipo de juego en el que el jugador debe recorrer una mazmorra (normalmente generada
aleatoriamente) buscando objetos y enfrentÃ¡ndose a enemigos para poder avanzar.

Puesto que el juego iba a servir como demostraciÃ³n de las caracterÃ­sticas del motor, diseÃ±Ã© todo
entorno a dichas caracterÃ­sticas.

Los mapas del juego se crean a partir de un algoritmo aleatorio, de manera que cada partida que
se juega es distinta. AdemÃ¡s, una partida completa consta de 32 niveles distintos divididos en 4
zonas temÃ¡ticas distintas, cada zona usa un conjunto de texturas y colores para el mapa y los
enemigos.

El juego tambiÃ©n tiene un sistema de guardado y cargado de partidas, para evitar tener que
jugar los 32 niveles seguidos.

El diseÃ±o de las texturas y sprites, se encargÃ³ de realizarlo Alejandro Padilla Lozoya.
AdecuÃ¡ndolos a las limitaciones tÃ©cnicas del renderer y del Amstrad.

La mÃºsica la compuso Carlos Blaya Cases, usando el software Arkos Tracker.

### 9.2. Estructura del motor del juego

El motor del juego es una mÃ¡quina de estados, cada estado representa una parte distinta del
videojuego.

La mayor parte de los estados son los distintos menÃºs del juego, ademÃ¡s tambiÃ©n hay un estado
para la pantalla de carga y un estado â€œen partidaâ€.

Todos los estados comparten una misma estructura y el motor solo tiene que conocerla para
poder llamar a las funciones de cualquier estado, de esta manera se facilita la creaciÃ³n e
inclusiÃ³n de nuevos estados.

Todo el juego estÃ¡ dirigido por eventos de menÃºs, incluso dentro de la partida el jugador maneja
el juego seleccionando elementos del menÃº de la interfaz, de esta manera se evita que haga
acciones inintencionadas en caso de que una acciÃ³n tarde mÃ¡s de lo debido.


### 9.3. Algoritmo de generaciÃ³n de mapas

```
Inicio
```
```
Determinar celda inicial, asignarle
aÃ±adirla al stacktipo suelo y
```
```
tratar Celdas por = X*Y-
1
```
```
Quedan celdas por tratar?
```
```
No
```
```
Fin
```
```
Si Hay paredes?
```
```
Si
```
```
pared con suelo Buscar primera
adyacente
```
```
Convertir a suelo y quitar de la lista
*
```
```
No Quedan celdas en el stack?
No
```
```
Si
```
```
Obtener primera celda del stack y
comprobar su tipo
```
```
tipo de celdaSe conoce el? No Asignarle tipo*
```
```
Se trata de suelo?
Si
adyacentes de AÃ±adir celdas
tipo desconocido al stack
```
```
No
AÃ±adir celda a la lista de paredes
```
```
Celdas por tratar se
reduce en 1
```
```
Lista de paredes
vacia
```
```
el stackCeldas en : 1 Celdas en la lista de
aumenta en paredes 1
```
```
el stack se Celdas en
reduce en 1
Si
```
```
Celdas en el stack
entre aumenta 0 y 4
```
```
Celdas en la lista de
paredes se reduce en
1
```
```
*Asignar tipo en funciÃ³n de la
celdas tratadas cantidad de
subgrupos de para crear
celdas*
```
```
puerta y asignar *Convertir a
nuevo grupo a las siguientes celdas
a tratar*
```
## Figura 9-1. Diagrama del funcionamiento del generador de mapas

El generador de mapas empieza creando las paredes externas del mapa y a continuaciÃ³n
selecciona una posiciÃ³n aleatoria del mapa para empezar la generaciÃ³n. Esa primera posiciÃ³n se
usa tambiÃ©n como punto de inicio para el jugador.

A partir de ahÃ­ el generador va analizando las celdas contiguas y aÃ±adiendo a un stack las que
todavÃ­a no han sido tratadas, para posteriormente ir tratÃ¡ndolas una a una y asignÃ¡ndoles suelo o
pared. En caso de que la celda que estÃ¡ tratando sea una pared se aÃ±ade a un stack aparte para
procesar las paredes (para evitar que el mapa acabe con zonas separadas).

Este paso se repite hasta que no quedan celdas en el stack de celdas por procesar.

Esto genera un mapa de estilo laberÃ­ntico con algunas zonas abiertas y con una distribuciÃ³n
ligeramente caÃ³tica, pero sin desaprovechar ninguna parte del mapa.

Para evitar que los mapas se volvieran monÃ³tonos al avanzar con el juego, existen 4 conjuntos
distintos de paletas y texturas que se usan con los mapas y los NPC.

Cada conjunto se utiliza durante 8 mapas seguidos y despuÃ©s se cambia al siguiente conjunto.

Las texturas utilizadas para cada conjunto son las siguientes:

## Figura 9-2. Conjunto de texturas de la primera zona


## Figura 9-3. Conjunto de texturas de la segunda zona

## Figura 9-4. Conjunto de texturas de la tercera zona

## Figura 9-5. Conjunto de texturas de la Ãºltima zona

### 9.4. Objetos

Por los mapas aparecen repartidos objetos que el jugador puede usar para mejorar su personaje o
para salir de situaciones complicadas.

AdemÃ¡s de los objetos que hay en el mapa, los enemigos pueden soltar objetos al morir.

#### 9.4.1. Pociones

## Figura 9-6. PociÃ³n

La pociÃ³n sirve para que el jugador recupere parte de la salud perdida. Se puede usar desde el
menÃº de inventario.


#### 9.4.2. Pergaminos

## Figura 9-7. Pergamino

El pergamino permite al jugador huir rÃ¡pidamente de una situaciÃ³n complicada, ya que al usarse
teletransporta al jugador a una posiciÃ³n aleatoria del mapa. Se puede usar desde el menÃº de
inventario.

#### 9.4.3. Espadas

## Figura 9-8. Espada

Las espadas que el jugador encuentra por el mapa permiten que pueda ir mejorando a su
personaje y poder infringir mÃ¡s daÃ±o a los enemigos. Cada espada tiene un valor aleatorio de
daÃ±o asociado, Ã©ste siempre serÃ¡ mayor que el daÃ±o actual y estarÃ¡ dentro de un rango
dependiente del nivel del juego en el que se encuentre.

#### 9.4.4. Armaduras

## Figura 9-9. Armadura

Las armaduras permiten al jugador mejorar su defensa frente a los ataques de los enemigos.
Todas las armaduras que el jugador encuentre son iguales o mejores que la que lleva
actualmente, y la mejora que otorga siempre estÃ¡ dentro de un rango que depende del nivel en el
que se encuentre.


#### 9.4.5. Llaves

## Figura 9-10. Llave

La llave se trata del objeto mÃ¡s importante de cada nivel, es el objeto que necesita el jugador
para poder avanzar al siguiente nivel.

Una vez encontrada la llave se debe encontrar la puerta de salida que lleva al siguiente nivel.

### 9.5. NPCs

Los enemigos que el jugador se puede encontrar escalan en dificultad con el avance del jugador
en el juego.

Para cada zona existen 2 tipos de enemigos con comportamientos diferenciados, dependiendo
del comportamiento el jugador debe afrontarlos de una manera u otra.

#### 9.5.1. Comportamientos

En un principio se programaron 4 tipos distintos de comportamiento, pero debido al poco
espacio disponible en la memoria del Amstrad se tuvo que reducir a 2 tipos distintos.

_9.5.1.1.Pasivo_

Los enemigos con el comportamiento pasivo ignoraran al jugador cuando lo vean. Pero en caso
de que el jugador les ataque, Ã©stos se volverÃ¡n agresivos y atacarÃ¡n al jugador.

En cuanto los enemigos con este comportamiento se encuentran dÃ©biles tratarÃ¡n de huir del
jugador.

El enemigo que sigue este comportamiento en el juego es la rata, que aparece en todos los
niveles.

## Figura 9-11. Rata (enemigo)


_9.5.1.2.Agresivo_

Los enemigos agresivos no dudarÃ¡n en atacar y perseguir al jugador en el momento en que lo

tengan a la vista.

Son enemigos muy insistentes que no cesan en intentar matar al jugador y al contrario que los

enemigos pasivos, no tratarÃ¡n de huir cuando estÃ©n dÃ©biles.

Hay un tipo de enemigo por cada zona que sigue este comportamiento.

## Figura 9-12. Limo (enemigo de la primera zona)

## Figura 9-13. Guardia (enemigo de la segunda zona)

## Figura 9-14. Calavera (enemigo de la tercera zona)


## Figura 9-15. Caballero (enemigo de la cuarta zona)

## Figura 9-16. Rey (enemigo final del juego)

### 9.6. Interfaz

La interfaz del juego estÃ¡ principalmente compuesta de menÃºs, ya que todo el juego se controla
mediante elementos de menÃº.

#### 9.6.1. MenÃºs

_9.6.1.1.MenÃº principal_

Desde el menÃº principal se puede empezar nueva partida, acceder al menÃº de opciones, cargar
una partida guardada o acceder a la pantalla de crÃ©ditos.


## Figura 9-17. MenÃº principal

9.6.1.1.1.Nueva partida

Permite empezar una nueva partida del juego, se empieza en el nivel 1 con un nuevo personaje.

9.6.1.1.2.Cargar partida

Permite cargar una partida previamente guardada. Para cargar la partida se debe introducir una
cadena de caracteres vÃ¡lida. En caso de no ser vÃ¡lida no cargarÃ¡ nada.

Para la comprobaciÃ³n, el juego aplica una mÃ¡scara binaria a la cadena introducida y hace una
verificaciÃ³n de suma. Al resultado de la suma se le aplica otra mÃ¡scara binaria y se compara con
un fragmento de la cadena. Si coincide es que la cadena introducida es vÃ¡lida.

u8 savegame_checksave(){
u8 i = SAVEDATA_SIZE-1;
u8 checksum=0;
while(i){
--i;
checksum+=(saveArray[i]^SAVE_MASK);
}
checksum=checksum^CHECKSUM_MASK^SAVE_MASK;
return (checksum==save.checksum);
}
En el cÃ³digo, la variable save y la variable saveArray apuntan a los mismos datos.


## Figura 9-18. MenÃº de cargar partida

9.6.1.1.3.Opciones

En el menÃº de opciones se puede cambiar la configuraciÃ³n de la mÃºsica y de las texturas.
Pueden activarse y desactivarse en cualquier momento o desde el menÃº de opciones del menÃº
principal.


## Figura 9-19. MenÃº de opciones

9.6.1.1.4.CrÃ©ditos

La pantalla de crÃ©ditos muestra los crÃ©ditos del juego.


## Figura 9-20. Pantalla de crÃ©ditos

_9.6.1.2.MenÃº de partida_

El menÃº de partida lista las acciones que puede hacer el jugador durante su turno y tambiÃ©n da
acceso a los menÃºs de inventario y de pausa.

## Figura 9-21. MenÃº de partida

Las acciones de cada botÃ³n son las siguientes:

```
ï‚· BotÃ³n de acciÃ³n: Permite realizar una acciÃ³n que dependerÃ¡ de la situaciÃ³n en la que
estÃ© el jugador (atacar si tiene delante a un enemigo o recoger si es un objeto)
ï‚· Botones de movimiento: Permiten al jugador avanzar o girarse.
ï‚· BotÃ³n de espera: Permite que el jugador pase su turno, esto harÃ¡ a todos los enemigos
avanzar un turno.
ï‚· BotÃ³n de inventario: Permite al jugador acceder a su inventario.
ï‚· BotÃ³n de pausa: Permite pausar el juego y acceder al menÃº de pausa.
```

9.6.1.2.1.MenÃº de inventario

## Figura 9-22. MenÃº de inventario

El menÃº del inventario permite al jugador utilizar una pociÃ³n o un pergamino, siempre que
tenga unidades disponibles. El uso de uno de estos objetos hace que el turno del jugador acabe.

9.6.1.2.2.MenÃº de pausa

## Figura 9-23. MenÃº de pausa

En el menÃº de pausa el jugador puede modificar las opciones del juego, guardar su progreso y
salir de la partida o directamente salir al menÃº principal sin guardar.

Si el jugador decide guardar partida, aparecerÃ¡ en pantalla una cadena de texto que el jugador
debe apuntar y que serÃ¡ la que deba introducir en el menÃº de cargar partida.


## Figura 9-24. MenÃº de guardar partida

_9.6.1.3.MenÃº de opciones_

El menÃº de opciones del menÃº de pausa ofrece las mismas opciones que aparecen en el menÃº
principal. Se pueden activar y desactivar tanto la mÃºsica como las texturas.

## Figura 9-25. MenÃº de opciones


#### 9.6.2. Interfaz de partida

## Figura 9-26. Interfaz de partida

La interfaz de la partida ofrece al jugador informaciÃ³n sobre su posiciÃ³n, las estadÃ­sticas de su
personaje, el nivel en el que se encuentra, un registro de lo sucedido en los Ãºltimos turnos y le
permite ver lo que ve su personaje.

_9.6.2.1.Minimapa_

## Figura 9-27. Minimapa

El minimapa le da al jugador informaciÃ³n de sus alrededores y su propia posiciÃ³n (en rojo). Le
marca la posiciÃ³n de los enemigos cercanos (en naranja) y de la salida del mapa (en verde).

Puesto que el mapa es mucho mayor de lo que muestra el minimapa, conforme nos vamos
moviendo el minimapa se va actualizando con las zonas de mapa a las que nos vamos
acercando.

_9.6.2.2.EstadÃ­sticas del jugador_

Esta parte de la interfaz muestra informaciÃ³n sobre el personaje del jugador y el nivel en el que
se encuentra.


## Figura 9-28. EstadÃ­sticas del jugador

Los valores mostrados de arriba abajo son los siguientes:

```
ï‚· Nivel: Indica en quÃ© nivel del juego se encuentra el jugador.
ï‚· HP: Indica la salud del personaje, en verde la salud restante y en rojo la faltante.
ï‚· El primer sÃ­mbolo representa una espada, indica el poder de ataque del personaje.
ï‚· El segundo sÃ­mbolo representa un escudo, indica la defensa del personaje.
ï‚· El tercer sÃ­mbolo representa una pociÃ³n, indica la cantidad de pociones que tiene el
jugador en su inventario.
ï‚· El cuarto sÃ­mbolo representa un pergamino, indica la cantidad de pergaminos que
tiene el jugador en su inventario.
ï‚· El ultimo sÃ­mbolo representa una llave, indica si el jugador ha obtenido la llave en el
nivel actual.
```
_9.6.2.3.Registro de acciones_

## Figura 9-29. Registro de acciones

Sirve para mostrar al jugador un registro de los ataques realizados por Ã©l o por los enemigos y el
daÃ±o realizado por cada uno.


_9.6.2.4.BrÃºjula_

## Figura 9-30. BrÃºjula

Le indica al jugador en quÃ© direcciÃ³n estÃ¡ mirando.

_9.6.2.5.Ventana 3D_

## Figura 9-31. Ventana 3D

Esta es la zona donde se ve el renderer en acciÃ³n, aquÃ­ se muestra una visiÃ³n 3D desde el punto
de vista del personaje. AquÃ­ el jugador puede ver en 3D los alrededores del personaje, asÃ­ como
los objetos y enemigos que haya a la vista.


## 10. Conclusiones

Al inicio de este proyecto no estaba seguro de que lograrÃ­a conseguir mi objetivo de desarrollar

un renderer 3D para una mÃ¡quina como Amstrad debido a las grandes dificultades tÃ©cnicas a las

que me enfrentaba.

Sin embargo, puedo decir que el resultado obtenido es mucho mejor de lo que esperaba en un

principio, he logrado desarrollar un renderer 3D y un videojuego que haga uso de Ã©l, con

caracterÃ­sticas raramente vistas en juegos de la Ã©poca del Amstrad, empezando por el 3D, y

siguiendo con el sistema de guardado y carga de partidas y la generaciÃ³n de mapas.

Durante la realizaciÃ³n del proyecto he necesitado hacer uso de muchos conocimientos

adquiridos durante la carrera, pero tambiÃ©n he necesitado reforzar otros como la programaciÃ³n a

bajo nivel (que, aunque no haya llegado al nivel de ensamblador, sÃ­ que he trabajado

directamente con la memoria y el alojamiento manual de Ã©sta). TambiÃ©n he adquirido nuevos

conocimientos y he ganado experiencia como programador, puesto que el reto que suponÃ­a este

proyecto requerÃ­a de conocimientos y tÃ©cnicas de programaciÃ³n considerablemente avanzadas.

El resultado final ha sido un juego en 3D que, a pesar de no ser el mÃ¡s divertido, es jugable

cuenta con un alto nivel rejugabilidad gracias a que sus mapas son generados de forma aleatoria.


## 11. BibliografÃ­a y referencias

```
[1] CPCMania:
http://www.cpcmania.com/Docs/Programming/Painting_pixels_introduction_to_video_
memory.htm
[2] Lode's Computer Graphics Tutorial: Tutorial donde explica el funcionamiento de un
renderer de raycast y su implementaciÃ³n.
http://lodev.org/cgtutor/raycasting.html#Introduction
[3] Battlezone: https://en.wikipedia.org/wiki/Battlezone_(1980_video_game)
[4] Wayout: https://en.wikipedia.org/wiki/Wayout
[5] Wolfenstein 3D: https://en.wikipedia.org/wiki/Wolfenstein_3D
[6] Doom: https://en.wikipedia.org/wiki/Doom_(1993_video_game)
[7] Quake: https://es.wikipedia.org/wiki/Quake_(videojuego)
```

## 12. Anexos

[1] Gameplay del juego usando el renderer:
https://www.youtube.com/watch?v=rDEM1u3_3jo
[2] Repositorio del proyecto: https://github.com/piterayo/MazeAdventure
[3] Archivo de GeoGebra usado para la maquetaciÃ³n del renderer:
https://drive.google.com/file/d/0Bzj8--X5OLbAdnZiM1dBWll0d3M/view?usp=sharing

