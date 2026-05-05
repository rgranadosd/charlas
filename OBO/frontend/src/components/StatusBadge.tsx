interface StatusBadgeProps {
  label: string;
}

export function StatusBadge({ label }: StatusBadgeProps) {
  const normalized = label.toLowerCase();
  const className = normalized.includes("available") || normalized.includes("ok")
    ? "status-badge is-ok"
    : normalized.includes("waiting") || normalized.includes("started")
      ? "status-badge is-warn"
      : normalized.includes("expired") || normalized.includes("error")
        ? "status-badge is-error"
        : "status-badge";

  return <span className={className}>{label}</span>;
}
