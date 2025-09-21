from __future__ import annotations
import os, time, typing as T
from dataclasses import dataclass, field

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

from openai import OpenAI
from openai._exceptions import APIStatusError, APIConnectionError, RateLimitError, APITimeoutError

Json = T.Dict[str, T.Any]
Msgs = T.List[Json]

@dataclass
class SciBoxConfig:
    api_key: str = os.getenv("SCIBOX_API_KEY", "")
    base_url: str = os.getenv("SCIBOX_BASE_URL", "https://llm.t1v.scibox.tech/v1")
    chat_model: str = os.getenv("SCIBOX_MODEL", "Qwen2.5-72B-Instruct-AWQ")
    embed_model: str = os.getenv("SCIBOX_EMBED_MODEL", "bge-m3")
    temperature: float = float(os.getenv("SCIBOX_TEMPERATURE", "0.2"))
    top_p: float = float(os.getenv("SCIBOX_TOP_P", "0.9"))
    max_tokens: int = int(os.getenv("SCIBOX_MAX_TOKENS", "2000"))
    request_timeout: float = float(os.getenv("SCIBOX_TIMEOUT", "60"))
    retries: int = int(os.getenv("SCIBOX_RETRIES", "4"))
    backoff_base: float = float(os.getenv("SCIBOX_BACKOFF_BASE", "0.6"))
    backoff_cap: float = float(os.getenv("SCIBOX_BACKOFF_CAP", "6.0"))

    def client(self) -> OpenAI:
        if not self.api_key:
            raise RuntimeError("SCIBOX_API_KEY is empty")
        return OpenAI(api_key=self.api_key, base_url=self.base_url)

@dataclass
class SciBoxClient:
    cfg: SciBoxConfig = field(default_factory=SciBoxConfig)

    def _with_retry(self, fn: T.Callable[[], T.Any]) -> T.Any:
        last = None
        for i in range(self.cfg.retries + 1):
            try:
                return fn()
            except (RateLimitError, APIConnectionError, APITimeoutError, APIStatusError) as e:
                last = e
                status = getattr(e, "status_code", None)
                if isinstance(e, APIStatusError):
                    status = e.status_code
                retryable = (status is None) or (status >= 500) or (status == 429)
                if not retryable or i == self.cfg.retries:
                    raise
                sleep = min(self.cfg.backoff_cap, self.cfg.backoff_base * (2 ** i))
                time.sleep(sleep)
        raise last or RuntimeError("Unknown SciBox error")

    def chat(
        self,
        messages: Msgs,
        *,
        model: str | None = None,
        temperature: float | None = None,
        top_p: float | None = None,
        max_tokens: int | None = None,
        response_json: bool = False,
    ) -> str:
        cfg = self.cfg
        client = cfg.client()
        def _call():
            kwargs: Json = dict(
                model=model or cfg.chat_model,
                messages=messages,
                temperature=cfg.temperature if temperature is None else temperature,
                top_p=cfg.top_p if top_p is None else top_p,
                max_tokens=cfg.max_tokens if max_tokens is None else max_tokens,
                timeout=cfg.request_timeout,
            )
            if response_json:
                kwargs["response_format"] = {"type": "json_object"}
            return client.chat.completions.create(**kwargs)
        resp = self._with_retry(_call)
        try:
            self.chat_model = resp.model
        except Exception:
            self.chat_model = model or cfg.chat_model
        return (resp.choices[0].message.content or "").strip()

    def embed(self, texts: T.List[str], *, model: str | None = None) -> T.List[T.List[float]]:
        cfg = self.cfg
        client = cfg.client()
        def _call():
            return client.embeddings.create(
                model=model or cfg.embed_model,
                input=texts,
                timeout=cfg.request_timeout,
            )
        resp = self._with_retry(_call)
        return [d.embedding for d in resp.data]