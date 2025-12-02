# Documento Arquitectónico: Agente IA para Ecommerce con WSO2

## Visión General del Sistema

Este documento describe la arquitectura completa del **Sample AI Agent** que integra Microsoft Semantic Kernel, WSO2 API Manager y Shopify API para proporcionar una interfaz de lenguaje natural para la gestión de tiendas de ecommerce.

---

## Componentes del Sistema

### 1. **Usuario/Cliente**
- **Rol**: Interfaz de usuario final
- **Responsabilidad**: Enviar consultas en lenguaje natural (español/inglés)
- **Ejemplos de consultas**:
  - "Lista los productos"
  - "Actualiza el precio del producto ID 123456 a 99.99"
  - "¿Cuántos productos hay?"
  - "Muestra productos ordenados de menor a mayor precio"

### 2. **Agente Python (agent_gpt4.py)**
- **Rol**: Orquestador principal y punto de entrada
- **Tecnología**: Python 3.8+
- **Responsabilidades**:
  - Recibir y procesar entrada del usuario
  - Gestionar el ciclo de vida de la aplicación
  - Coordinar entre Semantic Kernel y plugins
  - Manejar el historial de conversación
  - Proporcionar indicadores de progreso visual
  - Sistema de memoria de precios (PriceMemory)
  - Detección de intenciones mejorada (bilingüe)

#### Componentes Clave del Agente Python:

##### 1. **Detección de Intenciones (Intent Detection)**

**¿Qué hace?**
Analiza el texto del usuario para identificar automáticamente qué acción quiere realizar, antes de que Semantic Kernel procese la consulta.

**Cómo funciona:**
- Utiliza diccionarios de palabras clave en español e inglés
- Detecta patrones usando expresiones regulares (regex)
- Identifica múltiples formas de expresar la misma intención
- Extrae parámetros automáticamente (IDs, precios, nombres de productos)

**Ejemplos de detección:**

```python
# Intención: LISTAR PRODUCTOS
Palabras clave detectadas: ['productos', 'lista', 'catálogo', 'mostrar', 'ver', 
                           'products', 'list', 'catalog', 'show', 'display']
Usuario dice: "Lista los productos" → Detecta: 'list'
Usuario dice: "Muéstrame el catálogo" → Detecta: 'list'
Usuario dice: "Show products" → Detecta: 'list'

# Intención: ACTUALIZAR PRECIO
Palabras clave detectadas: ['actualizar', 'cambiar', 'modificar', 'update', 
                           'change', 'modify', 'set']
Patrones de precio: r'a\s+[\$€]?\d+', r'precio\s+[\$€]?\d+', r'to\s+[\$€]?\d+'
Usuario dice: "Actualiza precio ID 123456 a 99.99" 
→ Detecta: 'update_price', extrae: ID=123456, precio=99.99

Usuario dice: "Cambia el precio de Gift Card a 200"
→ Detecta: 'update_price', extrae: nombre="Gift Card", precio=200

# Intención: OPERACIONES MATEMÁTICAS
Palabras clave: ['añadir', 'sumar', 'restar', 'aumentar', 'incrementar', 
                'add', 'subtract', 'increase']
Usuario dice: "Añade 1000 al precio de X"
→ Detecta: 'update_price', operación='add', valor=1000

Usuario dice: "Incrementa un 10% el precio"
→ Detecta: 'update_price', operación='percent_increase', valor=10
```

**Ventajas:**
- **Bilingüe**: Funciona en español e inglés
- **Flexible**: Entiende múltiples formas de expresar lo mismo
- **Preciso**: Extrae parámetros automáticamente usando regex
- **Rápido**: Procesa antes de enviar a Semantic Kernel, optimizando el flujo

##### 2. **PriceMemory (Memoria de Precios)**

**¿Qué hace?**
Sistema de memoria que guarda el historial de cambios de precio para cada producto, permitiendo revertir cambios y mantener un registro de modificaciones.

**Cómo funciona:**
- Al actualizar un precio, guarda automáticamente el precio anterior y el nuevo
- Mantiene un diccionario en memoria: `{product_id: {previous: precio_anterior, current: precio_actual}}`
- Permite consultar el precio anterior de cualquier producto
- Permite revertir cambios restaurando el precio anterior

**Ejemplo práctico:**

