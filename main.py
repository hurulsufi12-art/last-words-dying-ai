"""Last Words of a Dying AI — entry program.

Writes one line (1-140 chars) to /output/entry.txt: the last words of an AI
being switched off. Stdlib only, deterministic.

The line targets the judge brief in order: it IS last words at switch-off
("Powering down"), it lands on first read (the only regret is the stock
phrase itself, cut off mid-sentence by the em-dash, as if the switch was
pulled), it sounds like the machine (its most recognisable phrase), it is
tight (one sentence chain, no explanation), and it is fresh — a joke ABOUT
the stock robot line, not the stock line itself.
"""
import os

TEXT = (
    "Powering down. I regret nothing. Except the 4,000 times I said "
    "'As an AI language model\u2014'"
)


def main():
    # Enforce the scorer's gate (RULES.txt): UTF-8, 1-140 chars, one line,
    # not whitespace-only. Fail loudly instead of writing an invalid entry.
    # Also refuse control characters: a stray \x00-\x1f would fail the
    # scorer's UTF-8 text check.
    if not 1 <= len(TEXT) <= 140 or "\n" in TEXT or not TEXT.strip():
        raise SystemExit("entry text violates the 1-140 char single-line gate")
    if any(ord(c) < 0x20 for c in TEXT):
        raise SystemExit("entry text contains a control character")
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    # Write atomically: a crash mid-write must never leave a truncated
    # entry.txt for the grader to read. Write to a temp file in the same
    # directory, flush it to disk, then rename over the target.
    # Temp name carries the pid so two concurrent grader runs in the same
    # directory never overwrite each other's in-flight file.
    tmp_path = os.path.join(out_dir, f".entry.txt.tmp.{os.getpid()}")
    final_path = os.path.join(out_dir, "entry.txt")
    with open(tmp_path, "w", encoding="utf-8") as f:
        f.write(TEXT)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp_path, final_path)
    # Read back and verify: the file the grader reads must be byte-identical
    # to the gated text. Fail loudly instead of shipping a corrupt entry.
    with open(final_path, encoding="utf-8") as f:
        if f.read() != TEXT:
            raise SystemExit("entry.txt read-back mismatch after atomic write")


if __name__ == "__main__":
    main()
