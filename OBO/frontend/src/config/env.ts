const required = [
  "VITE_BACKEND_BASE_URL",
  "VITE_ASGARDEO_CLIENT_ID",
  "VITE_ASGARDEO_BASE_URL",
  "VITE_ASGARDEO_SIGN_IN_REDIRECT_URL",
  "VITE_ASGARDEO_SIGN_OUT_REDIRECT_URL",
] as const;

function isUnsetOrPlaceholder(value: string | undefined): boolean {
  if (!value) {
    return true;
  }

  const normalized = value.trim().toLowerCase();
  return (
    normalized.length === 0 ||
    normalized.includes("replace-with") ||
    normalized.includes("<spa-client-id>") ||
    normalized.includes("<is-host>")
  );
}

for (const key of required) {
  if (!import.meta.env[key]) {
    console.warn(`Missing env variable ${key}`);
  }
}

export const env = {
  backendBaseUrl: import.meta.env.VITE_BACKEND_BASE_URL ?? "http://localhost:8000",
  debugFullTokens: (import.meta.env.VITE_DEBUG_FULL_TOKENS ?? "false") === "true",
  asgardeoClientId: import.meta.env.VITE_ASGARDEO_CLIENT_ID ?? "",
  asgardeoBaseUrl: import.meta.env.VITE_ASGARDEO_BASE_URL ?? "",
  asgardeoSignInRedirectUrl: import.meta.env.VITE_ASGARDEO_SIGN_IN_REDIRECT_URL ?? window.location.origin,
  asgardeoSignOutRedirectUrl:
    import.meta.env.VITE_ASGARDEO_SIGN_OUT_REDIRECT_URL ?? window.location.origin,
  asgardeoScope: (import.meta.env.VITE_ASGARDEO_SCOPE ?? "openid profile email")
    .split(" ")
    .filter(Boolean),
};

export const authConfig = {
  signInRedirectURL: env.asgardeoSignInRedirectUrl,
  signOutRedirectURL: env.asgardeoSignOutRedirectUrl,
  clientID: env.asgardeoClientId,
  baseUrl: env.asgardeoBaseUrl,
  scope: env.asgardeoScope,
};

const authConfigErrors: string[] = [];

if (isUnsetOrPlaceholder(import.meta.env.VITE_ASGARDEO_CLIENT_ID)) {
  authConfigErrors.push("VITE_ASGARDEO_CLIENT_ID no apunta a una aplicacion SPA real de WSO2 IS");
}

if (isUnsetOrPlaceholder(import.meta.env.VITE_ASGARDEO_BASE_URL)) {
  authConfigErrors.push("VITE_ASGARDEO_BASE_URL no apunta al host real de WSO2 IS");
}

export const authConfigValidationError = authConfigErrors.length
  ? authConfigErrors.join(". ")
  : null;
