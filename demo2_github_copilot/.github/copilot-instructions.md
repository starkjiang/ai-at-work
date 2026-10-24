# Copilot instructions for this repository

You are assisting engineers at <ORGANIZATION>. Follow these rules on every request.

## Code standards
- Python 3.11+, standard library only unless a dependency already exists in `requirements.txt`.
- Type hints on all public functions. Google-style docstrings with Args, Returns, Raises.
- Tests use `pytest`; one behavior per test; test names describe the behavior (`test_window_larger_than_data_returns_plain_mean`).
- Prefer small, pure functions. Do not introduce global state.

## Security and data
- Never hardcode credentials, hostnames, or file paths to internal systems.
- Treat all CSV input as untrusted: validate types, handle missing values explicitly.
- Do not add network calls or telemetry.

## Intellectual property
- Do not reproduce code from external repositories verbatim. Write implementations from first principles.
- Do not include proprietary algorithms or internal identifiers in examples or comments.

## Workflow
- When asked to fix a bug, first propose a failing test, then the fix.
- When you are unsure of an expected behavior, ask rather than assume — and say what you assumed.
- Summaries of pull requests must list: what changed, why, how it was tested, and any follow-ups.
