"""Thin provider abstraction so every demo script calls one function: complete().

Set LLM_PROVIDER in .env (or the environment) to mock | anthropic | openai | azure.
Mock mode never touches the network — it replays canned outputs from
prompts/mock_responses.yaml keyed by a `mock_key`, or echoes a placeholder.
"""
from __future__ import annotations

import os
from pathlib import Path

import yaml
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

HERE = Path(__file__).resolve().parent
PROVIDER = os.getenv("LLM_PROVIDER", "mock").lower()
MODEL = os.getenv("LLM_MODEL") or None


def _mock(prompt: str, system: str | None, mock_key: str | None) -> str:
    responses = yaml.safe_load((HERE / "prompts" / "mock_responses.yaml").read_text())
    if mock_key and mock_key in responses:
        return responses[mock_key].rstrip()
    return (
        "[mock mode] No canned response for this prompt. Set LLM_PROVIDER in .env to "
        "call a real model.\n\n--- prompt received ---\n" + prompt[:600]
    )


def _anthropic(prompt: str, system: str | None) -> str:
    import anthropic  # pip install anthropic

    client = anthropic.Anthropic()
    msg = client.messages.create(
        model=MODEL or "claude-sonnet-4-5",
        max_tokens=1500,
        system=system or "You are a helpful assistant.",
        messages=[{"role": "user", "content": prompt}],
    )
    return "".join(block.text for block in msg.content if block.type == "text")


def _openai(prompt: str, system: str | None) -> str:
    from openai import OpenAI  # pip install openai

    client = OpenAI()
    resp = client.chat.completions.create(
        model=MODEL or "gpt-4o",
        messages=[
            {"role": "system", "content": system or "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
    )
    return resp.choices[0].message.content or ""


def _azure(prompt: str, system: str | None) -> str:
    from openai import AzureOpenAI  # pip install openai

    client = AzureOpenAI(
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21"),
    )
    resp = client.chat.completions.create(
        model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
        messages=[
            {"role": "system", "content": system or "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
    )
    return resp.choices[0].message.content or ""


def complete(prompt: str, system: str | None = None, mock_key: str | None = None) -> str:
    """Send one prompt to the configured provider and return the text reply."""
    if PROVIDER == "mock":
        return _mock(prompt, system, mock_key)
    if PROVIDER == "anthropic":
        return _anthropic(prompt, system)
    if PROVIDER == "openai":
        return _openai(prompt, system)
    if PROVIDER == "azure":
        return _azure(prompt, system)
    raise ValueError(f"Unknown LLM_PROVIDER={PROVIDER!r}; use mock, anthropic, openai, or azure")
