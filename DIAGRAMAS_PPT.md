# Diagramas para Presentación PowerPoint

Este documento contiene diagramas simplificados y listos para usar en presentaciones PowerPoint.

---

## Diagrama 1: Arquitectura de Alto Nivel

```
┌─────────────────────────────────────────────────────────────────────┐
│                    ARQUITECTURA DE ALTO NIVEL                      │
└─────────────────────────────────────────────────────────────────────┘

    ┌──────────┐
    │ Usuario  │
    │ (NLP)    │
    └────┬─────┘
         │
         │ Consulta en lenguaje natural
         ▼
    ┌─────────────────────┐
    │  Agente Python      │
    │  (Orquestador)      │
    └────┬────────────────┘
         │
         │ Consulta procesada
         ▼
    ┌─────────────────────┐
    │ Semantic Kernel     │
    │  (Orquestación IA)   │
    └────┬────────────────┘
         │
         ├─────────────────┬──────────────┐
         │                 │              │
         ▼                 ▼              │
    ┌──────────┐    ┌──────────────┐
    │ Plugin   │    │   LLM        │
    │ Shopify  │    │  Requests    │
    │          │    │  (OpenAI)    │
    └────┬─────┘    └──────┬───────┘
         │                 │
         └─────────┬───────┴──────────────┘
                   │
                   │ OAuth2
                   │ (Todas las llamadas externas)
                   ▼
         ┌─────────────────────┐
         │  WSO2 API Gateway   │
         │  (Centralizado)      │
         └────┬─────────────────┘
              │
              ├─────────────────┬──────────────┐
              │                 │              │
              ▼                 ▼
    ┌─────────────────┐  ┌─────────────────┐
    │   Shopify API   │  │   OpenAI API    │
    │                 │  │  (IA Gateway)    │
    └─────────────────┘  └─────────────────┘
```

---

## Diagrama 2: Flujo de una Llamada (Simplificado)

```
┌─────────────────────────────────────────────────────────────────────┐
│              FLUJO DE UNA LLAMADA - ACTUALIZAR PRECIO              │
└─────────────────────────────────────────────────────────────────────┘

1. USUARIO
   "Actualiza precio ID 123456 a 99.99"
         │
         ▼
2. AGENTE PYTHON
   • Detecta intención: UPDATE_PRICE
   • Extrae: ID=123456, precio=99.99
         │
         ▼
3. SEMANTIC KERNEL
   • Orquesta ejecución
   • Llama a función del plugin
         │
         ▼
4. PLUGIN SHOPIFY
   • Obtiene precio actual ($150.00)
   • Prepara actualización
         │
         ▼
5. AUTENTICACIÓN WSO2
   • Obtiene token OAuth2
         │
         ▼
6. WSO2 GATEWAY
   • Valida token
   • Enruta a Shopify
         │
         ▼
7. SHOPIFY API
   • Actualiza precio a $99.99
   • Confirma cambio
         │
         ▼
8. RESPUESTA
   • Plugin valida éxito
   • Guarda en memoria
         │
         ▼
9. SEMANTIC KERNEL
   • Prepara prompt para LLM
         │
         │ OAuth2
         ▼
10. WSO2 IA GATEWAY
    • Valida token
    • Enruta a OpenAI
         │
         ▼
11. OPENAI API
    • Procesa prompt
    • Genera respuesta natural
         │
         │ Respuesta vía WSO2
         ▼
12. SEMANTIC KERNEL
    • Recibe respuesta formateada
         │
         ▼
13. USUARIO
    "Precio actualizado de $150.00 a $99.99"
```

---

## Diagrama 3: Componentes y Responsabilidades

