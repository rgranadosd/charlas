# Música y Sonidos con Amstrad

**Jeremy Vine**

Edición española de la obra *Bells and Whistles on the Amstrad*.

---

## Página 1

# Música y Sonidos con Amstrad

**AMSTRAD**  
**ESPAÑA**  
**Jeremy Vine**  
**AMSTRAD CPC 464**

---

## Página 2

**Música y Sonidos con Amstrad**

---

## Página 3

A Michael y Rosalind

---

## Página 4

# Música y Sonidos
# con Amstrad

**Jeremy Vine**

**indescomp**

---

## Página 5

MUSICA Y SONIDOS CON AMSTRAD

Edición española de la obra

BELLS AND WHISTLES ON THE AMSTRAD  
Jeremy Vine

publicada en castellano bajo licencia de

Shiva Publishing Limited  
64 Welsh Row  
Nantwich, Cheshire CW5 5ES  
Inglaterra

*Traducción:*  
Emilio Benito Santos

INDESCOMP, S. A.  
Avda. del Mediterráneo, 9  
28007 Madrid

© 1984 Jeremy Vine  
© 1985 Indescomp, S. A.

Reservados todos los derechos. Prohibida la reproducción total o parcial de la obra, por cualquier medio, sin el permiso escrito de los editores.

I.S.B.N.: 28-86176-29-8  
Depósito Legal: 10948-1985

Impresión: Gráficas Lormo. Isabel Méndez, 15. 28038-Madrid.

*Producción de la edición española:*  
Vector Ediciones  
Gutierre de Cetina, 61  
28017 Madrid

---

## Página 6

# Contenido

- Prólogo
- 1 ¿Qué voy a aprender?
- 2 Introducción al sonido
- 3 Sonilandia
- 4 Interludio musical
- 5 El sonido de la música
- 6 La envolvente de volumen
- 7 La envolvente de tono
- 8 Efectos especiales
- 9 Música, maestro
- 10 Ritmo
- 11 Campanas y silbidos
- Apéndice A Palabras reservadas del BASIC de Amstrad
- Apéndice B Los parámetros de SOUND
- Apéndice C Parámetros de la envolvente de volumen
- Apéndice D Parámetros de la envolvente de tono
- Apéndice E Tabla de notas, frecuencias y números de tono
- Apéndice F El generador de sonido: notas técnicas

---

## Página 7

# Prólogo

El gran atractivo de los microordenadores domésticos se debe a los efectos que ejercen sobre nuestros sentidos. La vista y el oído, además de permitirnos hacer una vida normal, pueden procurarnos placer a través de aquello que vemos y oímos. En este área, los ordenadores pueden ser inigualables. Los juegos para ordenadores son tan populares gracias a los efectos visuales que incorporan, y en esto el Amstrad no se queda atrás. Pero los efectos especiales no son solamente visuales. Los ordenadores pueden generar sonidos curiosos, variados y llamativos. De esto es de lo que trata el libro.

El Amstrad CPC 464 tiene incorporado un circuito integrado generador de sonidos. Las instrucciones de BASIC que lo controlan parecen a primera vista complicadas y desconcertantes, pero trataré de explicarlas y demostrar lo fácil que es producir sonidos en el Amstrad. No doy por supuestos demasiados conocimientos por parte del lector; todos los programas han sido escritos teniendo en mente al principiante. No obstante, para aprovechar al máximo la programación de sonidos, es conveniente que el lector tenga unos conocimientos, siquiera rudimentarios, de BASIC.

Vamos a exponer los principios fundamentales de la música y el sonido y a explicar cómo se pueden programar efectos sonoros, tales como ruido de explosiones, y simular el sonido de diversos instrumentos musicales. Usted podrá también utilizar el teclado del Amstrad como si fuera el teclado de un piano. Daremos programas con los que interpretar todo tipo de música, desde simples escalas hasta jazz. Sin embargo, lo más apasionante para el lector llegará cuando sea capaz de programar los sonidos de su gusto; cuando termine de leer este libro estará en condiciones de hacerlo.

Termino con una nota personal. Éste es mi tercer libro; debo agradecer el constante apoyo y aliento de mi familia y amigos a lo largo de muchas y muy duras semanas. Mención especial merecen mis amigos del mundo de las revistas, en particular Tony Quinn, de *Acorn User*, quien publicó mis primeros trabajos y no ha dejado de ayudarme desde entonces.

Londres, 1984

Jeremy Vine

---

## Página 8

# Sobre el autor

