import { useState } from "react";
import type { SessionResponse } from "../types/models";
import { ClaimsViewer } from "./ClaimsViewer";
import { CodeBlock } from "./CodeBlock";
import { ScopeChips } from "./ScopeChips";
import { StatusBadge } from "./StatusBadge";
import { TokenCard } from "./TokenCard";

interface ArtifactInspectorProps {
  session: SessionResponse | null;
  selectedStepOrder: number | null;
  showHeader?: boolean;
}

interface CollapsibleInspectorPanelProps {
  title: string;
  subtitle?: string;
  statusLabel?: string;
  defaultExpanded?: boolean;
  children: React.ReactNode;
}

interface IdentityMeaningRow {
  field: string;
  meaning: string;
}

function CollapsibleInspectorPanel({
  title,
  subtitle,
  statusLabel,
  defaultExpanded = false,
  children,
}: CollapsibleInspectorPanelProps) {
  const [expanded, setExpanded] = useState(defaultExpanded);

  return (
    <section className="panel">
      <div className="panel__header">
        <div className="panel-collapsible-title">
          <button
            type="button"
            className="collapse-toggle"
            onClick={() => setExpanded((current) => !current)}
            aria-label={expanded ? "Colapsar panel" : "Expandir panel"}
            title={expanded ? "Colapsar panel" : "Expandir panel"}
          >
            {expanded ? "▼" : "▶"}
          </button>
          <div>
            <h3>{title}</h3>
            {subtitle ? <p>{subtitle}</p> : null}
          </div>
        </div>
        {statusLabel ? <StatusBadge label={statusLabel} /> : null}
      </div>
      {expanded ? <div className="panel-collapsible-content">{children}</div> : null}
    </section>
  );
}

function formatInlineValue(value: unknown): string {
  if (value === null || value === undefined) {
    return "n/a";
  }
  if (Array.isArray(value)) {
    return value.join(", ") || "n/a";
  }
  if (typeof value === "object") {
    return JSON.stringify(value);
  }
  const normalized = String(value);
  return normalized.trim() ? normalized : "n/a";
}

const STEP_2_IDENTITY_ROWS: IdentityMeaningRow[] = [
  {
    field: "AGENT_ID",
    meaning: "Identidad lógica del agente en WSO2",
  },
  {
    field: "client_id",
    meaning: "Identidad técnica del cliente OAuth",
  },
  {
    field: "sub",
    meaning: "Subject técnico del token",
  },
  {
    field: "act.sub",
    meaning: "Agente delegado dentro del OBO token",
  },
];

const STEP_LABELS: Record<number, string> = {
  1: "Login usuario",
  2: "Obtener AGENT_TOKEN",
  3: "Comparar USER_TOKEN vs AGENT_TOKEN",
  4: "Iniciar delegacion OBO",
  5: "Abrir pantalla de consentimiento",
  6: "Intercambiar code por OBO_TOKEN",
  7: "Leer mis ficheros con OBO_TOKEN",
};

const STEP_EXPLANATIONS: Record<number, { title: string; body: string }> = {
  1: {
    title: "Resumen",
    body: "Este bloque identifica al usuario que ha iniciado sesion en la SPA.",
  },
  2: {
    title: "Resumen",
    body: "En el paso 2 no se espera ver agent_id dentro del AGENT_TOKEN. El agent_id lógico viene de configuración; la identidad técnica del token se muestra como client_id/sub; la identidad delegada del agente aparecerá en act.sub cuando exista OBO_TOKEN.",
  },
  3: {
    title: "Resumen",
    body: "Aqui se contrasta el mismo recurso con ambos tokens: USER_TOKEN debe permitir acceso al recurso del usuario y AGENT_TOKEN debe quedar denegado porque no aporta contexto delegado.",
  },
  4: {
    title: "Resumen",
    body: "La delegacion arranca usando la identidad logica del agente ya configurada y el cliente OAuth ya autenticado, pero todavia no existe actor delegado en el token.",
  },
  5: {
    title: "Resumen",
    body: "El authorization code prueba consentimiento del usuario. Aun no redefine la identidad del agente; eso solo queda fijado en el token delegado final.",
  },
  6: {
    title: "Resumen",
    body: "Despues del OBO, la trazabilidad correcta es sub para el usuario y act.sub para el agente delegado.",
  },
  7: {
    title: "Resumen",
    body: "Si la llamada final funciona, es porque el OBO token ya expresa al usuario en sub y al agente delegado en act.sub para auditoria y autorizacion.",
  },
};

