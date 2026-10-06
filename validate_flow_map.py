#!/usr/bin/env python3
"""Static validator for standalone interactive flow-map HTML artifacts."""
from pathlib import Path
import argparse
import re
import shutil
import subprocess
import sys
import tempfile


def check(condition, message, failures):
    if condition:
        print(f"PASS  {message}")
    else:
        print(f"FAIL  {message}")
        failures.append(message)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("html", help="Path to standalone HTML file")
    args = parser.parse_args()
    path = Path(args.html)
    failures = []

    check(path.is_file(), "artifact exists", failures)
    if not path.is_file():
        return 1

    text = path.read_text(encoding="utf-8")
    lower = text.lower()
    check("<!doctype html>" in lower, "HTML5 doctype present", failures)
    check("<meta name=\"viewport\"" in lower or "<meta name='viewport'" in lower,
          "viewport metadata present", failures)
    check("<style" in lower and "</style>" in lower, "inline CSS present", failures)
    check("<script" in lower and "</script>" in lower, "inline JavaScript present", failures)

    external = re.findall(r"(?:src|href)\s*=\s*['\"]https?://", text, re.I)
    check(not external, "no external script or stylesheet dependencies", failures)
    check("prefers-reduced-motion" in text, "reduced-motion handling present", failures)
    check("focus-visible" in text, "visible keyboard-focus styling present", failures)
    check("aria-label" in text or "aria-labelledby" in text,
          "accessible naming markers present", failures)

    interaction_markers = ["pointerdown", "wheel", "keydown"]
    check(all(marker in text for marker in interaction_markers),
          "pan, zoom, and keyboard interaction handlers present", failures)

    scripts = re.findall(r"<script(?:\s[^>]*)?>(.*?)</script>", text, re.I | re.S)
    node = shutil.which("node")
    if scripts and node:
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as temp:
            temp.write("\n".join(scripts))
            js_path = temp.name
        result = subprocess.run([node, "--check", js_path], capture_output=True, text=True)
        Path(js_path).unlink(missing_ok=True)
        check(result.returncode == 0, "JavaScript syntax passes Node.js check", failures)
        if result.returncode:
            print(result.stderr.strip())
    else:
        print("SKIP  JavaScript syntax check, Node.js or inline script unavailable")

    if failures:
        print(f"\n{len(failures)} validation failure(s)")
        return 1
    print("\nValidation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
