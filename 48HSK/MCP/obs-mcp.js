#!/usr/bin/env node

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import fetch from "node-fetch";

const OBS_BRIDGE_BASE_URL = "http://localhost:8888/call";

// Schema Zod de entrada para texto
const SetObsTextSchema = z.object({
  inputName: z
    .string()
    .describe("Nombre de la fuente de texto en OBS (por ejemplo, RotuloDemo)."),
  text: z
    .string()
    .describe("Texto que se quiere mostrar en la fuente."),
});

// Schema Zod de entrada para activar/desactivar elementos
const SetSceneItemEnabledSchema = z.object({
  itemName: z
    .string()
    .describe("Nombre del elemento en OBS (por ejemplo, Logo)."),
  enabled: z
    .boolean()
    .describe("true para mostrar el elemento, false para ocultarlo."),
  sceneName: z
    .string()
    .optional()
    .describe("Nombre de la escena (opcional, usa la escena actual si no se especifica)."),
});

// Implementación de la tool (SIN tipos TS)
async function setObsTextImplementation(input) {
  const body = {
    inputName: input.inputName,
    inputSettings: {
      text: input.text,
    },
  };

  try {
    const res = await fetch(`${OBS_BRIDGE_BASE_URL}/SetInputSettings`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });

    if (!res.ok) {
      const txt = await res.text();
      console.error(`OBS bridge devolvió ${res.status}: ${txt}`);
      return {
        content: [
          {
            type: "text",
            text: `Error del bridge OBS (${res.status}): ${txt}`,
          },
        ],
      };
    }

    return {
      content: [
        {
          type: "text",
          text: `Texto actualizado en OBS para ${input.inputName}`,
        },
      ],
    };
  } catch (err) {
    console.error("Error llamando al bridge OBS:", err);
    return {
      content: [
        {
          type: "text",
          text: `Error llamando al bridge OBS: ${err.message}`,
        },
      ],
    };
  }
}

// Implementación para activar/desactivar elementos de escena
async function setSceneItemEnabledImplementation(input) {
  const body = {
    itemName: input.itemName,
    enabled: input.enabled,
  };

  if (input.sceneName) {
    body.sceneName = input.sceneName;
  }

  try {
    const res = await fetch(`${OBS_BRIDGE_BASE_URL}/SetSceneItemEnabled`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });

    if (!res.ok) {
      const txt = await res.text();
      console.error(`OBS bridge devolvió ${res.status}: ${txt}`);
      return {
        content: [
          {
            type: "text",
            text: `Error del bridge OBS (${res.status}): ${txt}`,
          },
        ],
      };
    }

    const action = input.enabled ? "activado" : "desactivado";
    return {
      content: [
        {
          type: "text",
          text: `Elemento ${input.itemName} ${action} en OBS`,
        },
      ],
    };
  } catch (err) {
    console.error("Error llamando al bridge OBS:", err);
    return {
      content: [
        {
          type: "text",
          text: `Error llamando al bridge OBS: ${err.message}`,
        },
      ],
    };
  }
}

// Crear MCP server
const server = new McpServer({
  name: "obs-bridge",
  version: "1.0.0",
});

// Registrar tools
server.registerTool(
  "set_obs_text",
  {
    description: "Cambia el texto de una fuente de OBS usando el bridge HTTP local.",
    inputSchema: SetObsTextSchema,
  },
  async (args) => {
    return await setObsTextImplementation(args);
  },
);

server.registerTool(
  "set_obs_item_visibility",
  {
    description: "Activa o desactiva (muestra u oculta) un elemento de escena en OBS, como el Logo.",
    inputSchema: SetSceneItemEnabledSchema,
  },
  async (args) => {
    return await setSceneItemEnabledImplementation(args);
  },
);

// Arrancar por STDIO
async function main() {
  try {
    const transport = new StdioServerTransport();
    await server.connect(transport);
    console.error("obs-bridge MCP server escuchando por stdio");
  } catch (err) {
    console.error("Error al iniciar obs-bridge:", err);
    process.exit(1);
  }
}

main();
