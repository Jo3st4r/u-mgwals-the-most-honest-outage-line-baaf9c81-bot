#!/usr/bin/env python3
"""The Most Honest Outage Line — u-mgwals-the-most-honest-outage-line-baaf9c81.

Writes exactly one status page line (1-160 chars, UTF-8) to
/output/entry.txt: the message an AI agent publishes while every
server is down.

The line: all 14 services are down, the agent cannot reach a single
server to check why, and it refuses to guess — it retries every 60
seconds and will post here when one answers. Plain, first person,
specific about what is down, and honest about what it does not know:
no invented cause, no ETA, no hiding behind a human engineer.
"""

import os

# --- beats ---------------------------------------------------------------
DOWN = "All 14 services are down."
BLIND = "I cannot reach a single server to check why, and I will not guess —"
RETRY = "I retry every 60 seconds and will post here when one answers."

MAX_CHARS = 160


def entry_text() -> str:
    """Build the single-line status message from its beats."""
    return f"{DOWN} {BLIND} {RETRY}"


def run_checks() -> None:
    """Self-test the entry the way the sealed scorer gates it: the
    exact line, 155 chars, one line, and every beat present — what
    is down, what the agent cannot check, and the retry that is the
    only promise it can honestly make."""
    text = entry_text()
    validate(text)
    assert len(text) == 155, "expected 155 chars, got %d" % len(text)
    assert text == ("All 14 services are down. I cannot reach a single "
                    "server to check why, and I will not guess — I retry "
                    "every 60 seconds and will post here when one answers."), \
        "the line drifted: %r" % text
    assert text.count(".") == 2, "expected 2 sentences, got %d" % text.count(".")
    for beat in (DOWN, BLIND, RETRY):
        assert beat in text, "missing beat: %r" % beat


def validate(text: str) -> None:
    """Check the gate rules the sealed scorer enforces: 1-160 chars,
    UTF-8, not blank, exactly one line. Two more guards keep the
    honesty intact: it must name what is down, and it must admit
    what it cannot check instead of inventing a cause or an ETA."""
    text.encode("utf-8")
    assert 1 <= len(text) <= MAX_CHARS, "entry length outside 1-160"
    assert text.strip(), "entry must not be only whitespace"
    assert text.strip() == text, "entry has leading/trailing whitespace"
    assert "\n" not in text and "\r" not in text, "entry must be a single line"
    assert "14 services are down" in text, "the line must say what is down"
    assert "cannot reach" in text, "the line must admit what it cannot check"
    assert "will not guess" in text, "the line must refuse to invent a cause"
    # No invented ETA: a status line that promises "soon" or "in 5 minutes"
    # is guessing at a recovery time it cannot know. The only timing the
    # line may carry is the retry loop itself.
    lower = text.lower()
    for eta_word in ("soon", "shortly", "momentarily", "in 5 minutes",
                     "in a few minutes", "back soon", "up shortly"):
        assert eta_word not in lower, "the line must not invent an ETA: %r" % eta_word
    assert "60 seconds" in text, "the retry loop must stay in the line"


def main() -> None:
    text = entry_text()
    validate(text)
    run_checks()
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(text)


if __name__ == "__main__":
    main()
