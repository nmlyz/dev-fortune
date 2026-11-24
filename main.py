#!/usr/bin/env python3
"""Write one fortune-cookie line for developers to /output/entry.txt.

The line is a single original sentence of at most 120 characters: a
short, balanced piece of fortune-cookie wisdom aimed at a software
developer, stating a fate about legacy code with a quiet double
meaning that rewards a second read.

The chosen line:

    The function you are afraid to touch has been afraid of you
    for years.

Why this line, against the brief's five weights in order:

1. It is fortune-cookie wisdom, not a slogan, a punchline, or
   generic advice: it states a fate, it does not tell the reader
   what to do and it does not end on a joke.
2. It reads like a real fortune cookie: one short balanced sentence
   that lands in a single breath, seventy characters long.
3. It says something true about a developer's day: every senior
   engineer knows a function nobody dares to touch, and the fear
   around it is real.
4. It turns that truth in a way the reader has not heard before:
   the feared thing is afraid too. The usual version of this
   thought blames the past author; this one reverses the fear.
5. It leaves a quiet twist that rewards a second read: on the
   first read the function is the object of fear, on the second
   read the fear is mutual, and the reader is the one being
   watched by the code they avoid.

The program is deterministic: it always writes the same bytes.
"""

import os

# The winning line, chosen from 36 candidates by a mock pairwise
# tournament judged on the competition brief (see
# dev-fortune-candidates.md in the build notes). Seventy characters,
# one sentence, one line.
LINE = (
    "The function you are afraid to touch "
    "has been afraid of you for years."
)

# The competition gate: /output/entry.txt must be UTF-8 text of
# 1 to 120 characters, not only white space, a single line.
MAX_LENGTH = 120


def validate(text):
    """Check the entry against the gate before writing it."""
    if not isinstance(text, str):
        raise TypeError("entry must be text")
    stripped = text.strip()
    if not 1 <= len(stripped) <= MAX_LENGTH:
        raise ValueError(
            "entry must be 1 to %d characters, got %d"
            % (MAX_LENGTH, len(stripped))
        )
    if "\n" in stripped or "\r" in stripped:
        raise ValueError("entry must be a single line")
    if not stripped:
        raise ValueError("entry must not be only white space")
    if stripped.count(".") != 1 or not stripped.endswith("."):
        raise ValueError("entry must be one sentence ending in a period")
    return stripped


def write_entry(out_dir):
    """Write the validated line to entry.txt, readable by everyone.

    The output directory itself is never chmodded, only the file it
    holds: the grader collects the outputs as another user, so the
    file must be mode 0644. The directory is created when missing;
    OUTPUT_DIR overrides the default /output for local runs.
    """
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    text = validate(LINE)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text + "\n")
    # Make the file readable by every user (the grader runs as
    # another user); never chmod the directory itself.
    os.chmod(path, 0o644)
    return path


def main():
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    path = write_entry(out_dir)
    print("wrote %s (%d characters)" % (path, len(validate(LINE))))


if __name__ == "__main__":
    # A permissive umask so files the program opens are readable;
    # write_entry still chmods entry.txt explicitly, which covers
    # files created through paths that ignore the umask.
    os.umask(0o022)
    main()