```
┌─────────────────────────────────────────────────────────────────────┐
│              COMPONENTES Y SUS RESPONSABILIDADES                   │
└─────────────────────────────────────────────────────────────────────┘

┌──────────────────────┐
│   USUARIO            │
│ • Envía consultas     │
│ • Recibe respuestas   │
└──────────────────────┘

┌──────────────────────┐
│   AGENTE PYTHON      │
│ • Orquestación        │
│ • Detección intenciones│
│ • Gestión de estado   │
│ • Memoria de precios  │
└──────────────────────┘

┌──────────────────────┐
│ SEMANTIC KERNEL      │
│ • Conecta LLM y       │
│   funciones          │
│ • Gestiona contexto   │
│ • Sistema de plugins  │
└──────────────────────┘

┌──────────────────────┐
│   OPENAI GPT-4o-mini  │
│ • Procesa lenguaje    │
│   natural             │
│ • Genera respuestas   │
│ • Anti-alucinación    │
│ • Acceso vía WSO2     │
│   IA Gateway          │
└──────────────────────┘

┌──────────────────────┐
│  PLUGIN SHOPIFY      │
│ • Funciones ejecutables│
│ • Abstracción API     │
│ • Operaciones CRUD    │
└──────────────────────┘

┌──────────────────────┐
│  WSO2 API GATEWAY    │
│ • Autenticación OAuth2│
│ • Enrutamiento        │
│   - Shopify API       │
│   - OpenAI API        │
│ • Seguridad           │
│ • Rate limiting       │
│ • Centralizado        │
└──────────────────────┘

┌──────────────────────┐
│   SHOPIFY API        │
│ • Gestión productos   │
│ • Actualización precios│
│ • Búsqueda            │
│ • Acceso vía WSO2     │
└──────────────────────┘
```

---

## Diagrama 4: Flujo de Autenticación OAuth2

```
┌─────────────────────────────────────────────────────────────────────┐
│                    FLUJO OAUTH2 CLIENT CREDENTIALS                  │
└─────────────────────────────────────────────────────────────────────┘

AGENTE PYTHON                    WSO2 TOKEN ENDPOINT
┌─────────────┐                  ┌──────────────────┐
│             │                  │                  │
│ Necesita    │                  │                  │
│ token       │                  │                  │
│             │                  │                  │
│ POST /token │─────────────────►│ Valida           │
│ Headers:    │                  │ credenciales      │
│ Basic auth  │                  │                  │
│             │                  │ Genera            │
│             │                  │ access_token      │
│             │◄─────────────────│                  │
│ Almacena    │                  │ Respuesta:        │
│ token       │                  │ {access_token}    │
│             │                  │                  │
└──────┬──────┘                  └──────────────────┘
       │
       │ Usa token en llamadas
       │ Authorization: Bearer {token}
       ▼
WSO2 API GATEWAY
┌─────────────────────────────┐
│                             │
│ Valida token                │
│                             │
│ Enruta a:                   │
│  • Shopify API              │
│  • OpenAI API (IA Gateway)  │
│                             │
└─────────────────────────────┘
```

---

## Diagrama 5: Stack Tecnológico

```
┌─────────────────────────────────────────────────────────────────────┐
│                      STACK TECNOLÓGICO                             │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    CAPA DE PRESENTACIÓN                     │
│  • Interfaz de línea de comandos (CLI)                      │
│  • Lenguaje natural (Español/Inglés)                        │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    CAPA DE APLICACIÓN                        │
│  • Python 3.8+                                               │
│  • Microsoft Semantic Kernel                                 │
│  • OpenAI GPT-4o-mini                                        │
│  • Sistema de plugins                                        │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    CAPA DE INTEGRACIÓN                       │
│  • WSO2 API Manager (Gateway)                                │
│  • OAuth2 Client Credentials                                 │
│  • REST API                                                  │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    CAPA DE DATOS/SERVICIOS                    │
│  • Shopify Admin API (vía WSO2 Gateway)                      │
│  • OpenAI API (vía WSO2 IA Gateway)                          │
│  • Gestión de productos                                      │
│  • Gestión de precios                                        │
│  • Procesamiento de lenguaje natural                         │
└─────────────────────────────────────────────────────────────┘
```

---

## Diagrama 6: Funciones del Plugin Shopify

