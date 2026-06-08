from __future__ import annotations

import unittest
from unittest.mock import patch

from oauth_session import OAuthCallbackHandler, OAuthClient
from oauth2_apim import get_gateway_access_token
from request_identity import CallerIdentity, use_caller_identity


class AuthContextTests(unittest.TestCase):
    def setUp(self) -> None:
        OAuthCallbackHandler.scopes = None
        OAuthCallbackHandler.access_token = None
        OAuthCallbackHandler.id_token_payload = None
        OAuthCallbackHandler.user_permissions = None

    def test_ensure_token_uses_request_scoped_caller_identity(self) -> None:
        client = OAuthClient(force_auth=False)

        with patch.object(client, "_decode_token_payload", return_value={"sub": "user-1", "scope": "openid offline_access"}):
            with patch.object(client, "_check_user_permissions", return_value={"View Products"}) as check_permissions:
                with use_caller_identity(CallerIdentity(access_token="caller-token", user_id="user-1")):
                    token = client.ensure_token()

        self.assertEqual(token, "caller-token")
        self.assertEqual(OAuthCallbackHandler.access_token, "caller-token")
        self.assertEqual(OAuthCallbackHandler.scopes, "openid offline_access")
        self.assertEqual(OAuthCallbackHandler.user_permissions, {"View Products"})
        check_permissions.assert_called_once_with("user-1")

    def test_gateway_access_token_prefers_request_scoped_identity(self) -> None:
        with use_caller_identity(CallerIdentity(access_token="caller-token", user_id="user-1")):
            self.assertEqual(get_gateway_access_token(), "caller-token")

    def test_gateway_access_token_uses_cached_end_user_token(self) -> None:
        with patch("oauth2_apim.Path.read_text", return_value='{"access_token": "cached-user-token", "expires_at": 9999999999}'):
            self.assertEqual(get_gateway_access_token(), "cached-user-token")


if __name__ == "__main__":
    unittest.main()