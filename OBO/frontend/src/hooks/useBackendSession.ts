import { useEffect, useState } from "react";

import { env } from "../config/env";
import { BackendApi } from "../services/api";
import type { ProtectedAccessRequest, SessionResponse } from "../types/models";

const SESSION_STORAGE_KEY = "obo-demo-session-id";

function getOrCreateSessionId(): string {
  const existing = window.localStorage.getItem(SESSION_STORAGE_KEY);
  if (existing) {
    return existing;
  }
  const created = window.crypto.randomUUID();
  window.localStorage.setItem(SESSION_STORAGE_KEY, created);
  return created;
}

function createFreshSessionId(): string {
  const created = window.crypto.randomUUID();
  window.localStorage.setItem(SESSION_STORAGE_KEY, created);
  return created;
}

function describeError(error: unknown): string {
  if (error instanceof Error) {
    return error.message;
  }
  return "Unknown error";
}

export function useBackendSession() {
  const [sessionId, setSessionId] = useState(() => getOrCreateSessionId());
  const [api, setApi] = useState(() => new BackendApi(env.backendBaseUrl, getOrCreateSessionId()));
  const [session, setSession] = useState<SessionResponse | null>(null);
  const [loadingAction, setLoadingAction] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    void refreshSession();
  }, [api]);

  async function withLoading<T>(label: string, action: () => Promise<T>): Promise<T> {
    setLoadingAction(label);
    setError(null);
    try {
      return await action();
    } catch (nextError) {
      setError(describeError(nextError));
      throw nextError;
    } finally {
      setLoadingAction(null);
    }
  }

  async function refreshSession(): Promise<SessionResponse> {
    const next = await api.getSession();
    setSession(next);
    return next;
  }

  async function syncUserToken(
    accessToken: string,
    userProfile?: Record<string, unknown>,
  ): Promise<SessionResponse> {
    return withLoading("Sincronizar USER_TOKEN", async () => {
      const next = await api.syncUserToken(accessToken, userProfile);
      setSession(next);
      return next;
    });
  }

  async function fetchAgentToken(): Promise<SessionResponse> {
    return withLoading("Obtener AGENT_TOKEN", async () => {
      const next = await api.fetchAgentToken();
      setSession(next);
      return next;
    });
  }

  async function startObo(): Promise<SessionResponse> {
    return withLoading("Iniciar delegacion OBO", async () => {
      const next = await api.startObo();
      setSession(next);
      return next;
    });
  }

  async function exchangeObo(): Promise<SessionResponse> {
    return withLoading("Intercambiar code por OBO_TOKEN", async () => {
      const next = await api.exchangeObo();
      setSession(next);
      return next;
    });
  }

  async function testAgentAccess(request: ProtectedAccessRequest): Promise<SessionResponse> {
    return withLoading("Probar acceso con AGENT_TOKEN", async () => {
      const next = await api.testAgentAccess(request);
      setSession(next);
      return next;
    });
  }

  async function testUserAccess(request: ProtectedAccessRequest): Promise<SessionResponse> {
    return withLoading("Probar acceso con USER_TOKEN", async () => {
      const next = await api.testUserAccess(request);
      setSession(next);
      return next;
    });
  }

  async function testOboAccess(request: ProtectedAccessRequest): Promise<SessionResponse> {
    return withLoading("Leer mis ficheros con OBO_TOKEN", async () => {
      const next = await api.testOboAccess(request);
      setSession(next);
      return next;
    });
  }

  async function uploadWithObo(fileName: string): Promise<SessionResponse> {
    return testOboAccess({
      resource_path: "/files/upload",
      method: "POST",
      payload: { file_name: fileName },
    });
  }

  async function shareWithObo(fileId: string, target: string): Promise<SessionResponse> {
    return testOboAccess({
      resource_path: `/files/${fileId}/share`,
      method: "POST",
      payload: { target },
    });
  }

  function resetSession(): string {
    const nextSessionId = createFreshSessionId();
    setSessionId(nextSessionId);
    setSession(null);
    setError(null);
    setLoadingAction(null);
    setApi(new BackendApi(env.backendBaseUrl, nextSessionId));
    return nextSessionId;
  }

  return {
    sessionId,
    session,
    loadingAction,
    error,
    refreshSession: () => withLoading("Refrescar sesion", refreshSession),
    syncUserToken,
    fetchAgentToken,
    startObo,
    exchangeObo,
    testAgentAccess,
    testUserAccess,
    testOboAccess,
    uploadWithObo,
    shareWithObo,
    resetSession,
  };
}
