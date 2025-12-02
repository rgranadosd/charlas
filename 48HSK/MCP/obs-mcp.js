#!/usr/bin/env node

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import fetch from "node-fetch";

const OBS_BRIDGE_URL = "http://localhost:8888/call/SetInputSettings";

// Schema Zod de entrada
const SetObsTextSchema = z.object({
  inputName: z
    .string()
    .describe("Nombre de la fuente de texto en OBS (por ejemplo, RotuloDemo)."),
  text: z
    .string()
    .describe("Texto que se quiere mostrar en la fuente."),
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
    const res = await fetch(OBS_BRIDGE_URL, {
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

// Crear MCP server
const server = new McpServer({
  name: "obs-bridge",
  version: "1.0.0",
});

// Registrar tool
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
