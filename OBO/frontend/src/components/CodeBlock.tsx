import { useState } from "react";

interface CodeBlockProps {
  title?: string;
  value: unknown;
  collapsible?: boolean;
  showHeader?: boolean;
}

export function CodeBlock({ title, value, collapsible = false, showHeader = true }: CodeBlockProps) {
  const [expanded, setExpanded] = useState(!collapsible);
  const stringValue = typeof value === "string" ? value : JSON.stringify(value, null, 2);

  async function copy() {
    try {
      await navigator.clipboard.writeText(stringValue);
      return;
    } catch {
      const textarea = document.createElement("textarea");
      textarea.value = stringValue;
      textarea.setAttribute("readonly", "true");
      textarea.style.position = "absolute";
      textarea.style.left = "-9999px";
      document.body.appendChild(textarea);
      textarea.select();
      document.execCommand("copy");
      document.body.removeChild(textarea);
    }
  }

  return (
    <div className="code-block">
      {showHeader ? (
        <div className="code-block__header">
          <div className="code-block__title">
            {collapsible ? (
              <button
                type="button"
                className="collapse-toggle"
                onClick={() => setExpanded((current) => !current)}
                aria-label={expanded ? "Colapsar" : "Expandir"}
                title={expanded ? "Colapsar" : "Expandir"}
              >
                {expanded ? "▼" : "▶"}
              </button>
            ) : null}
            {title ? <strong>{title}</strong> : <span />}
          </div>
          <div className="code-block__actions">
            <button
              type="button"
              className="ghost-button icon-button"
              onClick={() => void copy()}
              aria-label="Copiar"
              title="Copiar"
            >
              ⧉
            </button>
          </div>
        </div>
      ) : null}
      {expanded ? <pre>{stringValue}</pre> : null}
    </div>
  );
}
