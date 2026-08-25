from aimem.redact import redact_sensitive_text


def test_redact_token_and_password() -> None:
    text = "token sk-abcdefghijklmnopqrstuvwxyz password=hunter2"
    out = redact_sensitive_text(text)
    assert "sk-abcdefghijklmnopqrstuvwxyz" not in out
    assert "hunter2" not in out
    assert "[REDACTED_TOKEN]" in out
    assert "[REDACTED]" in out


def test_redact_leaves_ordinary_text() -> None:
    assert redact_sensitive_text("prefer short Chinese answers") == "prefer short Chinese answers"