Jeremy Vine estudió en la William Ellis Grammar School, Highgate, Londres, y en el City of London Polytechnic, donde se licenció en Psicología. Su primer contacto con ordenadores tuvo lugar con ocasión de sus estudios de licenciatura; desde entonces no se ha alejado de ellos. Cuando dejó el Politécnico, Jeremy trabajó por libre para la revista *Acorn User*, antes de incorporarse a Acorn Computers Limited. Durante este tiempo también estudió para un Master en Neurofisiología. Ahora, tras abandonar Acorn, dedica todo su tiempo a trabajar como escritor autónomo. Además de los libros para Shiva, publica con regularidad en varias revistas de informática, de una de las cuales es editor consultivo. Sus aficiones son tenis, piano, fotografía y, naturalmente, ordenadores.

---

## Página 9

# 1. ¿Qué voy a aprender?

La compra de su Amstrad pudo haber estado motivada por su irrefrenable deseo de jugar a los marcianos o quizá porque pensaba dedicarlo a aplicaciones más serias: programas educativos, proceso de textos o incluso aplicaciones comerciales. No es probable, en cambio, que lo comprara por el generador de sonido que tiene incorporado. Quizá supiera que el Amstrad puede producir sonidos, pero seguramente no cuán variados pueden llegar a ser. Sin embargo, ahora que ha adquirido este libro, se dará cuenta de que su Amstrad puede producir bastante más que un simple «bip». De hecho, las magníficas posibilidades sonoras de este ordenador pueden añadir una nueva dimensión a todas las demás aplicaciones.

El Amstrad es una máquina versátil; su capacidad de sonido es tan sobresaliente como todas las demás. Pero, claro, no se podía esperar menos de un fabricante de alta fidelidad. ¿Se imagina a Amstrad fabricando una máquina silenciosa?

El libro tiene dos objetivos principales. En primer lugar, le enseña los rudimentos de la generación del sonido y la música. Por si usted no sabe tocar ningún instrumento musical ni leer partituras, hay una introducción a estos temas que le dará todos los conocimientos necesarios para programar música en el Amstrad.

El segundo objetivo del libro es explicarle las instrucciones que controlan los efectos sonoros. El área de la música y el sonido es muy amplia, pero las instrucciones de BASIC del Amstrad han sido diseñadas para hacer lo más sencillo posible el control de todos los aspectos de la generación de sonido.

Así pues, ¿qué va usted a aprender? La respuesta es que casi todo lo que pueda necesitar en este campo: la música de todos los tipos estará al alcance de sus dedos. Para quienes prefieran los ruidos y efectos sonoros, el Amstrad ofrece una notable capacidad para simular los sonidos que nos rodean.

---

## Página 10

En este libro damos ejemplos de timbres telefónicos, alarmas, explosiones y silbidos. Hablaremos de estos efectos y de muchos más, con el propósito de inducirle a experimentar y descubrir sus propios efectos especiales.

En todos los listados del libro las palabras reservadas de BASIC aparecen en mayúsculas, pero usted puede teclearlas en minúsculas si lo prefiere; el ordenador hará la conversión automáticamente.

Y ahora comienza la fiesta. Siéntese, relájese y encienda su Amstrad. Pronto empezará a oír, no sólo el ruido de las teclas, sino también música. ¡La aventura va a ser sonada!

---

## Página 11

# 2. Introducción al sonido

La generación de sonidos en el Amstrad es realmente fácil, pero, por supuesto, es necesario conocer y entender todas las instrucciones que controlan el generador. Estas instrucciones, hay que reconocerlo, son complicadas; pero vale la pena hacer un pequeño esfuerzo.

Antes de abordar la primera instrucción necesitamos dar un repaso a los principios fundamentales del sonido. Esto le dará una base firme para saber qué efecto quiere conseguir y así poder utilizar correctamente las instrucciones adecuadas en cada caso.

### Características del sonido

Imagine un sonido cualquiera: un ruido estrepitoso, un suave pitido o una balada. Si es sonido, tendrá características comunes con los demás sonidos. Las características de todo sonido son: intensidad, tono y duración.

#### Intensidad

La intensidad es la característica que percibimos como «volumen»; hace que un sonido o ruido nos parezca más fuerte o más suave. En el Amstrad el volumen global de todos los sonidos generadores se controla mediante el mando de volumen situado al lado derecho de la carcasa. Pero la intensidad de cada nota se puede controlar por programa poniendo en el lugar correspondiente de la instrucción adecuada un número, del 0 al 7.

---

## Página 12

Cuando se percute una tecla del piano, la intensidad del volumen producido crece al principio (durante la fase denominada «de ataque») y luego decrece (en la fase «de declive»). Algo similar ocurre en todos los instrumentos; las diferencias están en que el ataque y el declive sean más o menos rápidos. En el capítulo 6 se estudian las envolventes de volumen, responsables de estas variaciones de intensidad.

