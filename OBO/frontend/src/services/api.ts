import type { ProtectedAccessRequest, SessionResponse } from "../types/models";

function parsePayload(text: string): unknown {
  if (!text) {
    return null;
  }

  try {
    return JSON.parse(text);
  } catch {
    return text;
  }
}

function describeErrorPayload(payload: unknown, path: string): string {
  if (typeof payload === "string") {
    return payload;
  }

  if (typeof payload === "object" && payload) {
    const maybeDetail = (payload as { detail?: unknown }).detail;
    if (typeof maybeDetail === "string") {
      return maybeDetail;
    }
    if (typeof maybeDetail === "object" && maybeDetail) {
      const detailObject = maybeDetail as { message?: unknown; reason?: unknown };
      if (typeof detailObject.message === "string") {
        return detailObject.message;
      }
      if (typeof detailObject.reason === "string") {
        return detailObject.reason;
      }
      return JSON.stringify(maybeDetail, null, 2);
    }

    return JSON.stringify(payload, null, 2);
  }

  return `Request to ${path} failed`;
}

export class DemoApiError extends Error {
  status: number;
  payload: unknown;

  constructor(message: string, status: number, payload: unknown) {
    super(message);
    this.status = status;
    this.payload = payload;
  }
}

export class BackendApi {
  constructor(
    private readonly baseUrl: string,
    private readonly sessionId: string,
  ) {}

  private async request<T>(path: string, init?: RequestInit): Promise<T> {
    const response = await fetch(`${this.baseUrl}${path}`, {
      ...init,
      headers: {
        "Content-Type": "application/json",
        "X-Demo-Session-Id": this.sessionId,
        ...(init?.headers ?? {}),
      },
    });
    const text = await response.text();
    const payload = parsePayload(text);
    if (!response.ok) {
      const message = describeErrorPayload(payload, path);
      throw new DemoApiError(message, response.status, payload);
    }
    return payload as T;
  }

  getSession(): Promise<SessionResponse> {
    return this.request<SessionResponse>("/api/session", { method: "GET" });
  }

  syncUserToken(accessToken: string, userProfile?: Record<string, unknown>): Promise<SessionResponse> {
    return this.request<SessionResponse>("/api/session/user-token", {
      method: "POST",
      body: JSON.stringify({ access_token: accessToken, user_profile: userProfile ?? null }),
    });
  }

  fetchAgentToken(): Promise<SessionResponse> {
    return this.request<SessionResponse>("/api/agent-token", { method: "POST" });
  }

  startObo(): Promise<SessionResponse> {
    return this.request<SessionResponse>("/api/obo/start", { method: "POST" });
  }

  exchangeObo(): Promise<SessionResponse> {
    return this.request<SessionResponse>("/api/obo/exchange", { method: "POST" });
  }

  testAgentAccess(request: ProtectedAccessRequest): Promise<SessionResponse> {
    return this.request<SessionResponse>("/api/test/agent-access", {
      method: "POST",
      body: JSON.stringify(request),
    });
  }

  testOboAccess(request: ProtectedAccessRequest): Promise<SessionResponse> {
    return this.request<SessionResponse>("/api/test/obo-access", {
      method: "POST",
      body: JSON.stringify(request),
    });
  }
}
