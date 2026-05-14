import { useState } from "react";

import type { SessionResponse } from "../types/models";
import { StatusBadge } from "./StatusBadge";

interface StepRunnerPanelProps {
  isAuthenticated: boolean;
  session: SessionResponse | null;
  selectedStepOrder: number | null;
  onSelectStep: (stepOrder: number) => void;
  loadingAction: string | null;
  error: string | null;
  canStartUserLogin: boolean;
  onLogin: () => void;
  onLogout: () => void;
  onRefresh: () => Promise<unknown>;
  onFetchAgentToken: () => Promise<unknown>;
  onStartObo: () => Promise<unknown>;
  onExchangeObo: () => Promise<unknown>;
  onOpenConsent: () => void;
  onTestUserAccess: () => Promise<unknown>;
  onTestAgentAccess: () => Promise<unknown>;
  onTestOboRead: () => Promise<unknown>;
  onUploadWithObo: () => Promise<unknown>;
  onShareWithObo: () => Promise<unknown>;
}

export function StepRunnerPanel({
  isAuthenticated,
  session,
  selectedStepOrder,
  onSelectStep,
  loadingAction,
  error,
  canStartUserLogin,
  onLogin,
  onLogout,
  onRefresh,
  onFetchAgentToken,
  onStartObo,
  onExchangeObo,
  onOpenConsent,
  onTestUserAccess,
  onTestAgentAccess,
  onTestOboRead,
  onUploadWithObo,
  onShareWithObo,
}: StepRunnerPanelProps) {
  const [failedStepOrders, setFailedStepOrders] = useState<number[]>([]);

  const userPhaseDone = isAuthenticated;
  const userTokenSynced = session?.artifacts.user.available ?? false;
  const agentPhaseDone = session?.artifacts.agent.available ?? false;
  const latestUserAccessTrace = session?.traces.find(
    (trace) => trace.action === "Probar acceso con USER_TOKEN",
  );
  const latestAgentAccessTrace = session?.traces.find(
    (trace) => trace.action === "Probar acceso con AGENT_TOKEN",
  );
  const userAccessAllowed =
    latestUserAccessTrace !== undefined && latestUserAccessTrace.response_status < 400;
  const userAccessRejected =
    latestUserAccessTrace !== undefined && latestUserAccessTrace.response_status >= 400;
  const agentAccessAllowed =
    latestAgentAccessTrace !== undefined && latestAgentAccessTrace.response_status < 400;
  const agentAccessRejected =
    latestAgentAccessTrace !== undefined && latestAgentAccessTrace.response_status >= 400;
  const contrastAccessDone = userAccessAllowed && agentAccessRejected;
  const contrastAccessFailed = userAccessRejected || agentAccessAllowed || failedStepOrders.includes(3);
  const delegationPhaseDone = session?.artifacts.delegation.status === "available";
  const consentPhaseDone = session?.artifacts.authorization_code.status === "available";
  const oboPhaseDone = session?.artifacts.obo.available ?? false;
  const latestOboReadTrace = session?.traces.find(
    (trace) => trace.action === "Leer mis ficheros con OBO_TOKEN",
  );
  const oboReadDone = latestOboReadTrace !== undefined && latestOboReadTrace.response_status < 400;
  const oboReadFailed = latestOboReadTrace !== undefined && latestOboReadTrace.response_status >= 400;

  const guidedSteps = [
    {
      order: 1,
      label: "Login usuario",
      done: userPhaseDone,
      failed: failedStepOrders.includes(1),
    },
    {
      order: 2,
      label: "Obtener AGENT_TOKEN",
      done: agentPhaseDone,
      failed: failedStepOrders.includes(2),
    },
    {
      order: 3,
      label: "Comparar USER_TOKEN vs AGENT_TOKEN",
      done: contrastAccessDone,
      failed: contrastAccessFailed,
    },
    {
      order: 4,
      label: "Iniciar delegacion OBO",
      done: delegationPhaseDone,
      failed: failedStepOrders.includes(4),
    },
    {
      order: 5,
      label: "Abrir pantalla de consentimiento",
      done: consentPhaseDone,
      failed: failedStepOrders.includes(5),
    },
    {
      order: 6,
      label: "Intercambiar code por OBO_TOKEN",
      done: oboPhaseDone,
      failed: failedStepOrders.includes(6),
    },
    {
      order: 7,
      label: "Leer mis ficheros con OBO_TOKEN",
      done: oboReadDone,
      failed: oboReadFailed || failedStepOrders.includes(7),
    },
  ];

  const completedGuidedSteps = guidedSteps.filter((step) => step.done).length;
  const nextGuidedStep = guidedSteps.find((step) => !step.done) ?? null;
  const canTestUserAccess = userTokenSynced && agentPhaseDone;
  const canTestAgentAccess = userTokenSynced && agentPhaseDone;

  function getStepClass(order: number, done: boolean, failed: boolean) {
    if (done) {
      return "is-complete";
    }

    if (failed) {
      return "is-error";
    }

    if (nextGuidedStep?.order === order) {
      return "is-next";
    }

    return "is-pending";
  }

  function getStepStateLabel(order: number, done: boolean, failed: boolean) {
    if (done) {
      return "Completado";
    }

    if (failed) {
      return "Error";
    }

    if (nextGuidedStep?.order === order) {
      return "Siguiente";
    }

    return "Pendiente";
  }

  const guidedActions: Record<number, { onClick: () => Promise<unknown> | void; disabled: boolean }> = {
    1: {
      onClick: onLogin,
      disabled: !canStartUserLogin,
    },
    2: {
      onClick: onFetchAgentToken,
      disabled: false,
    },
    3: {
      onClick: onTestAgentAccess,
      disabled: false,
    },
    4: {
      onClick: onStartObo,
      disabled: false,
    },
    5: {
      onClick: onOpenConsent,
      disabled: !session?.artifacts.delegation.authorization_url.raw,
    },
    6: {
      onClick: onExchangeObo,
      disabled: false,
    },
    7: {
      onClick: onTestOboRead,
      disabled: false,
    },
  };

  async function runStepAction(order: number, action: () => Promise<unknown> | void) {
    onSelectStep(order);

    try {
      await action();
      setFailedStepOrders((current) => current.filter((stepOrder) => stepOrder !== order));
    } catch {
      setFailedStepOrders((current) =>
        current.includes(order) ? current : [...current, order],
      );
    }
  }

  async function handleStepClick(order: number) {
    const action = guidedActions[order];
    if (!action || action.disabled) {
      return;
    }

    await runStepAction(order, action.onClick);
  }

  function getContrastCardClass(trace: SessionResponse["traces"][number] | undefined, enabled: boolean) {
    if (!trace) {
      return enabled ? "is-pending" : "is-locked";
    }

    return trace.response_status < 400 ? "is-allowed" : "is-denied";
  }

  function getContrastCardStateLabel(trace: SessionResponse["traces"][number] | undefined, enabled: boolean) {
    if (!trace) {
      return enabled ? "Pendiente" : "Bloqueado";
    }

    return trace.response_status < 400 ? "Permitido" : "Denegado";
  }

  return (
    <section className="panel step-panel">
      <div className="panel__header">
        <div>
          <p className="eyebrow">Happy Path</p>
        </div>
        <StatusBadge label={loadingAction ?? "idle"} />
      </div>

      <div className="happy-path-layout">
        <div className="happy-path-flow" role="list" aria-label="Flujo guiado del protocolo">
          {guidedSteps.map((step, index) => {
            const action = guidedActions[step.order as keyof typeof guidedActions];

            if (step.order === 3) {
              return (
                <div key={step.order} className="happy-step-node" role="listitem">
                  <div
                    className={`happy-step happy-step--contrast ${getStepClass(step.order, step.done, step.failed)} ${selectedStepOrder === step.order ? "is-selected" : ""}`}
                  >
                    <div className="happy-step__topline">
                      <span className="button-order">{step.order}</span>
                      <span className="happy-step__state">{getStepStateLabel(step.order, step.done, step.failed)}</span>
                    </div>
                    <span className="happy-step__title">{step.label}</span>
                    <div className="happy-step-contrast-grid">
                      <button
                        type="button"
                        className={`happy-substep ${getContrastCardClass(latestUserAccessTrace, canTestUserAccess)}`}
                        onClick={() => {
                          void runStepAction(3, onTestUserAccess);
                        }}
                        disabled={!canTestUserAccess}
                      >
                        <span className="happy-substep__token">USER_TOKEN</span>
                        <span className="happy-substep__state">{getContrastCardStateLabel(latestUserAccessTrace, canTestUserAccess)}</span>
                        <span className="happy-substep__hint">Con USER_TOKEN el acceso al recurso debe permitirse.</span>
                        <span className="happy-substep__status-code">{latestUserAccessTrace?.response_status ?? "--"}</span>
                      </button>
                      <button
                        type="button"
                        className={`happy-substep ${getContrastCardClass(latestAgentAccessTrace, canTestAgentAccess)}`}
                        onClick={() => {
                          void runStepAction(3, onTestAgentAccess);
                        }}
                        disabled={!canTestAgentAccess}
                      >
                        <span className="happy-substep__token">AGENT_TOKEN</span>
                        <span className="happy-substep__state">{getContrastCardStateLabel(latestAgentAccessTrace, canTestAgentAccess)}</span>
                        <span className="happy-substep__hint">Con AGENT_TOKEN el acceso debe denegarse sin delegacion OBO.</span>
                        <span className="happy-substep__status-code">{latestAgentAccessTrace?.response_status ?? "--"}</span>
                      </button>
                    </div>
                  </div>
                  {index < guidedSteps.length - 1 ? <div className="happy-step-arrow" aria-hidden="true" /> : null}
                </div>
              );
            }

            return (
              <div key={step.order} className="happy-step-node" role="listitem">
                <button
                  type="button"
                  className={`happy-step ${getStepClass(step.order, step.done, step.failed)} ${selectedStepOrder === step.order ? "is-selected" : ""} ${action.disabled ? "is-action-disabled" : ""}`}
                  onClick={() => {
                    void handleStepClick(step.order);
                  }}
                  aria-disabled={action.disabled}
                >
                  <div className="happy-step__topline">
                    <span className="button-order">{step.order}</span>
                    <span className="happy-step__state">{getStepStateLabel(step.order, step.done, step.failed)}</span>
                  </div>
                  <span className="happy-step__title">{step.label}</span>
                </button>
                {index < guidedSteps.length - 1 ? <div className="happy-step-arrow" aria-hidden="true" /> : null}
              </div>
            );
          })}
        </div>
      </div>

      <div className="row g-3 step-detail-grid">
        <div className="col-12 col-lg-4">
          <div className="step-summary detail-card h-100">
            <div>
              <p className="step-summary__label">Progreso del flujo</p>
              <p className="step-summary__value">
                {completedGuidedSteps}/{guidedSteps.length} pasos guiados completados
              </p>
            </div>
            <div>
              <p className="step-summary__label">Sincronizacion automatica</p>
              <p className="step-summary__value">
                {userTokenSynced ? "USER_TOKEN disponible para inspeccion" : "USER_TOKEN pendiente"}
              </p>
            </div>
            <div>
              <p className="step-summary__label">Siguiente paso</p>
              <p className="step-summary__value">
                {nextGuidedStep ? `${nextGuidedStep.order}. ${nextGuidedStep.label}` : "Flujo guiado completado"}
              </p>
            </div>
          </div>
        </div>

        <div className="col-12 col-lg-4">
          <div className="detail-card detail-card--actions h-100">
            <div>
              <p className="step-summary__label">Sesion</p>
              <p className="detail-copy">Controles auxiliares fuera del happy path.</p>
            </div>
            <button type="button" className="ghost-button" onClick={onLogout}>
              Logout usuario
            </button>
            <button type="button" className="ghost-button" onClick={() => void onRefresh()}>
              Refrescar sesion
            </button>
          </div>
        </div>

        <div className="col-12 col-lg-4">
          <div className="detail-card detail-card--actions h-100">
            <div>
              <p className="step-summary__label">Operaciones OBO extra</p>
              <p className="detail-copy">Acciones posteriores al flujo principal.</p>
            </div>
            <button type="button" className="ghost-button" onClick={() => void onUploadWithObo()}>
              8. Subir fichero con OBO_TOKEN
            </button>
            <button type="button" className="ghost-button" onClick={() => void onShareWithObo()}>
              9. Compartir fichero con OBO_TOKEN
            </button>
          </div>
        </div>
      </div>

      {error ? <p className="error-text">{error}</p> : null}
    </section>
  );
}