La sensación de volumen depende también de otros factores; por ejemplo, de la duración. Un sonido que dure solamente una fracción de segundo parecerá más suave que uno que dure más tiempo, aunque ambos tengan en realidad la misma intensidad.

**Tono**

Dicho con palabras sencillas, el tono es la característica que hace que los sonidos den la sensación de ser más o menos graves o agudos. Más técnicamente, lo que caracteriza el tono es la frecuencia, esto es, el número de ondas de sonido por segundo.

**Duración**

La duración de una nota es el tiempo durante el que ésta está sonando. En todas las composiciones musicales se especifica la duración que ha de tener cada una de las notas y la velocidad a la que la pieza ha de ser ejecutada.

---

## Página 13

Las instrucciones de sonidos del Amstrad permiten especificar la duración de las notas.

Con todos estos recursos disponemos de los medios necesarios para programar una gran variedad de sonidos. Pero las posibilidades de control del generador del sonido del Amstrad son aún más amplias.

### Canales de sonido

El Amstrad tiene **tres** canales de sonido. El programador puede elegir que los canales suenen al unísono o por separado. Los canales llevan los nombres de A, B y C.

Aparte de las notas musicales, el Amstrad puede generar otros sonidos, los llamados efectos de «ruido blanco». En ellos se basan los ruidos de explosiones y otros similares que podemos escuchar en muchos juegos, así como los efectos de percusión que podemos combinar con la música.

Cada canal tiene su propia cola, y en cada una hay espacio para un máximo de cinco instrucciones. Una de ellas será la activa y las otras estarán esperando.

---

## Página 14

# ¿Suena complicado?

Todo esto puede parecerle elemental, o quizá extremadamente complejo. Cualquiera que sea su base en música y programación, este libro no le dejará abandonado. De todo lo dicho volveremos a ocuparnos cuando llegue el momento, y entonces daremos todas las explicaciones necesarias.

Pero empecemos ya a estudiar las instrucciones de BASIC con las que se programan los sonidos del Amstrad.

---

## Página 15

# 3. Sonilandia

Bien, hemos hablado de todas esas magníficas posibilidades sonoras del Amstrad CPC 464, pero ¿qué tenemos que hacer para que el altavoz empiece a sonar? Lo primero, subir el mando de volumen al máximo y dejarlo así. Ahora teclee la siguiente orden:

```basic
SOUND 1,478
```

La nota que ha oído es DO media, con duración de un cincuentavo de segundo. La instrucción `SOUND` va seguida de varios parámetros, siete como máximo, con los que se controlan todas las características del sonido.

---

## Página 16

### El número de selección de canales

El primer parámetro de `SOUND`, representado por `C`, especifica qué canal o canales debe sonar y en qué condiciones.

| Canal | Valor |
|---|---:|
| Canal A | 1 |
| Canal B | 2 |
| Canal C | 4 |

### El número de tono

El segundo parámetro, `T`, controla el tono del sonido. En el ejemplo anterior se usó el número 478, que corresponde a la nota DO media. El parámetro `T` tiene que estar comprendido entre 0 y 4095.

---

## Página 17

Pruebe por ejemplo:

```basic
SOUND 1,956
SOUND 1,478
SOUND 1,60
```

Todas ellas producen la nota DO, pero de diferentes escalas. Cuanto menor es el número de tono, más aguda es la nota.

### El número de duración

Pasemos al siguiente parámetro, `D`, que especifica la duración del sonido, es decir, durante cuánto tiempo va a estar sonando la nota:

```basic
SOUND 1,568,100
```

La figura del libro presenta los parámetros de `SOUND` como:

```basic
SOUND C,T,D,V,EV,ET,R
```

---

## Página 18

El tercer parámetro especifica la duración en unidades de centésimas de segundo; `D=100` especifica un segundo.

| Valor | Efecto |
|---|---|
| Implícito: 20 | Valor por defecto |
| > 0 | Duración del sonido en centésimas de segundo |
| = 0 | Duración controlada por la envolvente de volumen (`ENV`) |
| < 0 | Número de veces que se repite la envolvente |

### El número de volumen

Veamos el cuarto parámetro, `V`, que especifica el volumen.

```basic
10 FOR volumen=0 TO 7
20 SOUND 1,478,25,volumen
30 NEXT
```

---

## Página 19

El volumen va aumentando con cada pasada por el bucle; cuando el número llega a 7, el sonido es de la máxima intensidad posible. El margen de valores es, pues, de 0 a 7.

Los parámetros quinto y sexto corresponden a las envolventes de volumen (`ENV`) y tono (`ENT`).

### El número de ruido

El último parámetro, `R`, es el número de tono del ruido. Especifica si se ha de producir ruido y, si es así, de qué frecuencia. Su margen utilizable es de 0 a 31.

---

## Página 20

