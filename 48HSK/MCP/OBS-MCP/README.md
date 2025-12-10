# MCP - Model Context Protocol Bridge for OBS Studio

Bridge that connects OBS Studio with the Model Context Protocol (MCP), allowing OBS control through standard protocols and AI tools.

## 📋 Description

This component provides an integration layer between OBS Studio and the Model Context Protocol, enabling AI agents and other applications to control OBS through a standard API.

## 🏗️ Architecture

The component consists of two parts:

1. **bridge.py** - HTTP server that connects directly to OBS Studio
2. **obs-mcp.js** - MCP server that exposes tools to control OBS

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│   MCP       │───▶│  obs-mcp.js  │───▶│  bridge.py  │───▶│  OBS Studio │
│  Client     │    │  (MCP Server)│    │  (HTTP API) │    │             │
└─────────────┘    └──────────────┘    └─────────────┘    └─────────────┘
```

## 🚀 Installation

### Prerequisites

- Node.js (v16 or higher)
- Python 3.8 or higher
- OBS Studio with WebSocket Server enabled
- `obsws-python` (installed automatically with pip)

### Configuration

1. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

2. **Install Python dependencies:**
   ```bash
   pip install aiohttp obsws-python
   ```

3. **Configure OBS Studio:**
   - Open OBS Studio
   - Go to `Tools` → `Settings` → `WebSocket Server`
   - Enable WebSocket Server
   - Configure the port (default: 4444)
   - Set a password

4. **Configure credentials:**
   
   ⚠️ **IMPORTANT:** OBS credentials must be configured in environment variables or in a `.env` file (not hardcoded in the code).
   
   Create a `.env` file in the MCP directory:
   ```bash
   OBS_HOST=localhost
   OBS_PORT=4444
   OBS_PASS=your_obs_password
   ```

## 🎯 Usage

### Start HTTP Bridge

The HTTP bridge must be running for the MCP server to communicate with OBS:

```bash
python bridge.py
```

The server will start at `http://localhost:8888`

### Start MCP Server

```bash
npm start
```

Or directly:

```bash
node obs-mcp.js
```

The MCP server communicates via STDIO, so it's typically run as part of an MCP client.

## 🔧 Features

### Available MCP Tools

- **`set_obs_text`** - Changes the text of a text source in OBS
  - Parameters:
    - `inputName`: Name of the text source in OBS
    - `text`: Text to display

- **`set_obs_item_visibility`** - Shows or hides a scene item in OBS (e.g., Logo)
  - Parameters:
    - `itemName`: Name of the scene item in OBS (e.g., "Logo")
    - `enabled`: `true` to show, `false` to hide
    - `sceneName`: (Optional) Scene name, uses current scene if not specified

### HTTP Bridge API

The bridge exposes a simple REST API:

- **POST** `/call/SetInputSettings` - Change properties of a source
  - Body: `{ "inputName": "source_name", "inputSettings": {...} }`

- **POST** `/call/SetSceneItemEnabled` - Show or hide a scene item
  - Body: `{ "itemName": "Logo", "enabled": true, "sceneName": "Scene Name" }`
  - `sceneName` is optional (uses current scene if not specified)

- **GET** `/openapi.json` - OpenAPI specification of the bridge

## 📝 Usage Examples

### From an MCP Client

```javascript
// Example call to set_obs_text tool
{
  "name": "set_obs_text",
  "arguments": {
    "inputName": "RotuloDemo",
    "text": "Hello from MCP!"
  }
}

// Example call to set_obs_item_visibility tool (show/hide Logo)
{
  "name": "set_obs_item_visibility",
  "arguments": {
    "itemName": "Logo",
    "enabled": true
  }
}
```

### Directly from HTTP

```bash
curl -X POST http://localhost:8888/call/SetInputSettings \
  -H "Content-Type: application/json" \
  -d '{
    "inputName": "RotuloDemo",
    "inputSettings": {
      "text": "Hello from HTTP!"
    }
  }'
```

## 🔒 Security

- ⚠️ **Don't hardcode credentials** in source code
- ✅ Use environment variables or `.env` files for OBS credentials
- ✅ The `.env` file is protected by `.gitignore`
- ✅ The HTTP bridge only accepts local connections by default

## 🛠️ Development

### Project Structure

```
MCP/
├── bridge.py          # HTTP server that connects to OBS
├── obs-mcp.js         # MCP server that exposes tools
├── package.json       # Node.js dependencies
├── package-lock.json  # Dependency lock file
├── run-demo.sh        # Script to verify system status
└── README.md          # This file
```

### Adding New Features

To add new MCP tools:

1. Add the endpoint in `bridge.py` (`handle_call` function)
2. Define the Zod schema in `obs-mcp.js`
3. Implement the tool function
4. Register the tool with `server.registerTool()`

## 🐛 Troubleshooting

### Error: "No connection to OBS"
- Verify that OBS Studio is running
- Confirm that WebSocket Server is enabled in OBS
- Check that the port and password are correct

### Error: "OBS bridge returned 404"
- Make sure `bridge.py` is running on port 8888
- Verify that the URL in `obs-mcp.js` is correct

### Error: "Module not found"
- Run `npm install` to install Node.js dependencies
- Run `pip install aiohttp obsws-python` for Python dependencies

## 📚 References

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [OBS WebSocket API](https://github.com/obsproject/obs-websocket)
- [obsws-python](https://github.com/aatikturk/obsws-python)

## 📝 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](../LICENSE) file for more details.
