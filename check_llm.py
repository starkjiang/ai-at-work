"""Verify that the demos will call a real model, not mock mode.

    python check_llm.py

Checks, in order: which provider .env selects, that the key is present, that the SDK is
installed, then makes one tiny real API call and prints the model id and token count the
API itself returned. Token counts come from the provider's servers, so if you see them the
call was real. Exit code 0 = ready, 1 = not ready.
"""
from __future__ import annotations

import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
ENV = ROOT / ".env"
OK, BAD, WARN = "  [ok] ", "  [!!] ", "  [..] "


def mask(key: str) -> str:
    return key[:7] + "..." + key[-4:] if len(key) > 12 else "(too short to be a real key)"


def fail(msg: str, fix: str) -> None:
    print(BAD + msg)
    print("       fix: " + fix)
    sys.exit(1)


def main() -> None:
    print("\nAI at Work — model connection check\n")

    # 1. .env
    if not ENV.exists():
        fail(f"No .env at {ENV}", "cp .env.example .env   (from the repo root), then edit it")
    load_dotenv(ENV, override=True)
    print(OK + f".env found at {ENV}")

    provider = os.getenv("LLM_PROVIDER", "mock").strip().lower()
    model = os.getenv("LLM_MODEL", "").strip()
    if provider == "mock":
        fail("LLM_PROVIDER=mock — the demos will replay canned answers, not call a model",
             "set LLM_PROVIDER=openai (or anthropic / azure) in .env")
    print(OK + f"LLM_PROVIDER={provider}")

    if provider == "openai":
        key = os.getenv("OPENAI_API_KEY", "").strip()
        if not key:
            fail("OPENAI_API_KEY is empty", "paste your key from platform.openai.com → API keys into .env")
        if not key.startswith("sk-"):
            print(WARN + "OPENAI_API_KEY does not start with 'sk-' — double-check you pasted the API key, not an org/project id")
        print(OK + f"OPENAI_API_KEY={mask(key)}")
        model = model or "gpt-4o"
        if not os.getenv("LLM_MODEL"):
            print(WARN + f"LLM_MODEL is empty; using the default '{model}'. Set it explicitly to a model your account has.")
        try:
            import openai
        except ImportError:
            fail("openai package not installed", "pip install openai")
        print(OK + f"openai SDK {openai.__version__} installed")

        print(WARN + f"calling {model} ...")
        client = openai.OpenAI()
        t0 = time.time()
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": "Reply with exactly: CONNECTED"}],
                max_tokens=10,
            )
        except openai.AuthenticationError:
            fail("the API rejected the key (401)", "create a new key; make sure it isn't revoked or for a different project")
        except openai.NotFoundError:
            try:
                ids = sorted(m.id for m in client.models.list() if m.id.startswith(("gpt", "o")))
                hint = "models your key can use: " + ", ".join(ids[:15])
            except Exception:
                hint = "check the model name on platform.openai.com/docs/models"
            fail(f"model '{model}' not found or not available to this key", f"set LLM_MODEL in .env. {hint}")
        except openai.RateLimitError as e:
            fail(f"rate limit / quota error: {e}",
                 "the account likely has no credit. Add billing at platform.openai.com → Billing (ChatGPT Plus does NOT include API credit)")
        except openai.APIConnectionError:
            fail("could not reach api.openai.com",
                 "a firewall or proxy is blocking it — common on corporate/university networks. Try another network, or set HTTPS_PROXY")
        except openai.BadRequestError as e:
            fail(f"bad request: {e}", "the model may need different parameters; try another LLM_MODEL")
        dt = time.time() - t0
        text = (resp.choices[0].message.content or "").strip()
        u = resp.usage
        print(OK + f"reply: {text!r}")
        print(OK + f"served by model id: {resp.model}")
        print(OK + f"tokens billed: {u.prompt_tokens} in / {u.completion_tokens} out   ({dt:.1f}s)")

    elif provider == "anthropic":
        key = os.getenv("ANTHROPIC_API_KEY", "").strip()
        if not key:
            fail("ANTHROPIC_API_KEY is empty", "paste your key from console.anthropic.com into .env")
        print(OK + f"ANTHROPIC_API_KEY={mask(key)}")
        try:
            import anthropic
        except ImportError:
            fail("anthropic package not installed", "pip install anthropic")
        model = model or "claude-sonnet-4-5"
        print(WARN + f"calling {model} ...")
        try:
            msg = anthropic.Anthropic().messages.create(
                model=model, max_tokens=10,
                messages=[{"role": "user", "content": "Reply with exactly: CONNECTED"}])
        except anthropic.APIError as e:
            fail(f"API error: {e}", "check the key, billing, model name (LLM_MODEL) and network")
        print(OK + f"reply: {msg.content[0].text.strip()!r}")
        print(OK + f"served by model id: {msg.model}")
        print(OK + f"tokens billed: {msg.usage.input_tokens} in / {msg.usage.output_tokens} out")

    elif provider == "azure":
        need = ["AZURE_OPENAI_API_KEY", "AZURE_OPENAI_ENDPOINT", "AZURE_OPENAI_DEPLOYMENT"]
        missing = [k for k in need if not os.getenv(k, "").strip()]
        if missing:
            fail(f"missing {', '.join(missing)}", "get these from your Azure OpenAI resource → Keys and Endpoint, and Deployments")
        try:
            import openai
        except ImportError:
            fail("openai package not installed", "pip install openai")
        client = openai.AzureOpenAI(api_key=os.environ["AZURE_OPENAI_API_KEY"],
                                    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
                                    api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21"))
        try:
            resp = client.chat.completions.create(model=os.environ["AZURE_OPENAI_DEPLOYMENT"], max_tokens=10,
                                                  messages=[{"role": "user", "content": "Reply with exactly: CONNECTED"}])
        except openai.APIError as e:
            fail(f"API error: {e}", "check endpoint URL, deployment name (not the model name), key, and API version")
        print(OK + f"reply: {resp.choices[0].message.content.strip()!r}")
        print(OK + f"served by model id: {resp.model}")
    else:
        fail(f"unknown LLM_PROVIDER={provider!r}", "use mock, openai, anthropic, or azure")

    print("\nReady. The demos will call this model. For per-call proof during the session, run with")
    print("LLM_DEBUG=1 in .env: each call prints a [llm] line with the model and token counts.\n")


if __name__ == "__main__":
    main()