```
┌─────────────────────────────────────────────────────────────────────┐
│              FUNCIONES EXPUESTAS AL LLM                            │
└─────────────────────────────────────────────────────────────────────┘

PLUGIN SHOPIFY
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  CONSULTAS                                                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ • get_products_list()                               │   │
│  │   → Lista todos los productos                       │   │
│  │                                                      │   │
│  │ • get_products_sorted(order)                        │   │
│  │   → Productos ordenados por precio                  │   │
│  │                                                      │   │
│  │ • count_products()                                  │   │
│  │   → Cuenta total de productos                       │   │
│  │                                                      │   │
│  │ • find_product_by_name(name)                        │   │
│  │   → Búsqueda con fuzzy matching                     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ACTUALIZACIONES                                            │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ • update_product_price(id, price)                   │   │
│  │   → Actualiza por ID                                │   │
│  │                                                      │   │
│  │ • update_product_price_by_name(name, price)        │   │
│  │   → Actualiza por nombre                            │   │
│  │                                                      │   │
│  │ • update_product_price_with_math(id, op, value)    │   │
│  │   → Operaciones matemáticas                         │   │
│  │                                                      │   │
│  │ • revert_price(id)                                  │   │
│  │   → Restaura precio anterior                        │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Diagrama 7: Casos de Uso Principales

```
┌─────────────────────────────────────────────────────────────────────┐
│                      CASOS DE USO PRINCIPALES                      │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  1. LISTAR PRODUCTOS                                        │
│  Usuario: "Lista los productos"                             │
│  → get_products_list()                                      │
│  → Respuesta: Lista completa con IDs y precios              │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  2. CONTAR PRODUCTOS                                        │
│  Usuario: "¿Cuántos productos hay?"                         │
│  → count_products()                                         │
│  → Respuesta: "La tienda tiene X productos"                 │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  3. ACTUALIZAR PRECIO POR ID                                │
│  Usuario: "Actualiza precio ID 123456 a 99.99"              │
│  → update_product_price(123456, "99.99")                   │
│  → Respuesta: "Precio actualizado de $X a $99.99"           │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  4. ACTUALIZAR PRECIO POR NOMBRE                            │
│  Usuario: "Cambia precio de Gift Card a 200"                │
│  → find_product_by_name("Gift Card")                        │
│  → update_product_price_by_name("Gift Card", "200")         │
│  → Respuesta: "Precio actualizado..."                       │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  5. OPERACIÓN MATEMÁTICA                                    │
│  Usuario: "Añade 1000 al precio de X"                       │
│  → update_product_price_with_math(id, "add", 1000)        │
│  → Respuesta: "Precio actualizado de $X a $Y (añadiendo...)"│
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  6. REVERTIR PRECIO                                         │
│  Usuario: "Vuelve precio original del ID 123456"            │
│  → revert_price(123456)                                     │
│  → Respuesta: "Precio restaurado a $X"                      │
└─────────────────────────────────────────────────────────────┘
```

---

## Diagrama 8: Ventajas de la Arquitectura

```
┌─────────────────────────────────────────────────────────────────────┐
│                    VENTAJAS DE LA ARQUITECTURA                     │
└─────────────────────────────────────────────────────────────────────┘

┌──────────────────────┐  ┌──────────────────────┐
│   SEGURIDAD          │  │   ESCALABILIDAD      │
│ • OAuth2             │  │ • Componentes        │
│ • WSO2 Gateway       │  │   independientes     │
│   Centralizado       │  │ • Escala horizontal  │
│ • Tokens seguros     │  │ • Gateway único      │
│ • Todas las APIs     │  │   punto de entrada   │
│   por gateway        │  │                     │
└──────────────────────┘  └──────────────────────┘

┌──────────────────────┐  ┌──────────────────────┐
│   MANTENIBILIDAD     │  │   EXTENSIBILIDAD      │
│ • Código modular     │  │ • Nuevos plugins      │
│ • Separación de      │  │ • Nuevas funciones    │
│   responsabilidades  │  │ • Fácil integración    │
└──────────────────────┘  └──────────────────────┘

┌──────────────────────┐  ┌──────────────────────┐
│   EXPERIENCIA         │  │   CONFIABILIDAD      │
│ • Lenguaje natural    │  │ • Anti-alucinación   │
│ • Bilingüe            │  │ • Validación datos   │
│ • Respuestas claras   │  │ • Verificación       │
└──────────────────────┘  └──────────────────────┘
```

---

## Diagrama 9: Flujo de Datos Detallado

```
┌─────────────────────────────────────────────────────────────────────┐
│                  FLUJO DE DATOS DETALLADO                         │
└─────────────────────────────────────────────────────────────────────┘

USUARIO
  │
  │ "Actualiza precio ID 123456 a 99.99"
  ▼
AGENTE PYTHON
  │ • Parsea entrada
  │ • Detecta: UPDATE_PRICE
  │ • Extrae: ID=123456, precio=99.99
  ▼
SEMANTIC KERNEL
  │ • Construye prompt
  │ • Identifica función: update_product_price()
  │ • Prepara contexto
  ▼
