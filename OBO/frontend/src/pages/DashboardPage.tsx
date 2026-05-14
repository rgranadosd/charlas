import { useEffect, useState } from "react";
import { useAuthContext } from "@asgardeo/auth-react";

import { ArtifactInspector } from "../components/ArtifactInspector";
import { StepRunnerPanel } from "../components/StepRunnerPanel";
import { TraceViewer } from "../components/TraceViewer";
import { authConfigValidationError } from "../config/env";
import { useBackendSession } from "../hooks/useBackendSession";

function deriveSuggestedStepOrder(isAuthenticated: boolean, session: ReturnType<typeof useBackendSession>["session"]): number {
  const agentAvailable = session?.artifacts.agent.available ?? false;
  const userAccessDone =
    session?.traces.some(
      (trace) => trace.action === "Probar acceso con USER_TOKEN" && trace.response_status < 400,
    ) ?? false;
  const agentAccessDone =
    session?.traces.some(
      (trace) => trace.action === "Probar acceso con AGENT_TOKEN" && trace.response_status >= 400,
    ) ?? false;
  const delegationStarted = session?.artifacts.delegation.status === "available";
  const authCodeAvailable = session?.artifacts.authorization_code.status === "available";
  const oboAvailable = session?.artifacts.obo.available ?? false;
  const oboReadDone =
    session?.traces.some((trace) => trace.action === "Leer mis ficheros con OBO_TOKEN") ?? false;

  const guided = [
    { order: 1, done: isAuthenticated },
    { order: 2, done: agentAvailable },
    { order: 3, done: userAccessDone && agentAccessDone },
    { order: 4, done: delegationStarted },
    { order: 5, done: authCodeAvailable },
    { order: 6, done: oboAvailable },
    { order: 7, done: oboReadDone },
  ];

  return guided.find((step) => !step.done)?.order ?? 7;
}

