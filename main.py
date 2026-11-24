"""The Houseplant Out-of-Office — make.fun entry.

Writes the out-of-office auto-reply a houseplant would send to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt).

The entry is one fixed line, 84 characters: a deadpan auto-reply from
a plant ignored since March, telling the sender their email changes
nothing. Short on purpose — on an exact tie the judge ranks the
smaller text first, then the earlier receipt.

Pure standard library only (os). No third-party packages, no network,
no environment secrets: everything the entry runs is in this file.
"""

import os

REPLY = "I am out of the office. I have been ignored since March. Your email changes nothing."

# Gate from RULES.txt: /output/entry.txt must be 1-120 UTF-8 chars.
LIMIT = 120


def problems(text):
    """List every way `text` would fail the competition gate."""
    found = []
    if not isinstance(text, str):
        return ["entry must be text"]
    if not 1 <= len(text) <= LIMIT:
        found.append("entry must be 1-%d characters, got %d"
                     % (LIMIT, len(text)))
    if not text.strip():
        found.append("entry must not be only whitespace")
    if "\n" in text or "\r" in text:
        found.append("entry must be a single line")
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        found.append("entry must be valid UTF-8")
    return found


def main():
    bad = problems(REPLY)
    if bad:
        raise ValueError("; ".join(bad))
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(REPLY)
    # The judge reads the file, not the string in memory, so read it
    # back and confirm the bytes on disk are exactly the reply.
    with open(path, "r", encoding="utf-8", newline="") as f:
        on_disk = f.read()
    if on_disk != REPLY:
        raise ValueError("entry.txt does not match the reply")
    print("wrote %d chars to %s (verified)" % (len(REPLY), path))


if __name__ == "__main__":
    main()