PLUGIN SHOPIFY
  │ • Ejecuta update_product_price()
  │ • PASO 1: GET /products/123456.json
  │   → Obtiene precio actual: $150.00
  │ • PASO 2: Prepara payload PUT
  │ • PASO 3: PUT /products/123456.json
  │   → Actualiza a $99.99
  │ • PASO 4: Valida respuesta
  │ • PASO 5: Guarda en PriceMemory
  ▼
WSO2 GATEWAY
  │ • Autentica con OAuth2
  │ • Enruta peticiones
  │ • Aplica políticas
  ▼
SHOPIFY API
  │ • Procesa GET (obtener actual)
  │ • Procesa PUT (actualizar)
  │ • Retorna confirmación
  ▼
RESPUESTA
  │ • Plugin retorna: "Éxito: $150.00 → $99.99"
  ▼
SEMANTIC KERNEL
  │ • Construye prompt mejorado
  │ • Prepara llamada a LLM
  │ • OAuth2 para OpenAI
  ▼
WSO2 IA GATEWAY
  │ • Valida token OAuth2
  │ • Enruta a OpenAI API
  │ • Aplica políticas
  ▼
OPENAI GPT-4o-mini
  │ • Recibe prompt vía WSO2 Gateway
  │ • Genera respuesta natural
  │ • "El precio del producto ID 123456
  │    se ha actualizado de $150.00 a $99.99"
  │ • Retorna vía WSO2 Gateway
  ▼
SEMANTIC KERNEL
  │ • Recibe respuesta formateada
  │ • Procesa y retorna
  ▼
USUARIO
  │ Recibe respuesta formateada
  └
```

---

## Diagrama 10: Sistema de Memoria de Precios

```
┌─────────────────────────────────────────────────────────────────────┐
│              SISTEMA DE MEMORIA DE PRECIOS (PriceMemory)           │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  PRICE MEMORY                                                │
│  ┌───────────────────────────────────────────────────────┐   │
│  │  price_history = {                                    │   │
│  │    "123456": {                                        │   │
│  │      "previous": "150.00",                            │   │
│  │      "current": "99.99"                               │   │
│  │    },                                                 │   │
│  │    "789012": {                                        │   │
│  │      "previous": "200.00",                            │   │
│  │      "current": "250.00"                              │   │
│  │    }                                                  │   │
│  │  }                                                    │   │
│  └───────────────────────────────────────────────────────┘   │
│                                                              │
│  OPERACIONES:                                                │
│  • remember_price_change(id, old, new)                       │
│  • get_previous_price(id)                                    │
│  • has_history(id)                                           │
│  • revert_price(id) → Restaura precio anterior              │
└─────────────────────────────────────────────────────────────┘
```

---

## Diagrama 11: ¿Qué es Semantic Kernel? (Explicación Visual)

```
┌─────────────────────────────────────────────────────────────────────┐
│              ¿QUÉ ES SEMANTIC KERNEL Y PARA QUÉ SIRVE?              │
└─────────────────────────────────────────────────────────────────────┘

PROBLEMA SIN SEMANTIC KERNEL:
┌─────────────────────────────────────────────────────────────┐
│  Usuario: "Actualiza precio de Gift Card a 200"            │
│                                                             │
│  Código tradicional necesita:                               │
│  • Parsing manual de texto                                 │
│  • Extracción manual de parámetros                         │
│  • Manejo de múltiples variaciones                         │
│  • Lógica condicional compleja                             │
│                                                             │
│  if "actualiza" in texto and "precio" in texto:            │
│      producto = extraer_producto(texto)                    │
│      precio = extraer_precio(texto)                        │
│      actualizar(producto, precio)                          │
└─────────────────────────────────────────────────────────────┘

SOLUCIÓN CON SEMANTIC KERNEL:
┌─────────────────────────────────────────────────────────────┐
│  Usuario: "Actualiza precio de Gift Card a 200"            │
│                                                             │
│  Semantic Kernel automáticamente:                          │
│  1. LLM analiza la intención                               │
│  2. LLM decide qué función llamar                          │
│  3. LLM extrae parámetros automáticamente                  │
│  4. Ejecuta la función                                     │
│  5. LLM genera respuesta natural                          │
│                                                             │
│  kernel.invoke_prompt("Actualiza precio...")                │
│  → LLM llama: update_product_price_by_name(                │
│       "Gift Card", "200")                                  │
│  → Respuesta: "Precio actualizado exitosamente"            │
└─────────────────────────────────────────────────────────────┘
```

---

## Diagrama 12: Flujo de Semantic Kernel (Ejemplo Detallado)

```
┌─────────────────────────────────────────────────────────────────────┐
│         FLUJO DE SEMANTIC KERNEL - EJEMPLO PASO A PASO              │
└─────────────────────────────────────────────────────────────────────┘