```basic
10 ENV 15,43,-68,3
20 FOR volumen=0 TO 7
30 SOUND 1,478,25,volumen,15,0,0
40 NEXT
```

Si cambia la línea 30 por:

```basic
30 SOUND 1,478,25,volumen,15,0,10
```

apreciará el efecto del ruido añadido.

También se propone este programa para experimentar con `SOUND`:

```basic
10 CLS
20 PRINT"Elija numero de tono (0-4095)"
30 INPUT t
40 PRINT"Elija numero de duracion (1-32767)"
50 INPUT d
60 PRINT"Elija volumen (0-7)"
```

---

## Página 21

```basic
70 INPUT v
80 PRINT"Elija ruido (0-31)"
90 INPUT r
100 SOUND 1,t,d,v,0,0,r
110 PRINT"Pulse una tecla para continuar"
120 x$=INKEY$:IF x$="" THEN 120 ELSE 10
```

### Cóctel de canales

El número de selección de canales sirve para más cosas que la simple elección de un canal. Se puede usar también para sincronizar, retener sonidos o borrar colas.

Ejemplo:

```basic
SOUND 3,478,50,7
```

porque 1 (canal A) + 2 (canal B) = 3.

---

## Página 22

| Valor | Canal(es) | Efecto |
|---:|---|---|
| 1 | A | Seleccionar canal A |
| 2 | B | Seleccionar canal B |
| 4 | C | Seleccionar canal C |
| 8 | → A | Sincronizar con canal A |
| 16 | → B | Sincronizar con canal B |
| 32 | → C | Sincronizar con canal C |
| 64 | — | Retener sonido |
| 128 | — | Borrar cola de sonidos |

---

## Página 23

Ejemplo de combinación:

```basic
1 (canal A) + 16 (sincronizar con B) + 64 (retener) = 81
```

### SQ y RELEASE

La función `SQ` da el número de plazas libres que quedan en la cola del sonido del canal especificado. Esto es útil para determinar si un determinado canal está aún activo.

```basic
10 PRINT "Esta sonando el canal A"
20 SOUND 1,261,250,7
25 WHILE SQ(1)>127:WEND
30 PRINT "FIN"
```

`RELEASE` libera el sonido de un canal si éste está retenido.

---

## Página 24

Con esto termina el repaso de las instrucciones de sonido del Amstrad. La mejor forma de entenderlas y dominarlas es experimentar con la instrucción `SOUND`.

---

## Página 25

# 4. Interludio musical

En este capítulo se da una introducción a la terminología y la notación de la música. El objetivo es preparar al lector para convertir una pieza musical en un programa de ordenador.

### Pentagramas y notas

La música se escribe en papel rayado, agrupando las líneas de cinco en cinco. Un grupo de rayas es lo que se llama *pentagrama*.

---

## Página 26

Las notas se pueden escribir sobre las líneas o entre dos de ellas. La altura a la que se encuentra una nota indica su nombre.

Cada siete notas los nombres se repiten; es decir, las siete primeras notas son DO, RE, MI, FA, SOL, LA, SI, y la siguiente vuelve a ser DO, pero una octava más arriba.

### Duración

Hay diversos signos que caracterizan las diferentes duraciones de las notas.

---

## Página 27

| Nota | Nombre |
|---|---|
| o | Redonda |
| d | Blanca |
| d | Negra |
| δ | Corchea |
| δ | Semicorchea |
| δ | Fusa |

Se pueden indicar períodos de silencio insertando pausas entre notas.

---

## Página 28

# Claves y escalas

Para facilitar la lectura de la música se pueden utilizar dos pentagramas paralelos. Las dos claves más frecuentes, sobre todo en música para piano, son las de SOL y FA.

Cada serie de ocho notas forma una **escala**. La más sencilla es la de DO mayor.

Todas las escalas mayores responden al mismo esquema: tono-tono-semitono-tono-tono-tono-semitono.

---

## Página 29

Las teclas negras del piano representan sostenidos y bemoles. Una nota afectada por sostenido o bemol puede ser devuelta a su tono original mediante el signo becuadro.

---

## Página 30

### Compases y ritmo

La música está dividida en porciones llamadas *medidas o compases*. Al principio de la partitura se especifica la duración de los compases mediante la signatura de tiempo.

También se explican conceptos como **staccato**, **ligado** y **ligadura**.

---

## Página 31

Se anima al lector a releer el capítulo si lo considera necesario antes de pasar a escribir música en el Amstrad.

---

## Página 33

# 5. El sonido de la música

La conversión de la música a una forma que el Amstrad pueda comprender es relativamente sencilla. En este capítulo se utilizan los valores de `T` que hacen que el generador de sonido emita tonos musicales.

### Escalas cromáticas

La fórmula correcta para calcular la frecuencia es:

