from __future__ import annotations

import unittest
from unittest.mock import patch

from oauth_session import OAuthCallbackHandler, OAuthClient
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


if __name__ == "__main__":
    unittest.main()