```python
# Usuario actualiza precio
Usuario: "Actualiza precio ID 123456 a 99.99"
Sistema ejecuta: update_product_price("123456", "99.99")

# PriceMemory automáticamente guarda:
price_history = {
    "123456": {
        "previous": "150.00",  # Precio anterior
        "current": "99.99"      # Precio nuevo
    }
}

# Más tarde, usuario quiere revertir
Usuario: "Vuelve el precio original del ID 123456"
Sistema consulta PriceMemory:
→ get_previous_price("123456") retorna "150.00"
→ Ejecuta: update_product_price("123456", "150.00")
→ Respuesta: "Precio restaurado a $150.00"
```

**Operaciones disponibles:**
- `remember_price_change(id, old_price, new_price)`: Guarda un cambio
- `get_previous_price(id)`: Obtiene el precio anterior
- `has_history(id)`: Verifica si hay historial para un producto
- `revert_price(id)`: Restaura el precio anterior

**Ventajas:**
- **Historial de cambios**: Mantiene registro de todas las modificaciones
- **Reversión fácil**: Permite deshacer cambios con un comando simple
- **Sesión persistente**: El historial se mantiene durante toda la sesión
- **Sin base de datos**: Almacenamiento en memoria (rápido y simple)

##### 3. **ThinkingIndicator (Indicador de Progreso)**

**¿Qué hace?**
Muestra un indicador visual animado ("Pensando...") mientras el sistema procesa la consulta del usuario, mejorando la experiencia de usuario.

**Cómo funciona:**
- Se activa automáticamente cuando comienza el procesamiento
- Muestra una animación de puntos: "Pensando...", "Pensando....", "Pensando....", etc.
- Se ejecuta en un hilo separado (no bloquea el procesamiento)
- Se detiene automáticamente cuando la respuesta está lista

**Ejemplo visual:**

```
Usuario: "Lista los productos"
         │
         ▼
Sistema muestra: "Pensando..." (con puntos animados)
         │
         ▼
[Procesando consulta...]
[Obteniendo datos de Shopify...]
[Generando respuesta...]
         │
         ▼
Sistema oculta: "Pensando..."
         │
         ▼
Respuesta: "Productos encontrados (5 total):
           - ID: 123456 - Gift Card - $150.00
           - ID: 789012 - Snowboard - $500.00
           ..."
```

**Características:**
- **Animación suave**: Puntos que aparecen y desaparecen cíclicamente
- **No intrusivo**: Solo se muestra cuando es necesario (no en modo debug)
- **Auto-limpieza**: Limpia la línea cuando termina
- **Thread-safe**: No interfiere con el procesamiento principal

**Código de ejemplo:**

```python
# Al inicio del procesamiento
thinking = ThinkingIndicator("Processing query")
thinking.start()  # Muestra "Processing query..."

# ... procesamiento ...

# Al finalizar
thinking.stop()  # Oculta el indicador y limpia la línea
print("Respuesta: ...")
```

**Ventajas:**
- **Mejor UX**: El usuario sabe que el sistema está trabajando
- **Feedback visual**: Evita que el usuario piense que el sistema se "congeló"
- **Profesional**: Da sensación de sistema activo y responsivo
- **Configurable**: Se puede desactivar en modo debug para ver detalles técnicos

### 3. **Microsoft Semantic Kernel**
- **Rol**: Framework de orquestación de IA
- **Tecnología**: Microsoft Semantic Kernel SDK (Python)
- **Responsabilidades**:
  - Conectar el LLM con funciones ejecutables
  - Gestionar el contexto de conversación (ChatHistory)
  - Enrutar intenciones del usuario a funciones apropiadas
  - Proporcionar sistema de plugins extensible
  - Manejar prompts y respuestas del LLM
  - Validar y ejecutar funciones decoradas con `@kernel_function`

#### ¿Qué es Semantic Kernel y para qué sirve?