```text
frecuencia = 440 * (2^(octava + ((n-10)/12)))
```

y el número de tono se obtiene con:

```text
T = ROUND(125000 / frecuencia)
```

---

## Página 34

```basic
10 FOR num=1 TO 12
20 READ a(y)
30 frec=440*(2^(0+((a(y)-10)/12)))
40 tono=ROUND(125000/frec)
50 SOUND 1,tono,35,15
60 NEXT
70 DATA 1,2,3,4,5,6,7,8,9,10,11,12
```

También se muestra cómo construir la escala de DO mayor modificando la línea `DATA`.

---

## Página 35

### Melodías

```basic
10 tempo=2.5
20 RESTORE 90
30 FOR x=1 TO 37
40 READ tono,duracion
50 frec=440*(2^(0+((tono-10)/12)))
60 numtono=ROUND(125000/frec)
70 SOUND 1,numtono,duracion*tempo,15
80 NEXT
90 DATA 27,10,29,10,25,10,22,20,24,10,20,20
100 DATA 15,10,17,10,13,10,10,20,12,10,8,20
110 DATA 3,10,5,10,1,10,-2,20,0,10,-2,10,-3,10,-4,40
120 DATA 3,10,4,10,5,10,13,20,5,10,13,20,5,10,13,40
130 DATA 13,10,15,10,17,10,13,10,15,10,17,20,12,10,15,20,13,40
```

---

## Página 37

# 6. La envolvente de volumen

La instrucción de envolvente de volumen (`ENV`) permite controlar la variación del volumen con el tiempo para un sonido dado.

```basic
ENV n,P1,Q1,R1,P2,Q2,R2,P3,Q3,R3,P4,Q4,R4,P5,Q5,R5
```

---

## Página 38

Ejemplo:

```basic
10 ENV 1,10,4,3,5,-3,20,1,0,20,5,3,10,10,-3,30
20 SOUND 1,478,0,0,1,0,0
```

La forma de la envolvente se divide en hasta cinco secciones. Cada sección se caracteriza por tres parámetros: número de escalones, altura de cada escalón y duración de cada escalón.

---

## Página 39

Ejemplo de cálculo de duración total de una envolvente:

```text
(3*10)+(20*5)+(20*1)+(10*5)+(30*10)=500
```

Como las unidades son centésimas de segundo, 500 equivale a 5 segundos.

Una envolvente puede cancelarse redefiniéndola sin secciones:

```basic
ENV 1
```

---

## Página 40

Programa de prueba para `ENV`:

```basic
10 CLS
20 PRINT"Elija numero de saltos (0-127)"
30 INPUT numsaltos
40 PRINT"Elija tama\o del salto (-128 a +127)"
50 INPUT tamsalto
60 PRINT"Elija tiempo de pausa (0-255)"
70 INPUT tiempopausa
80 ENV 1,numsaltos,tamsalto,tiempopausa
90 SOUND 1,240,15,15,1,1,0
100 ENV 1
110 PRINT"Pulse una tecla para continuar"
120 x$=INKEY$:IF x$="" THEN 120
130 GOTO 10
```

---

## Página 41

### Instrumentos

Se explica que es posible imitar, dentro de ciertos límites, el sonido de instrumentos musicales mediante envolventes, aunque el generador electrónico tiene limitaciones inevitables.

---

## Página 43

# 7. La envolvente de tono

La instrucción `ENT` controla las variaciones de tono de las notas y crea un efecto de vibrato.

```basic
ENT n,T1,V1,W1,T2,V2,W2,T3,V3,W3,T4,V4,W4,T5,V5,W5
```

---

## Página 44

Ejemplo:

```basic
10 ENT 1,65,5,1,10,-2,10,10,2,5,30,-5,1
15 ENT 1
20 SOUND 1,478,50,15,0,1,0
```

---

## Página 45

Los parámetros de `ENT` funcionan de manera análoga a los de `ENV`, pero aplicados al tono. El número de escalones puede variar entre 0 y 239.

Si el número de envolvente se pone negativo, la envolvente se repite durante todo el tiempo en que la nota está sonando.

---

## Página 46

Programa para experimentar con `ENT`:

```basic
10 CLS
20 PRINT"Elija numero de escalones (0-239)"
30 INPUT numesc
40 PRINT"Elija tama\o de escalones (-128 a +127)"
50 INPUT tamaesc
60 PRINT"Elija duracion de escalones (0-255)"
70 INPUT duraesc
80 ENT 1,numesc,tamaesc,duraesc
90 SOUND 1,240,100,15,0,1,0
100 ENT 1
110 PRINT"Pulse una tecla para continuar"
120 x$=INKEY$:IF x$="" THEN 120
130 GOTO 10
```

