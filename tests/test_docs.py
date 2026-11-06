import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

_AUTOMODULE_RE = re.compile(r"^\.\.\s+automodule::\s+(\S+)\s*$", re.MULTILINE)


class TestEveryModuleHasExactlyOneAutomodulePage(unittest.TestCase):
    def test_every_module_is_documented_exactly_once(self):
        module_names = sorted(
            f"document2md.{path.stem}"
            for path in (ROOT / "document2md").glob("*.py")
            if path.stem != "__init__"
        )
        self.assertTrue(module_names, "expected at least one document2md/*.py module")

        rst_text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (ROOT / "docs" / "source").rglob("*.rst")
        )
        documented = _AUTOMODULE_RE.findall(rst_text)

        for name in module_names:
            occurrences = documented.count(name)
            self.assertEqual(
                occurrences, 1,
                f"{name} is named by {occurrences} automodule directives under "
                "docs/source/, expected exactly 1",
            )


class TestNoDeadDocumentationUrls(unittest.TestCase):
    """The developer docs live on GitHub Pages under /dev/, not on Read the Docs.

    The Read the Docs project was never imported and the site moved off
    INGEOTEC's Pages host, so these URLs answer 404; no tracked file may point
    at them again.
    """

    # Built from fragments so this file does not flag itself.
    DEAD = (
        "document2md." + "readthedocs.io",
        "readthedocs.org/projects/" + "document2md",
        "ingeotec." + "github.io",
    )

    def test_no_tracked_file_mentions_a_dead_url(self):
        try:
            listing = subprocess.run(
                ["git", "ls-files", "-z"],
                cwd=ROOT, capture_output=True, check=True,
            ).stdout
        except (OSError, subprocess.CalledProcessError):
            self.skipTest("git is not available or ROOT is not a git checkout")

        offenders = {}
        for name in filter(None, listing.decode("utf-8").split("\0")):
            path = ROOT / name
            if not path.is_file():
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            found = [url for url in self.DEAD if url in text]
            if found:
                offenders[name] = found

        self.assertFalse(
            offenders,
            "tracked files point at dead documentation URLs: "
            + "; ".join(f"{n}: {', '.join(u)}" for n, u in sorted(offenders.items())),
        )


if __name__ == "__main__":
    unittest.main()