ENTRADA DEL USUARIO
┌─────────────────────────────────────┐
│ "Actualiza el precio del producto  │
│  Gift Card a 200 dólares"          │
└──────────────┬─────────────────────┘
                │
                ▼
SEMANTIC KERNEL RECIBE EL MENSAJE
┌─────────────────────────────────────┐
│ • Agrega mensaje al ChatHistory     │
│ • Prepara contexto para el LLM     │
└──────────────┬─────────────────────┘
                │
                ▼
LLM (OpenAI) ANALIZA LA INTENCIÓN
┌─────────────────────────────────────┐
│ Análisis:                           │
│ • Intención: ACTUALIZAR_PRECIO      │
│ • Entidad: producto = "Gift Card"  │
│ • Entidad: precio = "200"           │
│ • Acción necesaria: llamar función  │
└──────────────┬─────────────────────┘
                │
                ▼
LLM DECIDE QUÉ FUNCIÓN LLAMAR
┌─────────────────────────────────────┐
│ Funciones disponibles:             │
│ • update_product_price(id, price)   │
│ • update_product_price_by_name(...) │ ← SELECCIONA ESTA
│ • get_products_list()               │
│ • count_products()                  │
└──────────────┬─────────────────────┘
                │
                ▼
LLM EXTRAE PARÁMETROS
┌─────────────────────────────────────┐
│ Parámetros extraídos:              │
│ • product_name = "Gift Card"       │
│ • new_price = "200"                 │
└──────────────┬─────────────────────┘
                │
                ▼
SEMANTIC KERNEL EJECUTA LA FUNCIÓN
┌─────────────────────────────────────┐
│ shopify_plugin.update_product_     │
│   price_by_name("Gift Card", "200") │
│                                     │
│ → Busca producto por nombre        │
│ → Obtiene ID del producto          │
│ → Actualiza precio vía WSO2        │
│ → Retorna: "Éxito: $150 → $200"   │
└──────────────┬─────────────────────┘
                │
                ▼
LLM RECIBE RESULTADO Y GENERA RESPUESTA
┌─────────────────────────────────────┐
│ Resultado recibido:                 │
│ "Éxito: Precio actualizado de       │
│  $150.00 a $200.00"                 │
│                                     │
│ LLM genera respuesta natural:       │
│ "El precio del producto Gift Card  │
│  se ha actualizado exitosamente    │
│  de $150.00 a $200.00."             │
└──────────────┬─────────────────────┘
                │
                ▼
RESPUESTA AL USUARIO
┌─────────────────────────────────────┐
│ "El precio del producto Gift Card  │
│  se ha actualizado exitosamente    │
│  de $150.00 a $200.00."             │
└─────────────────────────────────────┘
```

---

## Diagrama 13: Ventajas de Semantic Kernel

```
┌─────────────────────────────────────────────────────────────────────┐
│                    VENTAJAS DE SEMANTIC KERNEL                     │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  1. NO NECESITAS PARSING MANUAL                             │
│  ┌───────────────────────────────────────────────────────┐   │
│  │ Entiende múltiples formas de expresar lo mismo:      │   │
│  │ • "Actualiza precio de X a Y"                        │   │
│  │ • "Cambia el precio de X a Y"                        │   │
│  │ • "Modifica precio de X a Y"                         │   │
│  │ • "Pon el precio de X en Y"                          │   │
│  │ • "Update price of X to Y" (inglés también)         │   │
│  └───────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  2. EXTRACCIÓN AUTOMÁTICA DE PARÁMETROS                     │
│  ┌───────────────────────────────────────────────────────┐   │
│  │ El LLM identifica automáticamente:                  │   │
│  │ • Qué es el nombre del producto                      │   │
│  │ • Qué es el precio                                    │   │
│  │ • Qué es el ID                                        │   │
│  │ • Qué operación realizar                             │   │
│  └───────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  3. MANEJO DE CONTEXTO                                      │
│  ┌───────────────────────────────────────────────────────┐   │
│  │ Usuario: "Lista los productos"                       │   │
│  │ Sistema: [Muestra lista]                               │   │
│  │ Usuario: "Actualiza el primero a 100"                │   │
│  │ Sistema: [Entiende "el primero" = primer producto]   │   │
│  └───────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  4. COMPOSICIÓN DE FUNCIONES                                │
│  ┌───────────────────────────────────────────────────────┐   │
│  │ Usuario: "Busca el producto más caro y reduce 10%"  │   │
│  │ → LLM llama: get_products_sorted("desc")            │   │
│  │ → LLM llama: update_product_price_with_math(         │   │
│  │     id, "percent_reduce", 10)                         │   │
│  └───────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  5. MANEJO INTELIGENTE DE ERRORES                            │
│  ┌───────────────────────────────────────────────────────┐   │
│  │ Si una función falla, el LLM puede:                 │   │
│  │ • Intentar otra estrategia                           │   │
│  │ • Sugerir alternativas                               │   │
│  │ • Explicar el error de forma natural                 │   │
│  └───────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## Diagrama 14: Componentes del Agente Python - Explicación Detallada

