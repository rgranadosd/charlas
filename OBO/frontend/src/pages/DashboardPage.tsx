import { useEffect, useState } from "react";
import { useAuthContext } from "@asgardeo/auth-react";

import { ArtifactInspector } from "../components/ArtifactInspector";
import { StepRunnerPanel } from "../components/StepRunnerPanel";
import { TraceViewer } from "../components/TraceViewer";
import { authConfigValidationError } from "../config/env";
import { useBackendSession } from "../hooks/useBackendSession";

interface DashboardPageProps {
  theme: "light" | "dark";
  onToggleTheme: () => void;
}

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

export function DashboardPage({ theme, onToggleTheme }: DashboardPageProps) {
  const { state, signIn, signOut, getAccessToken, getBasicUserInfo, getDecodedIDToken } = useAuthContext();
  const backend = useBackendSession();
  const [accessToken, setAccessToken] = useState<string | null>(null);
  const [userProfile, setUserProfile] = useState<Record<string, unknown> | undefined>();
  const [idClaims, setIdClaims] = useState<Record<string, unknown>>({});
  const [lastSyncedToken, setLastSyncedToken] = useState<string | null>(null);
  const [selectedStepOrder, setSelectedStepOrder] = useState<number | null>(null);

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
    const authUrl = backend.session?.artifacts.delegation.authorization_url.raw;
    if (!authUrl) {
      return;
    }
    window.open(authUrl, "obo-consent", "popup=yes,width=680,height=800");
  }

  const canStartUserLogin = !authConfigValidationError;
  const panelError = backend.error ?? authConfigValidationError;

  return (
    <div className="app-shell container-fluid py-2 px-2 px-lg-3">
      <div className="row g-2 g-xl-3 align-items-start">
        <main className="col-12 col-xl-7 col-xxl-8">
          <div className="center-column">
            <header className="hero-panel panel">
              <div>
                <h1>On-Behalf-Of Protocol Lab</h1>
              </div>
              <div className="hero-actions">
                <button type="button" className="ghost-button" onClick={onToggleTheme}>
                  Theme: {theme}
                </button>
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

        <div className="col-12 col-xl-5 col-xxl-4">
          <ArtifactInspector session={backend.session} selectedStepOrder={selectedStepOrder} />
        </div>
      </div>
    </div>
  );
}