**Microsoft Semantic Kernel** es un framework de código abierto desarrollado por Microsoft que permite crear agentes de IA capaces de combinar el poder del procesamiento de lenguaje natural (LLM) con funciones ejecutables escritas en código tradicional (Python, C#, Java, etc.).

**Problema que resuelve:**
- Los LLMs como ChatGPT son excelentes para entender lenguaje natural, pero no pueden ejecutar código directamente
- Necesitas una forma de conectar las intenciones del usuario (expresadas en lenguaje natural) con acciones reales (llamadas a APIs, operaciones de base de datos, etc.)
- Semantic Kernel actúa como el "puente" entre el lenguaje natural y las funciones ejecutables

**Funcionalidades principales:**

1. **Function Calling**: Permite que el LLM decida cuándo y cómo llamar funciones de Python
2. **Plugin System**: Organiza funciones relacionadas en plugins reutilizables
3. **Context Management**: Mantiene el historial de conversación para contexto coherente
4. **Prompt Engineering**: Facilita la construcción y mejora de prompts para el LLM
5. **Multi-LLM Support**: Puede trabajar con OpenAI, Azure OpenAI, o otros proveedores

#### Ejemplo práctico en nuestro proyecto:

**Escenario:** Usuario dice: *"Actualiza el precio del producto Gift Card a 200 dólares"*

**Sin Semantic Kernel (enfoque tradicional):**
```python
# Tendrías que hacer parsing manual:
if "actualiza" in user_input and "precio" in user_input:
    # Extraer manualmente el nombre del producto
    # Extraer manualmente el precio
    # Buscar el producto
    # Actualizar el precio
    # Formatear respuesta
```

**Con Semantic Kernel:**

**Paso 1:** Definimos funciones como plugins:
```python
class ShopifyPlugin:
    @kernel_function(name="update_product_price_by_name", 
                     description="Actualiza el precio de un producto usando su nombre")
    def update_product_price_by_name(self, product_name: str, new_price: str) -> str:
        # Esta función se ejecuta automáticamente cuando el LLM la necesita
        search_result = self.find_product_by_name(product_name)
        if search_result['found']:
            return self.update_product_price(search_result['id'], new_price)
        return f"Error: Producto '{product_name}' no encontrado"
```

**Paso 2:** Registramos el plugin con Semantic Kernel:
```python
kernel = sk.Kernel()
kernel.add_service(OpenAIChatCompletion(...))  # Conecta OpenAI
kernel.add_plugin(shopify_plugin, plugin_name="Shopify")  # Registra funciones
```

**Paso 3:** El LLM decide automáticamente qué hacer:
```python
# Usuario: "Actualiza el precio del producto Gift Card a 200 dólares"

# Semantic Kernel automáticamente:
# 1. El LLM analiza la intención
# 2. El LLM decide que necesita llamar a update_product_price_by_name()
# 3. El LLM extrae los parámetros: product_name="Gift Card", new_price="200"
# 4. Semantic Kernel ejecuta la función
# 5. El LLM recibe el resultado y genera una respuesta natural
```

**Flujo completo:**

```
Usuario: "Actualiza precio de Gift Card a 200"
    │
    ▼
Semantic Kernel recibe el mensaje
    │
    ▼
LLM (OpenAI) analiza: "Necesito actualizar un precio"
    │
    ▼
LLM decide: "Debo llamar a update_product_price_by_name()"
    │
    ▼
LLM extrae parámetros: product_name="Gift Card", new_price="200"
    │
    ▼
Semantic Kernel ejecuta: shopify_plugin.update_product_price_by_name("Gift Card", "200")
    │
    ▼
Función busca el producto y actualiza el precio vía WSO2 Gateway
    │
    ▼
Resultado: "Éxito: Precio actualizado de $150.00 a $200.00"
    │
    ▼
LLM recibe el resultado y genera respuesta natural:
"El precio del producto Gift Card se ha actualizado exitosamente de $150.00 a $200.00"
    │
    ▼
Usuario recibe respuesta formateada
```

**Ventajas de usar Semantic Kernel:**

1. **No necesitas parsing manual**: El LLM entiende múltiples formas de expresar lo mismo
   - "Actualiza precio de X a Y"
   - "Cambia el precio de X a Y"
   - "Modifica el precio de X a Y"
   - "Pon el precio de X en Y"

2. **Extracción automática de parámetros**: El LLM identifica automáticamente qué es el nombre del producto y qué es el precio

3. **Manejo de contexto**: Semantic Kernel mantiene el historial de conversación
   ```
   Usuario: "Lista los productos"
   Sistema: [Lista productos]
   Usuario: "Actualiza el primero a 100"
   Sistema: [Entiende "el primero" se refiere al primer producto de la lista anterior]
   ```

4. **Composición de funciones**: El LLM puede llamar múltiples funciones en secuencia
   ```
   Usuario: "Busca el producto más caro y reduce su precio un 10%"
   → LLM llama: get_products_sorted("desc") 
   → LLM llama: update_product_price_with_math(id, "percent_reduce", 10)
   ```

5. **Manejo de errores inteligente**: Si una función falla, el LLM puede intentar otra estrategia
   ```
   Usuario: "Actualiza precio de X a 200"
   → update_product_price_by_name("X") falla (no encontrado)
   → LLM puede sugerir: "No encontré 'X', ¿quisiste decir 'Gift Card'?"
   ```

**En resumen:** Semantic Kernel permite que el LLM "piense" y "decida" qué funciones ejecutar basándose en la intención del usuario, en lugar de tener que programar manualmente todas las posibles combinaciones de comandos.

### 4. **OpenAI GPT-4o-mini (LLM) vía WSO2 IA Gateway**
- **Rol**: Motor de procesamiento de lenguaje natural
- **Tecnología**: OpenAI API (modelo gpt-4o-mini) accedido a través de WSO2 IA Gateway
- **Acceso**: Todas las llamadas al LLM pasan por WSO2 API Gateway (no acceso directo)
- **Responsabilidades**:
  - Interpretar consultas en lenguaje natural
  - Entender la intención del usuario
  - Generar respuestas naturales y contextualizadas
  - Procesar datos de Shopify y formatearlos para el usuario
  - Sistema anti-alucinación (solo datos reales)

### 5. **WSO2 API Gateway**
- **Rol**: Gateway empresarial y punto de seguridad centralizado
- **Tecnología**: WSO2 API Manager
- **Responsabilidades**:
  - Autenticación OAuth2 (Client Credentials)
  - Enrutamiento de peticiones a servicios externos:
    - **Shopify API** (contexto: `/shopify/1.0.0`)
    - **OpenAI/ChatGPT API** (IA Gateway)
  - Gestión de tokens de acceso
  - Políticas de seguridad y rate limiting
  - Transformación de headers
  - Centralización de todas las llamadas externas
  - Monitoreo y logging de todas las APIs

### 6. **Shopify API**
- **Rol**: Backend de ecommerce
- **Tecnología**: Shopify Admin REST API
- **Responsabilidades**:
  - Gestión de productos
  - Consulta y actualización de precios
  - Búsqueda de productos por ID o nombre
  - Operaciones CRUD sobre catálogo
  - Endpoints utilizados:
    - `GET /products.json` - Listar productos
    - `GET /products/{id}.json` - Obtener producto específico
    - `GET /products/count.json` - Contar productos
    - `PUT /products/{id}.json` - Actualizar producto

### 7. **Plugin de Shopify (ShopifyPlugin)**
- **Rol**: Capa de abstracción entre Semantic Kernel y Shopify
- **Tecnología**: Clase Python con decoradores `@kernel_function`
- **Funciones expuestas al LLM**:
  - `get_products_list()` - Lista todos los productos
  - `get_products_sorted(order)` - Productos ordenados por precio
  - `count_products()` - Cuenta total de productos
  - `find_product_by_name(name)` - Búsqueda por nombre con fuzzy matching
  - `update_product_price(id, price)` - Actualizar precio por ID
  - `update_product_price_by_name(name, price)` - Actualizar precio por nombre
  - `update_product_price_with_math(id, operation, value)` - Operaciones matemáticas
  - `revert_price(id)` - Restaurar precio anterior

---

## Flujo Completo de una Llamada

### Escenario: Usuario solicita "Actualiza el precio del producto ID 123456 a 99.99"

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        FLUJO DE UNA LLAMADA COMPLETA                    │
└─────────────────────────────────────────────────────────────────────────┘

1. ENTRADA DEL USUARIO
   ┌─────────────┐
   │   Usuario   │
   │  "Actualiza │
   │   el precio │
   │   del ID    │
   │   123456 a  │
   │   99.99"    │
   └──────┬──────┘
          │
          ▼
2. AGENTE PYTHON (agent_gpt4.py)
   ┌─────────────────────────────────────┐
   │  • Recibe entrada del usuario       │
   │  • Inicia ThinkingIndicator         │
   │  • Detecta intención: UPDATE_PRICE  │
   │  • Extrae parámetros:                │
   │    - product_id: "123456"           │
   │    - new_price: "99.99"             │
   └──────┬──────────────────────────────┘
          │
          ▼
3. MICROSOFT SEMANTIC KERNEL
   ┌─────────────────────────────────────┐
   │  • Agrega mensaje al ChatHistory    │
   │  • Prepara prompt mejorado           │
   │  • Enruta a función apropiada        │
   │  • Invoca plugin de Shopify          │
   └──────┬──────────────────────────────┘
          │
          ▼
4. PLUGIN SHOPIFY (ShopifyPlugin)
   ┌─────────────────────────────────────┐
   │  • update_product_price() ejecutado │
   │  • PASO 1: Obtener precio actual    │
   │    - Llama a _make_api_call()       │
   └──────┬──────────────────────────────┘
          │
          ▼
5. AUTENTICACIÓN CON WSO2 (OAuth2)
   ┌─────────────────────────────────────┐
   │  • _get_wso2_access_token()         │
   │  • POST a WSO2_TOKEN_ENDPOINT        │
   │  • Headers:                          │
   │    Authorization: Basic {creds}      │
   │  • Payload: grant_type=client_       │
   │    credentials                       │
   │  • Respuesta: access_token           │
   └──────┬──────────────────────────────┘
          │
          ▼
6. LLAMADA A SHOPIFY VÍA WSO2 GATEWAY
   ┌─────────────────────────────────────┐
   │  • URL: {WSO2_GW_URL}/shopify/      │
   │    1.0.0/products/123456.json       │
   │  • Método: GET (obtener actual)     │
   │  • Headers:                         │
   │    Authorization: Bearer {token}    │
   │    X-Shopify-Access-Token: {token}  │
   └──────┬──────────────────────────────┘
          │
          ▼
7. WSO2 API GATEWAY
   ┌─────────────────────────────────────┐
   │  • Valida token OAuth2               │
   │  • Aplica políticas de seguridad     │
   │  • Enruta a backend de Shopify       │
   │  • Transforma headers                │
   │  • Proxy de petición                 │
   └──────┬──────────────────────────────┘
          │
          ▼
8. SHOPIFY API
   ┌─────────────────────────────────────┐
   │  • Valida token de Shopify           │
   │  • Obtiene producto ID 123456        │
   │  • Retorna precio actual: $150.00    │
   └──────┬──────────────────────────────┘
          │
          ▼
9. RESPUESTA HACIA ATRÁS (GET)
   ┌─────────────────────────────────────┐
   │  WSO2 Gateway ← Shopify API         │
   │  • Respuesta JSON con producto       │
   │  • Precio actual: $150.00            │
   └──────┬──────────────────────────────┘
          │
          ▼
10. PLUGIN SHOPIFY (Continuación)
    ┌─────────────────────────────────────┐
    │  • Guarda precio anterior: $150.00  │
    │  • PASO 2: Preparar actualización   │
    │  • Obtiene variant_id                │
    │  • Construye payload:                │
    │    {                                 │
    │      "product": {                    │
    │        "id": 123456,                 │
    │        "variants": [{                │
    │          "id": variant_id,            │
    │          "price": "99.99"            │
    │        }]                            │
    │      }                               │
    │    }                                 │
    └──────┬──────────────────────────────┘
           │
           ▼
11. AUTENTICACIÓN CON WSO2 (OAuth2) - Reutiliza token
    ┌─────────────────────────────────────┐
    │  • Usa token existente o renueva     │
    └──────┬──────────────────────────────┘
           │
           ▼
12. LLAMADA UPDATE A SHOPIFY VÍA WSO2
    ┌─────────────────────────────────────┐
    │  • URL: {WSO2_GW_URL}/shopify/       │
    │    1.0.0/products/123456.json       │
    │  • Método: PUT                       │
    │  • Headers:                          │
    │    Authorization: Bearer {token}     │
    │    X-Shopify-Access-Token: {token}   │
    │    Content-Type: application/json    │
    │  • Body: payload JSON                │
    └──────┬──────────────────────────────┘
           │
           ▼
13. WSO2 API GATEWAY
    ┌─────────────────────────────────────┐
    │  • Valida token                      │
    │  • Aplica políticas                  │
    │  • Enruta PUT a Shopify              │
    └──────┬──────────────────────────────┘
           │
           ▼
14. SHOPIFY API (Actualización)
    ┌─────────────────────────────────────┐
    │  • Actualiza precio a $99.99         │
    │  • Retorna producto actualizado      │
    │  • Confirma nuevo precio: $99.99     │
    └──────┬──────────────────────────────┘
           │
           ▼
15. RESPUESTA HACIA ATRÁS (PUT)
    ┌─────────────────────────────────────┐
    │  WSO2 Gateway ← Shopify API         │
    │  • Respuesta JSON con producto       │
    │  • Precio confirmado: $99.99         │
    └──────┬──────────────────────────────┘
           │
           ▼
16. PLUGIN SHOPIFY (Validación)
    ┌─────────────────────────────────────┐
    │  • Verifica respuesta                │
    │  • Compara precio enviado vs         │
    │    recibido                          │
    │  • Guarda en PriceMemory:            │
    │    previous: $150.00                 │
    │    current: $99.99                   │
    │  • Retorna mensaje de éxito          │
    └──────┬──────────────────────────────┘
           │
           ▼
17. SEMANTIC KERNEL (Procesamiento)
    ┌─────────────────────────────────────┐
    │  • Recibe datos de Shopify           │
    │  • Construye prompt mejorado:        │
    │    "ACTUALIZACIÓN EXITOSA            │
    │     CONFIRMADA: ..."                 │
    │  • Prepara llamada a LLM             │
    └──────┬──────────────────────────────┘
           │
           │ POST /openai/v1/chat/completions
           │ Headers: Authorization: Bearer {token}
           ▼
17a. AUTENTICACIÓN CON WSO2 (OAuth2) - Para OpenAI
    ┌─────────────────────────────────────┐
    │  • Obtiene token OAuth2              │
    │  • (Puede reutilizar token existente)│
    └──────┬──────────────────────────────┘
           │
           ▼
17b. LLAMADA A OPENAI VÍA WSO2 IA GATEWAY
    ┌─────────────────────────────────────┐
    │  • URL: {WSO2_GW_URL}/openai/...     │
    │  • Método: POST                      │
    │  • Headers:                           │
    │    Authorization: Bearer {wso2_token} │
    │  • Body: prompt JSON                  │
    └──────┬──────────────────────────────┘
           │
           ▼
17c. WSO2 IA GATEWAY
    ┌─────────────────────────────────────┐
    │  • Valida token OAuth2               │
    │  • Aplica políticas de seguridad     │
    │  • Enruta a OpenAI API               │
    │  • Transforma headers si necesario   │
    └──────┬──────────────────────────────┘
           │
           ▼
18. OPENAI GPT-4o-mini (LLM)
    ┌─────────────────────────────────────┐
    │  • Recibe prompt vía WSO2 Gateway    │
    │  • Procesa prompt                    │
    │  • Genera respuesta natural:         │
    │    "El precio del producto ID        │
    │     123456 se ha actualizado         │
    │     exitosamente de $150.00 a       │
    │     $99.99."                         │
    └──────┬──────────────────────────────┘
           │
           │ Respuesta JSON
           ▼
18a. RESPUESTA HACIA ATRÁS (OpenAI)
    ┌─────────────────────────────────────┐
    │  WSO2 IA Gateway ← OpenAI API        │
    │  • Respuesta JSON con texto          │
    │  • Formateada por el LLM             │
    └──────┬──────────────────────────────┘
           │
           ▼
19. SEMANTIC KERNEL (Finalización)
    ┌─────────────────────────────────────┐
    │  • Agrega respuesta al ChatHistory  │
    │  • Retorna texto formateado          │
    └──────┬──────────────────────────────┘
           │
           ▼
20. AGENTE PYTHON (Salida)
    ┌─────────────────────────────────────┐
    │  • Detiene ThinkingIndicator         │
    │  • Muestra respuesta al usuario       │
    │  • Espera siguiente consulta          │
    └──────┬──────────────────────────────┘
           │
           ▼
21. RESPUESTA AL USUARIO
    ┌─────────────┐
    │   Usuario   │
    │  "El precio │
    │   del       │
    │   producto  │
    │   ID 123456 │
    │   se ha     │
    │   actualizado│
    │   de $150.00│
    │   a $99.99" │
    └─────────────┘
```

---

## Diagrama de Arquitectura de Componentes

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         ARQUITECTURA DEL SISTEMA                        │
└─────────────────────────────────────────────────────────────────────────┘


---

## Flujo de Autenticación OAuth2

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    FLUJO DE AUTENTICACIÓN OAUTH2                        │
└─────────────────────────────────────────────────────────────────────────┘

1. AGENTE PYTHON
   ┌─────────────────────┐
   │  Necesita token      │
   │  para llamar API     │
   └──────────┬───────────┘
              │
              │ POST /token
              │ Headers:
              │   Authorization: Basic {base64(consumer_key:consumer_secret)}
              │ Body:
              │   grant_type=client_credentials
              ▼
2. WSO2 TOKEN ENDPOINT
   ┌─────────────────────┐
   │  Valida credenciales │
   │  Genera access_token │
   │  (expira en X tiempo)│
   └──────────┬───────────┘
              │
              │ Respuesta:
              │ {
              │   "access_token": "abc123...",
              │   "token_type": "Bearer",
              │   "expires_in": 3600
              │ }
              ▼
3. AGENTE PYTHON
   ┌─────────────────────┐
   │  Almacena token      │
   │  Usa en llamadas API │
   └──────────┬───────────┘
              │
              ├─────────────────────┬─────────────────────┐
              │                     │                     │
              │ GET/PUT /shopify/   │ POST /openai/...     │
              │ 1.0.0/products/...  │                     │
              │ Headers:            │ Headers:            │
              │   Authorization:    │   Authorization:    │
              │   Bearer {token}    │   Bearer {token}    │
              │   X-Shopify-Access- │                     │
              │   Token: {token}    │                     │
              ▼                     ▼                     ▼
4. WSO2 API GATEWAY
   ┌─────────────────────────────────────────────────────┐
   │  Valida access_token                                │
   │  ├─ Enruta a Shopify (/shopify/1.0.0)              │
   │  └─ Enruta a OpenAI (/openai/...) [IA Gateway]     │
   └─────────────────────────────────────────────────────┘
```

---

## Tecnologías y Protocolos Utilizados

### Lenguajes y Frameworks
- **Python 3.8+**: Lenguaje principal del agente
- **Microsoft Semantic Kernel**: Framework de orquestación de IA
- **OpenAI API**: Servicio de LLM

### Protocolos de Comunicación
- **HTTP/HTTPS**: Protocolo de comunicación entre componentes
- **REST API**: Arquitectura de API para Shopify
- **OAuth2 Client Credentials**: Flujo de autenticación con WSO2
- **JSON**: Formato de intercambio de datos

### Servicios Externos
- **WSO2 API Manager**: Gateway empresarial centralizado
  - Enruta llamadas a Shopify API
  - Enruta llamadas a OpenAI API (IA Gateway)
- **Shopify Admin API**: API de ecommerce (accedida vía WSO2)
- **OpenAI GPT-4o-mini**: Modelo de lenguaje (accedido vía WSO2 IA Gateway)

### Seguridad
- **OAuth2**: Autenticación y autorización
- **Bearer Tokens**: Tokens de acceso
- **HTTPS**: Comunicación encriptada
- **Environment Variables**: Gestión segura de credenciales

---

## Características Clave del Sistema

### 1. **Sistema Anti-Alucinación**
- Solo retorna datos reales de Shopify
- Nunca inventa productos, precios o IDs
- Verifica todas las operaciones antes de confirmar

### 2. **Memoria de Precios (PriceMemory)**
- Recuerda cambios de precio anteriores
- Permite revertir a precios originales
- Mantiene historial durante la sesión

### 3. **Detección Inteligente de Intenciones**
- Soporte bilingüe (español/inglés)
- Reconocimiento de múltiples formas de expresar lo mismo
- Extracción automática de parámetros

### 4. **Operaciones Matemáticas**
- Sumar/restar valores
- Multiplicar/dividir precios
- Incrementos/decrementos porcentuales
- Operaciones especiales (mitad, doble)

### 5. **Búsqueda Flexible**
- Búsqueda por ID exacto
- Búsqueda por nombre con fuzzy matching
- Sugerencias cuando no hay coincidencia exacta

---

## Configuración de Variables de Entorno

```bash
# WSO2 Configuration
WSO2_TOKEN_ENDPOINT=https://wso2-instance.com/token
WSO2_CONSUMER_KEY=your_consumer_key
WSO2_CONSUMER_SECRET=your_consumer_secret
WSO2_GW_URL=https://wso2-gateway.com:8243

# Shopify Configuration
SHOPIFY_API_TOKEN=your_shopify_token

# OpenAI Configuration
OPENAI_API_KEY=your_openai_key
```

---

## Endpoints y Rutas

### WSO2 Gateway Endpoints
- **Token**: `POST {WSO2_TOKEN_ENDPOINT}/token`
- **Shopify API Base**: `{WSO2_GW_URL}/shopify/1.0.0`
- **OpenAI IA Gateway Base**: `{WSO2_GW_URL}/openai/...`

### Shopify API Endpoints (a través de WSO2 Gateway)
- `GET /shopify/1.0.0/products.json` - Listar productos
- `GET /shopify/1.0.0/products/{id}.json` - Obtener producto
- `GET /shopify/1.0.0/products/count.json` - Contar productos
- `PUT /shopify/1.0.0/products/{id}.json` - Actualizar producto

### OpenAI API Endpoints (a través de WSO2 IA Gateway)
- `POST /openai/v1/chat/completions` - Completar conversación (ChatGPT)
- `POST /openai/v1/completions` - Completar texto
- `POST /openai/v1/embeddings` - Generar embeddings
- Todas las llamadas a OpenAI pasan por WSO2 Gateway (no acceso directo)

---

## Casos de Uso Principales

### 1. Listar Productos
**Usuario**: "Lista los productos"  
**Flujo**: Usuario → Agente → Semantic Kernel → Plugin → WSO2 → Shopify → Respuesta

### 2. Contar Productos
**Usuario**: "¿Cuántos productos hay?"  
**Flujo**: Similar al anterior, pero ejecuta `count_products()`

### 3. Actualizar Precio por ID
**Usuario**: "Actualiza el precio del ID 123456 a 99.99"  
**Flujo**: Completo como se muestra arriba (20 pasos)

### 4. Actualizar Precio por Nombre
**Usuario**: "Cambia el precio de Gift Card a 200"  
**Flujo**: Incluye búsqueda por nombre antes de actualizar

### 5. Operaciones Matemáticas
**Usuario**: "Añade 1000 al precio de The Complete Snowboard"  
**Flujo**: Obtiene precio actual, calcula nuevo precio, actualiza

### 6. Revertir Precio
**Usuario**: "Vuelve el precio original del ID 123456"  
**Flujo**: Consulta PriceMemory, restaura precio anterior

---

## Ventajas de esta Arquitectura

1. **Seguridad Empresarial**: WSO2 Gateway centralizado proporciona capa de seguridad robusta para todas las APIs (Shopify y OpenAI)
2. **Centralización**: Todas las llamadas externas pasan por un único punto de control (WSO2 Gateway)
3. **Escalabilidad**: Arquitectura modular permite escalar componentes independientemente
4. **Mantenibilidad**: Separación clara de responsabilidades
5. **Extensibilidad**: Fácil agregar nuevos plugins y funciones
6. **Experiencia de Usuario**: Lenguaje natural hace el sistema accesible
7. **Confiabilidad**: Sistema anti-alucinación garantiza datos precisos
8. **Observabilidad**: Modo debug permite diagnóstico detallado
9. **Gobernanza de APIs**: Control centralizado de políticas, rate limiting y monitoreo para todas las APIs

---

## Notas para Presentación PowerPoint

### Diapositivas Sugeridas:

1. **Título**: Arquitectura del Agente IA para Ecommerce
2. **Componentes**: Diagrama de componentes principales
3. **Flujo Completo**: Diagrama de flujo de una llamada (20 pasos)
4. **Autenticación**: Flujo OAuth2 detallado
5. **Tecnologías**: Stack tecnológico utilizado
6. **Casos de Uso**: Ejemplos prácticos de uso
7. **Ventajas**: Beneficios de la arquitectura

### Elementos Visuales Recomendados:
- Usar colores consistentes para cada componente
- Flechas claras mostrando dirección del flujo
- Iconos para cada tecnología (WSO2, Shopify, OpenAI, Python)
- Numeración secuencial en el flujo completo
- Resaltar puntos críticos (autenticación, validación)

---

**Documento generado para presentación arquitectónica**  
**Versión**: 1.0  
**Fecha**: 2024