```
┌─────────────────────────────────────────────────────────────────────┐
│         COMPONENTES DEL AGENTE PYTHON - FUNCIONALIDADES             │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  1. DETECCIÓN DE INTENCIONES (Intent Detection)            │
│  ┌───────────────────────────────────────────────────────┐   │
│  │                                                      │   │
│  │  ¿QUÉ HACE?                                         │   │
│  │  Analiza el texto del usuario para identificar      │   │
│  │  qué acción quiere realizar                         │   │
│  │                                                      │   │
│  │  CÓMO FUNCIONA:                                      │   │
│  │  • Usa diccionarios de palabras clave               │   │
│  │  • Detecta patrones con regex                      │   │
│  │  • Funciona en español e inglés                     │   │
│  │  • Extrae parámetros automáticamente                │   │
│  │                                                      │   │
│  │  EJEMPLO:                                            │   │
│  │  Usuario: "Actualiza precio ID 123456 a 99.99"     │   │
│  │  → Detecta: 'update_price'                          │   │
│  │  → Extrae: ID=123456, precio=99.99                 │   │
│  │                                                      │   │
│  │  Palabras clave detectadas:                         │   │
│  │  • Listar: ['productos', 'lista', 'mostrar', ...]  │   │
│  │  • Actualizar: ['actualizar', 'cambiar', ...]      │   │
│  │  • Contar: ['cuántos', 'cantidad', ...]            │   │
│  │  • Operaciones: ['añadir', 'sumar', 'restar', ...] │   │
│  └───────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  2. PRICE MEMORY (Memoria de Precios)                      │
│  ┌───────────────────────────────────────────────────────┐   │
│  │                                                      │   │
│  │  ¿QUÉ HACE?                                         │   │
│  │  Guarda el historial de cambios de precio para      │   │
│  │  permitir revertir cambios                          │   │
│  │                                                      │   │
│  │  CÓMO FUNCIONA:                                      │   │
│  │  • Al actualizar precio, guarda precio anterior    │   │
│  │  • Mantiene diccionario en memoria                  │   │
│  │  • Permite consultar precio anterior                │   │
│  │  • Permite revertir cambios                         │   │
│  │                                                      │   │
│  │  ESTRUCTURA DE DATOS:                                │   │
│  │  price_history = {                                   │   │
│  │    "123456": {                                       │   │
│  │      "previous": "150.00",                          │   │
│  │      "current": "99.99"                             │   │
│  │    }                                                 │   │
│  │  }                                                   │   │
│  │                                                      │   │
│  │  EJEMPLO:                                            │   │
│  │  1. Usuario: "Actualiza ID 123456 a 99.99"         │   │
│  │     → Guarda: previous=$150.00, current=$99.99     │   │
│  │                                                      │   │
│  │  2. Usuario: "Vuelve precio original ID 123456"    │   │
│  │     → Consulta: get_previous_price("123456")        │   │
│  │     → Retorna: "150.00"                             │   │
│  │     → Restaura precio a $150.00                     │   │
│  └───────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  3. THINKING INDICATOR (Indicador de Progreso)             │
│  ┌───────────────────────────────────────────────────────┐   │
│  │                                                      │   │
│  │  ¿QUÉ HACE?                                         │   │
│  │  Muestra indicador visual animado mientras         │   │
│  │  procesa la consulta                                │   │
│  │                                                      │   │
│  │  CÓMO FUNCIONA:                                      │   │
│  │  • Se activa al inicio del procesamiento            │   │
│  │  • Muestra animación: "Pensando...", "Pensando...."│   │
│  │  • Se ejecuta en hilo separado                      │   │
│  │  • Se detiene cuando termina                        │   │
│  │                                                      │   │
│  │  EJEMPLO VISUAL:                                     │   │
│  │  Usuario: "Lista los productos"                    │   │
│  │  → Muestra: "Pensando..." (animado)                 │   │
│  │  → [Procesando...]                                  │   │
│  │  → [Obteniendo datos...]                           │   │
│  │  → Oculta: "Pensando..."                            │   │
│  │  → Muestra: "Productos encontrados..."              │   │
│  │                                                      │   │
│  │  VENTAJAS:                                          │   │
│  │  • Mejor experiencia de usuario                     │   │
│  │  • Feedback visual inmediato                        │   │
│  │  • Evita sensación de sistema "congelado"          │   │
│  └───────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## Diagrama 15: Flujo de Detección de Intenciones

```
┌─────────────────────────────────────────────────────────────────────┐
│              FLUJO DE DETECCIÓN DE INTENCIONES                     │
└─────────────────────────────────────────────────────────────────────┘