También se explican las fases de ataque, sostenimiento y caída del sonido.

---

## Página 47

Se indica que el generador de sonido del Amstrad no puede producir buenas imitaciones perfectas de instrumentos musicales, ya que el tono que genera no es una onda sinusoidal pura, sino una onda cuadrada con sus armónicos inherentes.

---

## Página 49

# 8. Efectos especiales

El Amstrad puede generar, además de música, efectos sonoros espectaculares que el lector puede incorporar a sus programas, especialmente juegos.

### Aventura sonada

```basic
10 ENT 1,80,-4,1
20 SOUND 1,478,50,15,0,1,0
30 GOTO 20
```

---

## Página 50

Otros ejemplos:

```basic
10 FOR tipo=1 TO 45
20 SOUND 1,901,7,15,0,0,1
30 FOR retardo=1 TO 100:NEXT
40 NEXT
```

```basic
10 FOR repetir=1 TO 6
20 radio=INT(RND*20)
30 SOUND 1,radio,100,15,0,0,1
40 NEXT
```

```basic
10 FOR repetir=0 TO 140
20 calcula=INT(RND*150)
30 SOUND 1,calcula,3,15,0,0,0
40 NEXT
```

---

## Página 51

Ejemplo de caída de bomba:

```basic
10 FOR cae=50 TO 150
20 SOUND 1,cae,3,15,0,0,0
30 NEXT
40 FOR repite=0 TO 45
50 calcula=1
60 SOUND 1,calcula,3,15,0,0,31
70 NEXT
```

---

## Página 52

Comienza el programa `8.6`, un generador de envolventes de volumen, con menú y captura de parámetros.

---

## Página 53

Final del programa `8.6`:

```basic
540 REM Ejecutar SOUND
560 SOUND canal,478,duracion,1,1,0,ruido
```

El programa permite repetir el sonido, modificar parámetros y visualizar la envolvente definida.

---

## Página 54

Se ofrece una tabla con parámetros orientativos para algunos sonidos, como disparos, instrumento de cuerda, golpes en puerta o tambor y explosión.

### Percusión

```basic
10 ENV 1,23,-68,3
20 FOR duración=1 TO 50
30 SOUND 7,748,duración,15,1,1,1
40 NEXT
```

---

## Página 55

# 9. Música, maestro

El objetivo es convertir al lector en un pianista, transformando el teclado del Amstrad en un teclado musical.

### Un sintetizador

```basic
30 w$=INKEY$:IF w$="" THEN 30
10 s$="q2w3er5t6y7ui9oOp"
70 SOUND 1,tono,15,15
50 frecuencia=440*(2^(1+((nota-10)/12)))
60 tono=ROUND(125000/frecuencia)
40 nota=INSTR(s$,w$)
20 WHILE x=0
80 WEND
```

---

## Página 56

Se explica cómo funciona el teclado musical y cómo la variable `nota` se deriva de la posición de la tecla pulsada dentro de la cadena `s$`.

---

## Página 57

Se muestra la correspondencia entre el teclado del Amstrad y el del piano, y se anima al lector a probar melodías sencillas.

---

## Página 58

### Más octavas

Para ampliar el teclado a dos octavas se añaden estas líneas:

```basic
15 octava$="zsxdcvgbhnjm,l.;/"
65 IF nota=0 THEN GOSUB 90
90 nota=INSTR(octava$,w$)
100 frecuencia=440*(2^(0+((nota-10)/12)))
110 tono=ROUND(125000/frecuencia)
120 RETURN
```

---

## Página 59

# 10. Ritmo

En este capítulo se explica cómo convertir la duración de las notas a números que el Amstrad pueda entender.

Se distingue entre **ritmo** y **tempo**.

---

## Página 60

| Nota | Duración |
|---|---:|
| 𝅿 | 10 |
| 𝅿. | 15 |
| 𝅿 | 20 |
| 𝅿. | 30 |
| ♩ | 40 |
| ♩. | 60 |
| 𝅼 | 80 |
| 𝅼. | 120 |
| 𝅽 | 160 |

Se recuerda que para variar el tempo basta con modificar el multiplicador aplicado a las duraciones antes de llamar a `SOUND`.

---

## Página 61

# 11. Campanas y silbidos

El espectro de los sonidos del Amstrad es muy amplio y prácticamente sólo está limitado por la imaginación del programador.

Se anima al lector a seguir experimentando con armonía para tres voces, tambores y más efectos.

---

## Página 62

Ejemplos finales de efectos sonoros:

Teléfono comunicando:

```basic
10 SOUND 1,100,40,15
20 FOR pausa=0 TO 900:NEXT
30 GOTO 10
```

Teléfono sin respuesta:

```basic
10 ENV 1,100,122,1
20 SOUND 1,239,0,15,1,0,0
30 FOR x=0 TO 2000:NEXT
40 GOTO 20
```

Silbido de locomotora:

```basic
10 FOR bocina=1 TO 3
20 SOUND 1,239,80,15,1,2,1
30 FOR pausa=0 TO 900:NEXT
40 NEXT
```

---

## Página 63

# Apéndice A. Palabras reservadas del BASIC de Amstrad

Este apéndice contiene un resumen de instrucciones de BASIC del Amstrad. Entre ellas aparecen, por ejemplo:

- `ABS`
- `AFTER`
- `AND`
- `ASC`
- `ATN`
- `AUTO`
- `BIN$`
- `BORDER`
- `CALL`
- `CAT`
- `CHAIN`
- `CHAIN MERGE`
- `CHR$`
- `CINT`
- `CLEAR`
- `CLG`
- `CLOSEIN`

---

## Página 64

Continúan las palabras reservadas de BASIC, incluyendo:

- `CLOSEOUT`
- `CLS`
- `CONT`
- `COS`
- `CREAL`
- `DATA`
- `DEF FN`
- `DEFINT`
- `DEFREAL`
- `DEFSTR`
- `DEG`
- `DELETE`
- `DI`
- `DIM`
- `DRAW`
- `DRAWR`
- `EDIT`
- `EI`
- `ELSE`
- `END`
- `ENT`
- `ENV`
- `EOF`
- `ERASE`
- `ERL`
- `ERR`
- `ERROR`
- `EVERY`
- `EXP`
- `FIX`
- `FOR`

---

## Página 65

Resumen de selección de canales y números de duración:

### Selección de canales

| Valor | Efecto |
|---:|---|
| 1 | Seleccionar canal A |
| 2 | Seleccionar canal B |
| 4 | Seleccionar canal C |
| 8 | Sincronizar con A |
| 16 | Sincronizar con B |
| 32 | Sincronizar con C |
| 64 | Retener |
| 128 | Borrar cola |

### Números de duración

- Implícito: 20
- Margen: -32768 a +32767
- `> 0`: duración del sonido
- `= 0`: duración controlada por `ENV`
- `< 0`: número de veces que se repite la envolvente

---

## Página 71

# Apéndice C. Parámetros de la envolvente de volumen

```basic
ENV n,P1,Q1,R1,P2,Q2,R2,P3,Q3,R3,P4,Q4,R4,P5,Q5,R5
```

- `n` = número de la envolvente
- `Pn` = número de escalones
- `Qn` = amplitud de los escalones
- `Rn` = duración de los escalones
- Mínimo = una sección
- Máximo = cinco secciones

Si no se define ninguna sección, por ejemplo `ENV 1`, la envolvente queda desactivada.

---

## Página 73

# Apéndice D. Parámetros de la envolvente de tono

```basic
ENT n,T1,V1,W1,T2,V2,W2,T3,V3,W3,T4,V4,W4,T5,V5,W5
```

- `n` = número de la envolvente
- `Tn` = número de escalones
- `Vn` = amplitud de los escalones
- `Wn` = duración de los escalones
- Mínimo = una sección
- Máximo = cinco secciones

Si no se define ninguna sección, por ejemplo `ENT 1`, la envolvente queda desactivada.

---

## Página 75

# Apéndice E. Tabla de notas, frecuencias y números de tono

DO media = C media = 1 (octava nº 0)

| n | Nota | Frecuencia | Número de tono | Parámetro de octava (P) |
|---:|---|---:|---:|---:|
| -35 | C | 32.703 | 3822 | -3 |
| -34 | C# | 34.648 | 3608 | -3 |
| -33 | D | 36.708 | 3405 | -3 |
| -32 | D# | 38.891 | 3214 | -3 |
| -31 | E | 41.203 | 3034 | -3 |
| -30 | F | 43.654 | 2863 | -3 |
| -29 | F# | 46.249 | 2703 | -3 |
| -28 | G | 48.999 | 2551 | -3 |
| -27 | G# | 51.913 | 2408 | -3 |
| -26 | A | 55.000 | 2273 | -3 |
| -25 | A# | 58.270 | 2145 | -3 |
| -24 | B | 61.735 | 2025 | -3 |
| -23 | C | 65.406 | 1911 | -2 |
| -22 | C# | 69.296 | 1804 | -2 |
| -21 | D | 73.416 | 1703 | -2 |
| -20 | D# | 77.782 | 1607 | -2 |
| -19 | E | 82.407 | 1517 | -2 |
| -18 | F | 87.307 | 1432 | -2 |
| -17 | F# | 92.499 | 1351 | -2 |
| -16 | G | 97.999 | 1276 | -2 |
| -15 | G# | 103.826 | 1204 | -2 |
| -14 | A | 110.000 | 1136 | -2 |

