from datetime import datetime, timedelta, timezone
import requests

from app.core.config import settings
from app.services.token_store import load_token_state, save_token_state, is_token_expired

TOKEN_URL = "https://api.mercadolibre.com/oauth/token"

class MercadoLivreAuthService:
    def _init_(self):
        self.client_id = settings.ML_CLIENT_ID
        self.client_secret = settings.ML_CLIENT_SECRET
        self.redirect_uri = settings.ML_REDIRECT_URI
        self.auth_code = settings.ML_AUTH_CODE

    def exchange_code_for_tokens(self):
        payload = {
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": self.auth_code,
            "redirect_uri": self.redirect_uri,
        }

        response = requests.post(
            TOKEN_URL,
            headers={
                "accept": "application/json",
                "content-type": "application/x-www-form-urlencoded",
            },
            data=payload,
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        self._persist_tokens(data)
        return data

    def refresh_access_token(self, refresh_token: str):
        payload = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": refresh_token,
        }

        response = requests.post(
            TOKEN_URL,
            headers={
                "accept": "application/json",
                "content-type": "application/x-www-form-urlencoded",
            },
            data=payload,
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        self._persist_tokens(data)
        return data

    def _persist_tokens(self, token_response: dict):
        expires_in = int(token_response.get("expires_in", 0))
        expires_at = datetime.now(timezone.utc) + timedelta(seconds=expires_in - 60)

        state = {
            "access_token": token_response.get("access_token", ""),
            "refresh_token": token_response.get("refresh_token", ""),
            "token_type": token_response.get("token_type", "bearer"),
            "expires_in": expires_in,
            "expires_at": expires_at.isoformat(),
            "user_id": token_response.get("user_id"),
            "scope": token_response.get("scope", ""),
        }
        save_token_state(state)

    def get_valid_access_token(self):
        state = load_token_state()

        if state.get("access_token") and not is_token_expired(state.get("expires_at", "")):
            return state["access_token"]

        if state.get("refresh_token"):
            refreshed = self.refresh_access_token(state["refresh_token"])
            return refreshed["access_token"]

        if self.auth_code:
            exchanged = self.exchange_code_for_tokens()
            return exchanged["access_token"]

        if settings.ML_ACCESS_TOKEN:
            return settings.ML_ACCESS_TOKEN

        raise RuntimeError("Nenhuma credencial válida do Mercado Livre disponível.")