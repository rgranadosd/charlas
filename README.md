# 🤖 Sample AI Agent for WSO2 API Manager

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Python-3.8+-green.svg)](https://python.org)
[![Semantic Kernel](https://img.shields.io/badge/Semantic%20Kernel-Microsoft-purple.svg)](https://github.com/microsoft/semantic-kernel)
[![WSO2](https://img.shields.io/badge/WSO2-API%20Manager-orange.svg)](https://wso2.com)
[![Shopify](https://img.shields.io/badge/Shopify-API-brightgreen.svg)](https://shopify.dev)

> **Agente inteligente de ecommerce** potenciado por **Microsoft Semantic Kernel** que integra WSO2 API Manager como gateway para acceder a las APIs de Shopify. Proporciona interacciones en lenguaje natural para gestionar tiendas Shopify con seguridad de nivel empresarial y capacidades avanzadas de orquestación de IA.

---

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Arquitectura](#-arquitectura)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación](#-instalación)
- [Configuración](#-configuración)
- [Uso](#-uso)
- [Semantic Kernel](#-microsoft-semantic-kernel-integration)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Seguridad](#-seguridad)
- [Solución de Problemas](#-solución-de-problemas)
- [Contribuir](#-contribuir)
- [Licencia](#-licencia)

---

## ✨ Características

- 🧠 **Integración con Microsoft Semantic Kernel** - Orquestación avanzada de IA con arquitectura de plugins
- 💬 **Interfaz de Lenguaje Natural** - Interactúa con tu tienda Shopify usando lenguaje natural en español o inglés
- 🔒 **Integración con WSO2 API Manager** - Gateway de APIs de nivel empresarial con autenticación OAuth2
- 📦 **Gestión Completa de Shopify** - Lista, busca, cuenta y actualiza productos con datos en tiempo real
- 💰 **Gestión Inteligente de Precios** - Actualiza precios por ID, nombre u operaciones matemáticas
- 🔐 **Gestión Segura de Credenciales** - Configuración basada en variables de entorno con protección .gitignore
- ⏱️ **Indicadores de Progreso en Tiempo Real** - Retroalimentación visual para todas las operaciones
- ✅ **Sistema Anti-alucinación** - Solo retorna datos reales de Shopify, nunca inventa información
- 🌐 **Soporte Bilingüe** - Acepta comandos en inglés y español
- 📜 **Historial de Precios y Rollback** - Recuerda precios anteriores y permite restaurarlos

## 📋 Requisitos Previos

- **Python 3.8 o superior**
- **Microsoft Semantic Kernel** (se instala vía pip)
- **Instancia de WSO2 API Manager** (versión 4.x recomendada)
- **Tienda Shopify** con acceso a API Admin
- **Clave de API de OpenAI** para funcionalidad de IA
- **Sistema operativo**: Linux, macOS o Windows con WSL

## 🚀 Instalación

### 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/rgranadosd/charlas.git
cd charlas
```

### 2️⃣ Crear y activar entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate  # En Linux/macOS
# o
.\venv\Scripts\activate  # En Windows
```

### 3️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4️⃣ Configurar variables de entorno

```bash
cp env.example .env
nano .env  # o usa tu editor favorito
```

Edita el archivo `.env` con tus credenciales reales. Ver sección [Configuración](#-configuración) para más detalles.

## 🎯 Inicio Rápido

### Verificar la configuración

Asegúrate de que tu archivo `.env` esté configurado correctamente con todas las credenciales necesarias.

### Iniciar el agente

```bash
# Usando el script de inicio
./start_agent.sh

# O ejecutar directamente
python3 agent_gpt4.py

# Modo debug (muestra información detallada)
python3 agent_gpt4.py --debug
```

### Ejemplos de uso

```
You: lista todos los productos
Assistant: [Lista de productos con IDs y precios]

You: cuántos productos tengo?
Assistant: Tienes 22 productos en tu tienda

You: actualiza el precio del producto 12345 a 29.99
Assistant: ✓ Precio actualizado correctamente

You: aumenta el precio del producto "Camiseta Azul" un 10%
Assistant: ✓ Precio actualizado de $20.00 a $22.00
```

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                      USUARIO / CLI                          │
│                  (Lenguaje Natural)                         │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                    AGENTE IA                                │
│         Microsoft Semantic Kernel + OpenAI                  │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │   Plugins   │  │ Chat History │  │ AI Functions │       │
│  │  (Shopify)  │  │  Management  │  │   Calling    │       │
│  └─────────────┘  └──────────────┘  └──────────────┘       │
└────────────────────────────┬────────────────────────────────┘
                             │ OAuth2 Token
                             ▼
┌─────────────────────────────────────────────────────────────┐
│              WSO2 API MANAGER (Gateway)                     │
│  ┌────────────┐  ┌─────────────┐  ┌──────────────┐         │
│  │   OAuth2   │  │   Routing   │  │   Security   │         │
│  │   Server   │  │   Policies  │  │   Policies   │         │
│  └────────────┘  └─────────────┘  └──────────────┘         │
└────────────────────────────┬────────────────────────────────┘
                             │ API Calls
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                    SHOPIFY API                              │
│         (Products, Pricing, Inventory)                      │
└─────────────────────────────────────────────────────────────┘
```

### Flujo de Datos

1. **Usuario** → Entrada en lenguaje natural
2. **Semantic Kernel** → Procesa la intención y selecciona funciones
3. **Plugin Shopify** → Solicita token OAuth2 a WSO2
4. **WSO2 Gateway** → Valida credenciales y retorna token
5. **Plugin Shopify** → Llama API de Shopify a través de WSO2
6. **WSO2 Gateway** → Aplica políticas y enruta la petición
7. **Shopify API** → Procesa y retorna datos
8. **Agente IA** → Formatea respuesta en lenguaje natural

## 📁 Estructura del Proyecto

```
SampleAIAgent/
├── 📄 agent_gpt4.py              # Script principal del agente IA
├── 🔧 start_agent.sh             # Script de inicio (ejecutable)
├── 🧪 test.sh                    # Suite completa de pruebas
├── 🔐 check_credential.sh        # Verificación de credenciales WSO2
├── 📋 env.example                # Plantilla de variables de entorno
├── 📦 requirements.txt           # Dependencias de Python
├── 🔒 .env                       # Variables de entorno (crear desde template)
├── 📜 LICENSE                    # Licencia Apache 2.0
├── 📖 README.md                  # Este archivo
└── 🙈 .gitignore                 # Archivos ignorados por Git
```

## ⚙️ Configuración

### 1. Configuración de WSO2 API Manager

#### Paso 1: Crear Aplicación en WSO2

1. Accede al **Developer Portal** de WSO2: `https://localhost:9443/devportal`
2. Inicia sesión (usuario por defecto: `admin` / contraseña: `admin`)
3. Navega a **Applications** → **Add New Application**
4. Crea una aplicación (ej. "ShopifyApp")
5. Ve a **Production Keys** → **Generate Keys**
6. Copia el **Consumer Key** y **Consumer Secret**
7. Guarda estos valores en tu archivo `.env`:
   ```bash
   WSO2_CONSUMER_KEY=tu_consumer_key
   WSO2_CONSUMER_SECRET=tu_consumer_secret
   ```

#### Paso 2: Importar API de Shopify

1. Accede al **Publisher** de WSO2: `https://localhost:9443/publisher`
2. Click en **Create API** → **Import Open API**
3. Importa la especificación de la API `admin-ShopifyAdminAPIProxy-1.0.0`
4. Configura el **Endpoint Backend** apuntando a Shopify:
   ```
   https://{tu-tienda}.myshopify.com/admin/api/2024-01
   ```
5. Establece el **Context** como: `/shopify/1.0.0`
6. Configura **Security** como OAuth2
7. **Save** y **Publish** la API

#### Paso 3: Suscribir la Aplicación a la API

1. Vuelve al **Developer Portal**
2. Ve a **APIs** → Selecciona la API de Shopify
3. Click en **Subscribe**
4. Selecciona tu aplicación creada anteriormente
5. Confirma la suscripción

### 2. Configuración de Shopify

#### Crear Custom App y Generar Token

1. Accede a tu **Shopify Admin Panel**
2. Ve a **Settings** → **Apps and sales channels**
3. Click en **Develop apps** (o "Desarrollar aplicaciones")
4. Click en **Create an app** → Dale un nombre (ej. "WSO2 Integration")
5. Ve a **Configuration** → **Admin API integration**
6. Configura los **Access scopes** necesarios:
   - ✅ `read_products`
   - ✅ `write_products`
   - ✅ `read_product_listings`
   - ✅ `write_product_listings`
7. Click en **Save**
8. Ve a **API credentials**
9. Click en **Install app** (confirma la instalación)
10. Copia el **Admin API access token** (solo se muestra una vez)
11. Guarda el token en tu archivo `.env`:
    ```bash
    SHOPIFY_API_TOKEN=shpat_xxxxxxxxxxxxxxxxxxxxx
    ```

### 3. Configuración de OpenAI

1. Ve a [OpenAI Platform](https://platform.openai.com/api-keys)
2. Inicia sesión o crea una cuenta
3. Navega a **API Keys**
4. Click en **Create new secret key**
5. Dale un nombre descriptivo (ej. "WSO2 Shopify Agent")
6. Copia la clave (solo se muestra una vez)
7. Guarda la clave en tu archivo `.env`:
   ```bash
   OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxx
   ```

## 🔒 Seguridad

### Mejores Prácticas Implementadas

- 🔐 **Variables de Entorno**: Todas las credenciales se almacenan en archivo `.env`
- 🙈 **Protección Git**: `.gitignore` previene exposición de credenciales
- 🔑 **Flujo OAuth2**: Autenticación segura basada en tokens con WSO2
- 🔒 **HTTPS**: Todas las comunicaciones API usan conexiones encriptadas
- 🔄 **Rotación de Tokens**: WSO2 maneja la renovación automática de tokens
- ✅ **Validación de Entrada**: Sanitización de todos los inputs del usuario
- 📝 **Logs Seguros**: No se registran credenciales en los logs

### Recomendaciones de Seguridad

1. **Nunca subas el archivo `.env` al repositorio**
2. **Usa HTTPS en producción** (no HTTP)
3. **Regenera tokens periódicamente**
4. **Limita los permisos de API** solo a los necesarios
5. **Monitorea el uso de API** en WSO2 Analytics
6. **Usa secretos de Kubernetes/Docker** en entornos containerizados

## 🔧 Solución de Problemas

### Problemas Comunes

#### ❌ Error 401 en WSO2 Gateway

**Síntoma**: `Error al obtener token WSO2: 401`

**Soluciones**:
1. Verifica que `WSO2_CONSUMER_KEY` y `WSO2_CONSUMER_SECRET` sean correctos
2. Confirma que la aplicación esté suscrita a la API
3. Regenera las Production Keys en WSO2 Developer Portal
4. Verifica que el endpoint de token sea correcto: `https://localhost:9443/oauth2/token`

#### ❌ Error 404 en WSO2 Gateway

**Síntoma**: `404 Not Found` al llamar a la API

**Soluciones**:
1. Verifica que el contexto de la API sea `/shopify/1.0.0`
2. Confirma que la API esté **Published** en WSO2 Publisher
3. Verifica que `WSO2_GW_URL` sea correcto: `https://localhost:8243`
4. Revisa que la API esté desplegada en el Gateway

#### ❌ Autenticación de Shopify Fallida

**Síntoma**: Error al acceder a productos de Shopify

**Soluciones**:
1. Verifica que `SHOPIFY_API_TOKEN` sea válido
2. Confirma los permisos de la Custom App en Shopify
3. Verifica que el token no haya expirado
4. Confirma que `SHOPIFY_STORE_NAME` sea correcto

#### ❌ Clave de OpenAI Inválida

**Síntoma**: `Invalid OpenAI API Key`

**Soluciones**:
1. Genera una nueva clave en [OpenAI Platform](https://platform.openai.com/api-keys)
2. Verifica que la clave tenga créditos disponibles
3. Confirma que no haya espacios en `OPENAI_API_KEY` en el `.env`
4. Verifica que la clave empiece con `sk-`

#### ❌ Variables de Entorno No Cargan

**Síntoma**: `Error: Faltan variables en .env`

**Soluciones**:
1. Confirma que el archivo se llame `.env` (no `env` ni `.env.example`)
2. Verifica que `.env` esté en el directorio raíz del proyecto
3. Comprueba que no haya espacios alrededor del `=` en las variables
4. Ejecuta `source .env` manualmente para verificar

### 🛠️ Comandos de Diagnóstico

```bash
# Verificar credenciales de WSO2
./check_credential.sh

# Ejecutar con logging detallado
python3 agent_gpt4.py --debug

# Verificar variables de entorno cargadas
python3 -c "from dotenv import load_dotenv; import os; load_dotenv(); print('WSO2_TOKEN_ENDPOINT:', os.getenv('WSO2_TOKEN_ENDPOINT'))"
```

### 📊 Logs y Debugging

Los logs se muestran en tiempo real. En modo debug (`--debug`), verás:
- Tokens de autenticación (parcialmente ocultos)
- URLs completas de las peticiones
- Headers enviados
- Respuestas de las APIs
- Tiempo de ejecución de cada operación

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Si quieres mejorar este proyecto:

1. **Fork** el repositorio
2. Crea una **rama** para tu feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. **Push** a la rama (`git push origin feature/AmazingFeature`)
5. Abre un **Pull Request**

### Áreas de Mejora

- [ ] Soporte para más operaciones de Shopify (inventario, pedidos, clientes)
- [ ] Integración con otros LLMs (Azure OpenAI, Anthropic Claude)
- [ ] Dashboard web para visualización
- [ ] Soporte para múltiples tiendas Shopify
- [ ] Tests automatizados con pytest
- [ ] Documentación de API en español
- [ ] Containerización con Docker
- [ ] CI/CD con GitHub Actions

## 📝 Licencia

Este proyecto está licenciado bajo **Apache License 2.0** - ver el archivo [LICENSE](LICENSE) para más detalles.

```
Copyright 2025 Sample AI Agent Project

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

## 📚 Referencias

- [Microsoft Semantic Kernel](https://github.com/microsoft/semantic-kernel) - Framework de orquestación de IA
- [WSO2 API Manager](https://wso2.com/api-manager/) - Gateway de APIs empresarial
- [Shopify Admin API](https://shopify.dev/docs/api/admin) - Documentación de la API de Shopify
- [OpenAI Platform](https://platform.openai.com/) - Plataforma de modelos de lenguaje

## 👥 Autores

- **Rafa Granados** - *Desarrollo inicial* - [@rgranadosd](https://github.com/rgranadosd)

## 🙏 Agradecimientos

- Equipo de Microsoft Semantic Kernel por el excelente framework
- Comunidad de WSO2 por la documentación y soporte
- OpenAI por los modelos de lenguaje GPT
- Shopify por la API bien documentada

---

<div align="center">

**🚀 Hecho con ❤️ para la gestión inteligente de ecommerce**

[![GitHub](https://img.shields.io/badge/GitHub-Repository-black?style=for-the-badge&logo=github)](https://github.com/rgranadosd/charlas)
[![WSO2](https://img.shields.io/badge/WSO2-API%20Manager-orange?style=for-the-badge&logo=wso2)](https://wso2.com)
[![Shopify](https://img.shields.io/badge/Shopify-Partner-brightgreen?style=for-the-badge&logo=shopify)](https://shopify.dev)

</div>
