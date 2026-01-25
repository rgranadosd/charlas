# Arquitectura Tecnológica del Agente Agéntico: Desglose de Componentes

Este documento explica en profundidad el "stack" tecnológico utilizado para construir el agente conversacional de Shopify, detallando el rol específico de cada pieza y cómo interactúan entre sí para crear una experiencia "agéntica" (capaz de razonar y actuar).

---

## 1. Python y Extensiones: El Cimiento de Ejecución

Python actúa como el lenguaje anfitrión ("Host Language"). Es el entorno donde vive el agente, se conecta a internet y ejecuta lógica determinista.

### ¿Por qué Python?
No solo es el estándar en IA, sino que permite integrar fácilmente bibliotecas de conexión a APIs (como `requests` para Shopify/WSO2) con bibliotecas de IA (Semantic Kernel).

### Extensiones Clave Utilizadas:
*   **`requests`:** Es la "mano" del agente. Mientras el cerebro (LLM) piensa "necesito actualizar el precio", `requests` es quien realmente envía el paquete HTTP `PUT` a la API de Shopify a través de WSO2.
*   **`asyncio`:** Permite que el agente sea **asíncrono**. Esto es vital porque las llamadas al LLM (OpenAI) y a la API de Shopify son lentas. `asyncio` permite que el programa no se congele mientras espera, manteniendo la interfaz fluida (por eso el indicador "Thinking..." no se bloquea).
*   **`dotenv`:** Gestiona la seguridad, cargando claves API desde un archivo `.env` para que nunca estén escritas en el código fuente.

---

## 2. Microsoft Semantic Kernel (SK): El Orquestador Agéntico

Semantic Kernel es la pieza central que convierte un script normal de Python en una arquitectura agéntica. Es el "pegamento" entre el código tradicional (funciones) y la inteligencia artificial (LLMs).

### ¿Qué hace exactamente en nuestro agente?

#### A. Abstracción del Modelo de IA
SK actúa como un adaptador universal.
*   **Sin SK:** Tendrías que escribir código específico para la API de OpenAI (`openai.ChatCompletion.create(...)`). Si mañana quieres cambiar a Azure OpenAI o a un modelo local (Ollama), tendrías que reescribir todo.
*   **Con SK:** Usas `kernel.add_service(...)`. Cambiar de cerebro es tan fácil como cambiar una línea de configuración.

#### B. Plugins y Funciones Nativas (`@kernel_function`)
Esta es la magia que permite al LLM "tocar" el mundo real.
*   Normalmente, un LLM solo genera texto. No puede "ver" tu base de datos ni "tocar" tu tienda Shopify.
*   **Semantic Kernel** permite decorar tus funciones de Python (como `update_product_price`) con `@kernel_function`.
*   Esto crea una "Skill" (Habilidad) que el Kernel expone. El Kernel le dice al LLM: *"Oye, tengo una herramienta llamada `update_product_price` que necesita un ID y un precio. Si necesitas usarla, dímelo"*.

#### C. Invocación de Prompts ("Semantic Functions")
SK permite tratar los prompts como si fueran funciones de código.
*   En nuestro código, `kernel.invoke_prompt(...)` no es solo enviar texto. SK gestiona el contexto, la memoria de la conversación y los parámetros, permitiendo crear flujos complejos (como el clasificador de intenciones) de forma estructurada.

---

## 3. LLM (Large Language Model): El Cerebro Razonador

En nuestra arquitectura, usamos **GPT-4o-mini** (vía OpenAI). Su rol no es "saberlo todo", sino **razonar y orquestar**.

### Roles Específicos del LLM en este Agente:

#### A. Clasificador de Intenciones (El "Router")
El LLM analiza el lenguaje natural ambiguo del usuario y decide qué camino tomar.
*   *Usuario:* "Oye, pon la tarjeta esa de regalo a 50 pavos, que está muy cara".
*   *LLM (Razonamiento):* "El usuario quiere cambiar un precio. La intención es `actualizar_precio`. El producto es 'tarjeta regalo' y el precio es '50'".
*   *Salida:* Genera un JSON estructurado que el código Python puede entender: `{"category": "actualizar_precio"}`.

#### B. Extractor de Entidades (El "Traductor")
Convierte texto sucio en datos limpios para la API.
*   Transforma "sin precios" en un booleano `False`.
*   Transforma "50 euros" en el número `50`.

#### C. Generador de Respuestas (El "Locutor")
Si la intención es `general` (ej. "¿Quién es el CEO de Apple?"), el LLM usa su conocimiento interno para responder directamente, actuando como un chatbot tradicional.

---

## Resumen de la Interacción

1.  **Python** inicia el bucle y escucha al usuario.
2.  **Semantic Kernel** toma el texto del usuario y lo envía al **LLM** con instrucciones ("Clasifica esto...").
3.  El **LLM** analiza y responde: "Es una actualización de precio".
4.  **Semantic Kernel** recibe la respuesta y devuelve el control a **Python**.
5.  **Python** ejecuta la función `update_product_price` (usando `requests`).
6.  **Python** muestra el resultado final al usuario.

Esta simbiosis es lo que define a una **Aplicación Agéntica**: Código determinista (herramientas) gobernado por Inteligencia Probabilística (LLM).