USUARIO ENVÍA CONSULTA
┌─────────────────────────────────────┐
│ "Actualiza precio ID 123456 a 99.99"│
└──────────────┬─────────────────────┘
               │
               ▼
AGENTE PYTHON RECIBE TEXTO
┌─────────────────────────────────────┐
│ • Convierte a minúsculas            │
│ • Prepara para análisis              │
└──────────────┬─────────────────────┘
               │
               ▼
ANÁLISIS DE PALABRAS CLAVE
┌─────────────────────────────────────┐
│ Busca en diccionarios:              │
│                                     │
│ UPDATE_PRICE keywords:              │
│ ['actualizar', 'cambiar', 'modificar',│
│  'update', 'change', 'modify']      │
│                                     │
│ ✓ Encontrado: "actualiza"           │
└──────────────┬─────────────────────┘
               │
               ▼
DETECCIÓN DE PATRONES (REGEX)
┌─────────────────────────────────────┐
│ Patrones de precio:                 │
│ • r'id[:\s]*(\d+)'                  │
│ • r'a\s+[\$€]?\d+'                  │
│ • r'precio\s+[\$€]?\d+'             │
│                                     │
│ ✓ Encontrado: ID=123456             │
│ ✓ Encontrado: precio=99.99          │
└──────────────┬─────────────────────┘
               │
               ▼
RESULTADO DE DETECCIÓN
┌─────────────────────────────────────┐
│ Intención: UPDATE_PRICE              │
│ Parámetros extraídos:                │
│ • product_id = "123456"              │
│ • new_price = "99.99"                │
│ • product_name = None                │
│ • math_operation = None              │
└──────────────┬─────────────────────┘
               │
               ▼
EJECUCIÓN DE FUNCIÓN
┌─────────────────────────────────────┐
│ shopify_plugin.update_product_price( │
│   "123456", "99.99")                │
└─────────────────────────────────────┘
```

---

## Diagrama 16: Flujo de PriceMemory

```
┌─────────────────────────────────────────────────────────────────────┐
│                    FLUJO DE PRICE MEMORY                           │
└─────────────────────────────────────────────────────────────────────┘

ESCENARIO 1: ACTUALIZAR PRECIO
┌─────────────────────────────────────────────────────────────┐
│ Usuario: "Actualiza precio ID 123456 a 99.99"             │
│                                                             │
│ 1. Sistema obtiene precio actual: $150.00                 │
│ 2. Actualiza precio a $99.99                               │
│ 3. PriceMemory guarda automáticamente:                    │
│                                                             │
│    price_history["123456"] = {                              │
│      "previous": "150.00",                                 │
│      "current": "99.99"                                     │
│    }                                                        │
│                                                             │
│ 4. Confirmación: "Precio actualizado de $150.00 a $99.99" │
└─────────────────────────────────────────────────────────────┘

ESCENARIO 2: REVERTIR PRECIO
┌─────────────────────────────────────────────────────────────┐
│ Usuario: "Vuelve precio original del ID 123456"            │
│                                                             │
│ 1. Sistema consulta PriceMemory:                          │
│    → has_history("123456") = True                          │
│    → get_previous_price("123456") = "150.00"               │
│                                                             │
│ 2. Sistema restaura precio:                                │
│    → update_product_price("123456", "150.00")              │
│                                                             │
│ 3. PriceMemory actualiza:                                  │
│    price_history["123456"] = {                              │
│      "previous": "99.99",   (ahora es el anterior)        │
│      "current": "150.00"    (precio restaurado)            │
│    }                                                        │
│                                                             │
│ 4. Confirmación: "Precio restaurado a $150.00"            │
└─────────────────────────────────────────────────────────────┘

