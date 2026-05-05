export interface SecretValue {
  available: boolean;
  preview: string | null;
  raw: string | null;
}

export interface TokenArtifact {
  status: string;
  available: boolean;
  preview: string | null;
  raw: string | null;
  claims: Record<string, unknown>;
  scopes: string[];
  subject: string | null;
  actor: string | null;
  issuer: string | null;
  audience: unknown;
  expires_at: string | null;
  explanation: string | null;
  consumer: string | null;
  issued_at: string | null;
}

export interface DelegationArtifact {
  status: string;
  authorization_url: SecretValue;
  state: SecretValue;
  code_verifier: SecretValue;
  code_challenge: SecretValue;
  scopes: string[];
  configured_agent_id: string | null;
  oauth_client_id: string | null;
  started_at: string | null;
}

export interface AuthorizationCodeArtifact {
  status: string;
  value: SecretValue;
  state_validated: boolean;
  received_at: string | null;
}

export interface SessionArtifacts {
  user: TokenArtifact;
  agent: TokenArtifact;
  delegation: DelegationArtifact;
  authorization_code: AuthorizationCodeArtifact;
  obo: TokenArtifact;
}

export interface ComparisonRow {
  artifact: string;
  issuer: string | null;
  subject: string | null;
  actor: string | null;
  use: string;
  status: string;
}

export interface TraceEntry {
  timestamp: string;
  action: string;
  endpoint: string;
  method: string;
  request_parameters: unknown;
  response_status: number;
  response_body: unknown;
  functional_interpretation: string;
  security_interpretation: string;
}

export interface SessionResponse {
  session_id: string;
  created_at: string;
  updated_at: string;
  configured_agent_id: string | null;
  oauth_client_id: string | null;
  token_sub: string | null;
  sub_matches_client_id: boolean;
  token_authentication_type: string | null;
  agent_token_claims: Record<string, unknown>;
  security_meaning: string | null;
  delegated_user_id: string | null;
  delegated_agent_id: string | null;
  artifacts: SessionArtifacts;
  comparison_rows: ComparisonRow[];
  last_api_request: unknown;
  last_api_response: unknown;
  last_security_explanation: string | null;
  traces: TraceEntry[];
  snapshot: Record<string, unknown>;
}

export interface ProtectedAccessRequest {
  resource_path?: string;
  method?: string;
  payload?: Record<string, unknown>;
}