export function ArtifactInspector({
  session,
  selectedStepOrder,
  showHeader = true,
}: ArtifactInspectorProps) {
  const user = session?.artifacts.user;
  const agent = session?.artifacts.agent;
  const delegation = session?.artifacts.delegation;
  const authCode = session?.artifacts.authorization_code;
  const obo = session?.artifacts.obo;
  const selectedStepLabel = selectedStepOrder ? STEP_LABELS[selectedStepOrder] : null;

  const showUser = selectedStepOrder === null || selectedStepOrder === 1 || selectedStepOrder === 3;
  const showAgent = selectedStepOrder === null || selectedStepOrder === 2 || selectedStepOrder === 3;
  const showDelegation =
    selectedStepOrder === null || selectedStepOrder === 4 || selectedStepOrder === 5;
  const showAuthorizationCode =
    selectedStepOrder === null || selectedStepOrder === 5 || selectedStepOrder === 6;
  const showObo = selectedStepOrder === null || selectedStepOrder === 6 || selectedStepOrder === 7;
  const showAgentRegistrationIdentity =
    selectedStepOrder === null || selectedStepOrder === 2 || selectedStepOrder === 3 || selectedStepOrder === 4 || selectedStepOrder === 5;
  const showOAuthClientIdentity =
    selectedStepOrder === null || selectedStepOrder === 2 || selectedStepOrder === 3 || selectedStepOrder === 4 || selectedStepOrder === 5;
  const showDelegatedActorIdentity =
    selectedStepOrder === null || selectedStepOrder === 6 || selectedStepOrder === 7;

  const showDecodedClaims =
    selectedStepOrder === null || selectedStepOrder === 1 || selectedStepOrder === 2 || selectedStepOrder === 3 || selectedStepOrder === 6 || selectedStepOrder === 7;

  const tokenClaimsInView =
    selectedStepOrder === 1
      ? user?.claims ?? {}
      : selectedStepOrder === 2 || selectedStepOrder === 3
        ? agent?.claims ?? {}
        : selectedStepOrder === 6 || selectedStepOrder === 7
          ? obo?.claims ?? {}
          : null;

  const showDecodedClaimsPanel = showDecodedClaims && tokenClaimsInView === null;

  const activeExplanation = selectedStepOrder ? STEP_EXPLANATIONS[selectedStepOrder] : null;

  const decodedClaims =
    selectedStepOrder === 1
      ? user?.claims ?? {}
      : selectedStepOrder === 2 || selectedStepOrder === 3
        ? agent?.claims ?? {}
        : selectedStepOrder === 6 || selectedStepOrder === 7
          ? obo?.claims ?? {}
          : obo?.available
            ? obo.claims
            : agent?.available
              ? agent.claims
              : user?.claims ?? {};

    const userSubject = user?.subject ?? null;
    const agentSubject = agent?.subject ?? null;
    const oboSubject = obo?.subject ?? null;
    const userSubMatchesAgentSub =
      userSubject !== null && agentSubject !== null && userSubject === agentSubject;
    const agentSubMatchesOboSub =
      agentSubject !== null && oboSubject !== null && agentSubject === oboSubject;

  let visiblePanelIndex = 0;
  const getDefaultExpanded = () => {
    const next = visiblePanelIndex === 0;
    visiblePanelIndex += 1;
    return next;
  };

  return (
    <aside className="inspector-column">
      <div className="inspector-sticky">
        {showHeader ? (
          <div className="inspector-title-row">
            <div>
              <h2>Inspector</h2>
              {selectedStepLabel ? <p className="muted">Mostrando datos de: {selectedStepOrder}. {selectedStepLabel}</p> : null}
            </div>
            <StatusBadge label={session ? "available" : "not-started"} />
          </div>
        ) : null}

        {showUser && user ? (
          <TokenCard
            key={`user-${selectedStepOrder ?? "all"}`}
            title="User Session"
            artifact={user}
            defaultExpanded={getDefaultExpanded()}
          />
        ) : null}
        {showAgentRegistrationIdentity ? <CollapsibleInspectorPanel
          key={`agent-registration-${selectedStepOrder ?? "all"}`}
          title="Configured Agent Identity"
          subtitle="AGENT_ID definido en backend / WSO2 agent registration"
          defaultExpanded={getDefaultExpanded()}
        >
          <dl className="meta-grid">
            <div>
              <dt>AGENT_ID</dt>
              <dd>{session?.configured_agent_id ?? "n/a"}</dd>
            </div>
            <div>
              <dt>source</dt>
              <dd>backend config / WSO2 agent registration</dd>
            </div>
          </dl>
          <p className="inspector-explanation-panel__body">Esta es la identidad logica del agente. No se deriva de claims del token ni de identificadores tecnicos del cliente OAuth.</p>
        </CollapsibleInspectorPanel> : null}
        {showOAuthClientIdentity ? <CollapsibleInspectorPanel
          key={`oauth-client-${selectedStepOrder ?? "all"}`}
          title="OAuth Client Identity"
          subtitle="Cliente OAuth autenticado con AGENT_TOKEN"
          defaultExpanded={getDefaultExpanded()}
        >
          <dl className="meta-grid">
            <div>
              <dt>oauth_client_id</dt>
              <dd>{session?.oauth_client_id ?? "n/a"}</dd>
            </div>
            <div>
              <dt>token_sub</dt>
              <dd>{session?.token_sub ?? "n/a"}</dd>
            </div>
            <div>
              <dt>sub_matches_client_id</dt>
              <dd>{session?.sub_matches_client_id ? "true" : "false"}</dd>
            </div>
            <div>
              <dt>token_authentication_type</dt>
              <dd>{session?.token_authentication_type ?? "n/a"}</dd>
            </div>
            <div>
              <dt>aud</dt>
              <dd>{formatInlineValue(agent?.audience)}</dd>
            </div>
          </dl>
          {session?.sub_matches_client_id || userSubMatchesAgentSub || agentSubMatchesOboSub ? (
            <div className="identity-badge-row">
              {session?.sub_matches_client_id ? (
                <span
                  className="semantic-badge semantic-badge--warning"
                  title="Coinciden en este token, pero no deben interpretarse como el agent_id lógico."
                >
                  Atencion: sub coincide con client_id
                </span>
              ) : null}
              {userSubMatchesAgentSub ? (
                <span
                  className="semantic-badge semantic-badge--warning"
                  title="USER_TOKEN y AGENT_TOKEN comparten el mismo sub. Revisa el contexto del grant para no mezclar identidades."
                >
                  Atencion: USER_TOKEN y AGENT_TOKEN comparten sub
                </span>
              ) : null}
              {agentSubMatchesOboSub ? (
                <span
                  className="semantic-badge semantic-badge--warning"
                  title="AGENT_TOKEN y OBO_TOKEN comparten sub. En OBO, el actor delegado debe revisarse en act.sub."
                >
                  Atencion: AGENT_TOKEN y OBO_TOKEN comparten sub
                </span>
              ) : null}
            </div>
          ) : null}
          <div className="identity-callout">
            <p className="identity-callout__title">Security meaning</p>
            <p className="identity-callout__body">{session?.security_meaning ?? "n/a"}</p>
          </div>
          <div className="identity-meaning-table-wrapper">
            <table className="identity-meaning-table">
              <thead>
                <tr>
                  <th>Campo</th>
                  <th>Significado</th>
                </tr>
              </thead>
              <tbody>
                {STEP_2_IDENTITY_ROWS.map((row) => (
                  <tr key={row.field}>
                    <td>{row.field}</td>
                    <td>{row.meaning}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <ScopeChips scopes={agent?.scopes ?? []} />
          <p className="inspector-explanation-panel__body">Esto representa la identidad técnica del cliente OAuth autenticado en WSO2. No sustituye al agent_id lógico.</p>
        </CollapsibleInspectorPanel> : null}
        {showAgent && agent ? (
          <TokenCard
            key={`agent-${selectedStepOrder ?? "all"}`}
            title="Agent Token"
            artifact={agent}
            defaultExpanded={getDefaultExpanded()}
          />
        ) : null}

        {showDelegation ? <CollapsibleInspectorPanel
          key={`delegation-${selectedStepOrder ?? "all"}`}
          title="Delegation State"
          subtitle="Rastrea state, PKCE y la URL de consentimiento."
          statusLabel={delegation?.status ?? "not-started"}
          defaultExpanded={getDefaultExpanded()}
        >
          <dl className="meta-grid">
            <div>
              <dt>state</dt>
              <dd>{delegation?.state.preview ?? "n/a"}</dd>
            </div>
            <div>
              <dt>configured_agent_id</dt>
              <dd>{delegation?.configured_agent_id ?? "n/a"}</dd>
            </div>
            <div>
              <dt>oauth_client_id</dt>
              <dd>{delegation?.oauth_client_id ?? "n/a"}</dd>
            </div>
            <div>
              <dt>started</dt>
              <dd>{delegation?.started_at ?? "n/a"}</dd>
            </div>
          </dl>
          <ScopeChips scopes={delegation?.scopes ?? []} />
          <CodeBlock title="authorization_url" value={delegation?.authorization_url.raw ?? "missing"} collapsible />
          <CodeBlock title="code_challenge" value={delegation?.code_challenge.raw ?? "missing"} collapsible />
          <CodeBlock title="code_verifier" value={delegation?.code_verifier.raw ?? delegation?.code_verifier.preview ?? "hidden"} collapsible />
        </CollapsibleInspectorPanel> : null}

        {showAuthorizationCode ? <CollapsibleInspectorPanel
          key={`authcode-${selectedStepOrder ?? "all"}`}
          title="Authorization Code"
          subtitle="Artefacto temporal obtenido tras consentimiento del usuario."
          statusLabel={authCode?.status ?? "not-started"}
          defaultExpanded={getDefaultExpanded()}
        >
          <p className="muted">state validado: {authCode?.state_validated ? "yes" : "no"}</p>
          <p className="muted">received_at: {authCode?.received_at ?? "n/a"}</p>
          <CodeBlock title="AUTHORIZATION_CODE" value={authCode?.value.raw ?? authCode?.value.preview ?? "missing"} collapsible />
        </CollapsibleInspectorPanel> : null}

        {showObo && obo ? (
          <TokenCard
            key={`obo-${selectedStepOrder ?? "all"}`}
            title="OBO Token"
            artifact={obo}
            defaultExpanded={getDefaultExpanded()}
          />
        ) : null}
        {showDelegatedActorIdentity ? <CollapsibleInspectorPanel
          key={`delegated-actor-${selectedStepOrder ?? "all"}`}
          title="Delegated Actor Identity"
          subtitle="Identidad efectiva despues del token exchange OBO"
          defaultExpanded={getDefaultExpanded()}
        >
          <dl className="meta-grid">
            <div>
              <dt>delegated_user_id</dt>
              <dd>{session?.delegated_user_id ?? "n/a"}</dd>
            </div>
            <div>
              <dt>delegated_agent_id</dt>
              <dd>{session?.delegated_agent_id ?? "n/a"}</dd>
            </div>
          </dl>
          <p className="inspector-explanation-panel__body">En el token delegado OBO, el usuario aparece en sub y el agente que actua en su nombre aparece en act.sub.</p>
        </CollapsibleInspectorPanel> : null}

        {showDecodedClaimsPanel ? <CollapsibleInspectorPanel
          key={`decoded-${selectedStepOrder ?? "all"}`}
          title="Decoded Claims"
          defaultExpanded={getDefaultExpanded()}
        >
          <ClaimsViewer title="Selected claims" claims={decodedClaims} />
        </CollapsibleInspectorPanel> : null}

        {activeExplanation ? <CollapsibleInspectorPanel
          key={`explanation-${selectedStepOrder ?? "all"}`}
          title={activeExplanation.title}
          defaultExpanded={getDefaultExpanded()}
        >
          <p className="inspector-explanation-panel__body">{activeExplanation.body}</p>
        </CollapsibleInspectorPanel> : null}
      </div>
    </aside>
  );
}