ESTADO DE LA MEMORIA
┌─────────────────────────────────────────────────────────────┐
│ price_history = {                                           │
│   "123456": {                                               │
│     "previous": "150.00",                                   │
│     "current": "99.99"                                      │
│   },                                                         │
│   "789012": {                                               │
│     "previous": "200.00",                                   │
│     "current": "250.00"                                     │
│   }                                                          │
│ }                                                            │
│                                                              │
│ Operaciones disponibles:                                    │
│ • remember_price_change(id, old, new)                       │
│ • get_previous_price(id)                                    │
│ • has_history(id)                                           │
│ • revert_price(id)                                           │
└─────────────────────────────────────────────────────────────┘
```

---

## Diagrama 17: Flujo de ThinkingIndicator

```
┌─────────────────────────────────────────────────────────────────────┐
│                  FLUJO DE THINKING INDICATOR                       │
└─────────────────────────────────────────────────────────────────────┘

INICIO DEL PROCESAMIENTO
┌─────────────────────────────────────┐
│ Usuario: "Lista los productos"     │
└──────────────┬─────────────────────┘
               │
               ▼
THINKING INDICATOR SE ACTIVA
┌─────────────────────────────────────┐
│ thinking = ThinkingIndicator(       │
│   "Processing query")               │
│ thinking.start()                    │
│                                     │
│ Pantalla muestra:                   │
│ "Processing query..." (animado)    │
│                                     │
│ [Hilo separado ejecuta animación]  │
└──────────────┬─────────────────────┘
               │
               ▼
PROCESAMIENTO EN PARALELO
┌─────────────────────────────────────┐
│ [Hilo 1: Animación]                 │
│ "Processing query..."               │
│ "Processing query...."              │
│ "Processing query....."             │
│ "Processing query...."              │
│ (ciclo continuo)                    │
│                                     │
│ [Hilo 2: Procesamiento]             │
│ • Detectar intención                 │
│ • Llamar a Shopify                   │
│ • Obtener datos                      │
│ • Generar respuesta                  │
└──────────────┬─────────────────────┘
               │
               ▼
FINALIZACIÓN
┌─────────────────────────────────────┐
│ thinking.stop()                      │
│                                     │
│ • Detiene animación                  │
│ • Limpia línea                       │
│ • Muestra respuesta                  │
│                                     │
│ Pantalla muestra:                   │
│ "Productos encontrados (5 total):   │
│  - ID: 123456 - Gift Card - $150.00"│
└─────────────────────────────────────┘

EJEMPLO VISUAL COMPLETO
┌─────────────────────────────────────┐
│ Usuario: Lista los productos       │
│                                     │
│ Sistema: Processing query...        │
│          Processing query....       │
│          Processing query.....      │
│          Processing query....       │
│                                     │
│ Sistema: [Limpia línea]            │
│                                     │
│ Sistema: Productos encontrados:     │
│          - ID: 123456 - Gift Card   │
│          - ID: 789012 - Snowboard   │
└─────────────────────────────────────┘
```

---

## Instrucciones para PowerPoint

### Colores Sugeridos:
- **Usuario**: Azul claro (#E3F2FD)
- **Agente Python**: Verde (#C8E6C9)
- **Semantic Kernel**: Púrpura (#E1BEE7)
- **OpenAI**: Naranja (#FFE0B2)
- **WSO2 Gateway**: Rojo/Naranja (#FFCCBC)
- **Shopify**: Verde esmeralda (#B2DFDB)

### Tipografía:
- Títulos: Arial Bold, 24pt
- Subtítulos: Arial Bold, 18pt
- Texto: Arial Regular, 14pt
- Código: Courier New, 12pt

### Animaciones Sugeridas:
- Entrada de componentes: Aparecer uno por uno
- Flujos: Flechas animadas siguiendo el orden
- Resaltar: Componente activo con efecto de brillo

### Transiciones:
- Entre diapositivas: Desvanecer suave
- Entre secciones: Cortina vertical

---

**Documento de diagramas para presentación PowerPoint**  
**Versión**: 1.0  
**Fecha**: 2024