---

## Página 76

| n | Nota | Frecuencia | Número de tono | Parámetro de octava (P) |
|---:|---|---:|---:|---:|
| -13 | A# | 116.541 | 1073 | -2 |
| -12 | B | 123.471 | 1012 | -2 |
| -11 | C | 130.813 | 956 | -1 |
| -10 | C# | 138.591 | 902 | -1 |
| -9 | D | 146.832 | 851 | -1 |
| -8 | D# | 155.564 | 804 | -1 |
| -7 | E | 164.814 | 758 | -1 |
| -6 | F | 174.614 | 716 | -1 |
| -5 | F# | 184.997 | 676 | -1 |
| -4 | G | 195.998 | 638 | -1 |
| -3 | G# | 207.652 | 602 | -1 |
| -2 | A | 220.000 | 568 | -1 |
| -1 | A# | 233.082 | 536 | -1 |
| 0 | B | 246.942 | 506 | -1 |
| +1 | C | 261.626 | 478 | 0 |
| +2 | C# | 277.183 | 451 | 0 |
| +3 | D | 293.665 | 426 | 0 |
| +4 | D# | 311.127 | 402 | 0 |
| +5 | E | 329.628 | 379 | 0 |
| +6 | F | 349.228 | 358 | 0 |
| +7 | F# | 369.994 | 338 | 0 |
| +8 | G | 391.995 | 319 | 0 |
| +9 | G# | 415.305 | 301 | 0 |
| +10 | A | 440.000 | 284 | 0 |
| +11 | A# | 466.164 | 268 | 0 |
| +12 | B | 493.883 | 253 | 0 |
| +13 | C | 523.251 | 239 | 1 |
| +14 | C# | 554.365 | 225 | 1 |
| +15 | D | 587.330 | 213 | 1 |
| +16 | D# | 622.254 | 201 | 1 |
| +17 | E | 659.255 | 190 | 1 |
| +18 | F | 698.457 | 179 | 1 |
| +19 | F# | 739.989 | 169 | 1 |
| +20 | G | 783.991 | 159 | 1 |
| +21 | G# | 830.609 | 150 | 1 |
| +22 | A | 880.000 | 142 | 1 |
| +23 | A# | 932.328 | 134 | 1 |
| +24 | B | 987.767 | 127 | 1 |
| +25 | C | 1046.502 | 119 | 2 |
| +26 | C# | 1108.731 | 113 | 2 |

---

## Página 77

| n | Nota | Frecuencia | Número de tono | Parámetro de octava (P) |
|---:|---|---:|---:|---:|
| +27 | D | 1174.659 | 106 | 2 |
| +28 | D# | 1244.508 | 100 | 2 |
| +29 | E | 1318.510 | 95 | 2 |
| +30 | F | 1396.913 | 89 | 2 |
| +31 | F# | 1479.978 | 84 | 2 |
| +32 | G | 1567.982 | 80 | 2 |
| +33 | G# | 1661.219 | 75 | 2 |
| +34 | A | 1760.000 | 71 | 2 |
| +35 | A# | 1864.655 | 67 | 2 |
| +36 | B | 1975.533 | 63 | 2 |
| +37 | C | 2093.004 | 60 | 3 |
| +38 | C# | 2217.461 | 56 | 3 |
| +39 | D | 2349.318 | 53 | 3 |
| +40 | D# | 2489.016 | 50 | 3 |
| +41 | E | 2637.021 | 47 | 3 |
| +42 | F | 2793.826 | 45 | 3 |
| +43 | F# | 2959.955 | 42 | 3 |
| +44 | G | 3135.963 | 40 | 3 |
| +45 | G# | 3322.438 | 38 | 3 |
| +46 | A | 3520.000 | 36 | 3 |
| +47 | A# | 3729.310 | 34 | 3 |
| +48 | B | 3951.066 | 32 | 3 |
| +49 | C | 4186.009 | 30 | 4 |
| +50 | C# | 4434.922 | 28 | 4 |
| +51 | D | 4698.636 | 27 | 4 |
| +52 | D# | 4978.032 | 25 | 4 |
| +53 | E | 5274.041 | 24 | 4 |
| +54 | F | 5587.652 | 22 | 4 |
| +55 | F# | 5919.911 | 21 | 4 |
| +56 | G | 6271.927 | 20 | 4 |
| +57 | G# | 6644.875 | 19 | 4 |
| +58 | A | 7040.000 | 18 | 4 |
| +59 | A# | 7458.621 | 17 | 4 |
| +60 | B | 7902.133 | 16 | 4 |

---

## Página 79

# Apéndice F

El OCR recuperado termina al inicio de este apéndice en el material disponible.
