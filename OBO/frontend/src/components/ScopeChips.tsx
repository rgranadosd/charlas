interface ScopeChipsProps {
  scopes: string[];
}

export function ScopeChips({ scopes }: ScopeChipsProps) {
  if (!scopes.length) {
    return <span className="muted">No scopes</span>;
  }

  return (
    <div className="scope-row">
      {scopes.map((scope) => (
        <span key={scope} className="scope-chip">
          {scope}
        </span>
      ))}
    </div>
  );
}