export function DashboardPage() {
  const { state, signIn, signOut, getAccessToken, getBasicUserInfo, getDecodedIDToken } = useAuthContext();
  const backend = useBackendSession();
  const [accessToken, setAccessToken] = useState<string | null>(null);
  const [userProfile, setUserProfile] = useState<Record<string, unknown> | undefined>();
  const [idClaims, setIdClaims] = useState<Record<string, unknown>>({});
  const [lastSyncedToken, setLastSyncedToken] = useState<string | null>(null);
  const [selectedStepOrder, setSelectedStepOrder] = useState<number | null>(null);
  const [isInspectorCollapsed, setIsInspectorCollapsed] = useState(false);
  const [consentWindowError, setConsentWindowError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;

    async function loadAuthenticatedState() {
      if (!state.isAuthenticated) {
        setAccessToken(null);
        setUserProfile(undefined);
        setIdClaims({});
        setLastSyncedToken(null);
        return;
      }

      const nextAccessToken = (await getAccessToken()) as string;
      const nextUserProfile = (await getBasicUserInfo()) as Record<string, unknown>;
      const nextIdClaims = ((await getDecodedIDToken()) as Record<string, unknown>) ?? {};

      if (!active) {
        return;
      }

      setAccessToken(nextAccessToken);
      setUserProfile(nextUserProfile);
      setIdClaims(nextIdClaims);
    }

    void loadAuthenticatedState();

    return () => {
      active = false;
    };
  }, [state.isAuthenticated, getAccessToken, getBasicUserInfo, getDecodedIDToken]);

  useEffect(() => {
    if (!accessToken || accessToken === lastSyncedToken) {
      return;
    }
    void backend.syncUserToken(accessToken, {
      ...(userProfile ?? {}),
      ...(Object.keys(idClaims).length ? { id_token_claims: idClaims } : {}),
    });
    setLastSyncedToken(accessToken);
  }, [accessToken, lastSyncedToken, userProfile, idClaims]);

  useEffect(() => {
    if (selectedStepOrder !== null) {
      return;
    }
    setSelectedStepOrder(deriveSuggestedStepOrder(state.isAuthenticated, backend.session));
  }, [selectedStepOrder, state.isAuthenticated, backend.session]);

  useEffect(() => {
    function onMessage(event: MessageEvent) {
      if (event.data?.type === "obo-callback-complete") {
        void backend.refreshSession();
      }
    }

    window.addEventListener("message", onMessage);
    return () => window.removeEventListener("message", onMessage);
  }, []);

  function openConsentWindow() {
    setConsentWindowError(null);
    const authUrl = backend.session?.artifacts.delegation.authorization_url.raw;
    if (!authUrl) {
      setConsentWindowError("No hay URL de consentimiento disponible. Ejecuta antes 'Iniciar delegacion OBO'.");
      return;
    }
    const popup = window.open(authUrl, "obo-consent", "popup=yes,width=680,height=800");
    if (!popup) {
      setConsentWindowError(
        "El navegador bloqueo la ventana emergente de consentimiento. Habilita popups para este sitio.",
      );
      return;
    }
    popup.focus();
  }

  const canStartUserLogin = !authConfigValidationError;
  const panelError = consentWindowError ?? backend.error ?? authConfigValidationError;
  const mainColumnClassName = isInspectorCollapsed
    ? "col-12 col-xl-11 col-xxl-11"
    : "col-12 col-xl-7 col-xxl-8";
  const inspectorColumnClassName = isInspectorCollapsed
    ? "col-12 col-xl-1 col-xxl-1 inspector-host is-collapsed"
    : "col-12 col-xl-5 col-xxl-4 inspector-host";

  return (
    <div className="app-shell container-fluid py-2 px-2 px-lg-3">
      <div className="row g-2 g-xl-3 align-items-start">
        <main className={mainColumnClassName}>
          <div className="center-column">
            <header className="hero-panel panel">
              <div className="hero-branding">
                <a
                  className="hero-logo-link"
                  href="https://wso2.com"
                  target="_blank"
                  rel="noreferrer"
                  aria-label="Open WSO2 homepage"
                >
                  <img
                    className="hero-logo"
                    src="https://wso2.cachefly.net/wso2/sites/all/image_resources/logos/WSO2-Logo-Black.webp"
                    alt="WSO2 logo"
                    loading="lazy"
                  />
                </a>
                <div className="hero-copy">
                  <p className="eyebrow">WSO2 Identity Server 7.2</p>
                  <h1>On-Behalf-Of Protocol Lab</h1>
                  <p className="hero-subtitle">
                    Flujo didactico con identidad de usuario, agente y delegacion OBO con trazas completas.
                  </p>
                </div>
              </div>
            </header>

            <StepRunnerPanel
              isAuthenticated={state.isAuthenticated}
              session={backend.session}
              selectedStepOrder={selectedStepOrder}
              onSelectStep={setSelectedStepOrder}
              loadingAction={backend.loadingAction}
              error={panelError}
              canStartUserLogin={canStartUserLogin}
              onLogin={() => {
                if (canStartUserLogin) {
                  void signIn();
                }
              }}
              onLogout={() => {
                backend.resetSession();
                setSelectedStepOrder(null);
                void signOut();
              }}
              onRefresh={backend.refreshSession}
              onFetchAgentToken={backend.fetchAgentToken}
              onStartObo={backend.startObo}
              onExchangeObo={backend.exchangeObo}
              onOpenConsent={openConsentWindow}
              onTestUserAccess={() => backend.testUserAccess({ resource_path: "/files/me", method: "GET" })}
              onTestAgentAccess={() => backend.testAgentAccess({ resource_path: "/files/me", method: "GET" })}
              onTestOboRead={() => backend.testOboAccess({ resource_path: "/files/me", method: "GET" })}
              onUploadWithObo={() => backend.uploadWithObo("generated-report.txt")}
              onShareWithObo={() => backend.shareWithObo("usr-1", "security-team@example.com")}
            />
            <TraceViewer traces={backend.session?.traces ?? []} selectedStepOrder={selectedStepOrder} />
          </div>
        </main>

        <aside className={inspectorColumnClassName}>
          <section className={`panel inspector-dock ${isInspectorCollapsed ? "is-collapsed" : ""}`}>
            <div className="panel__header inspector-dock__header">
              <div className="inspector-dock__title-row">
                <h2 className="inspector-dock__title">Inspector</h2>
                <p className="muted inspector-dock__subtitle">Estado del protocolo y artefactos</p>
              </div>
              <button
                type="button"
                className="collapse-toggle inspector-dock__toggle"
                onClick={() => setIsInspectorCollapsed((current) => !current)}
                aria-expanded={!isInspectorCollapsed}
                aria-label={isInspectorCollapsed ? "Expandir inspector" : "Colapsar inspector"}
                title={isInspectorCollapsed ? "Expandir inspector" : "Colapsar inspector"}
              >
                {isInspectorCollapsed ? "◀" : "▶"}
              </button>
            </div>
            <div className="inspector-dock__body">
              <ArtifactInspector
                session={backend.session}
                selectedStepOrder={selectedStepOrder}
                showHeader={false}
              />
            </div>
          </section>
        </aside>
      </div>
    </div>
  );
}
