"""Build the game's Huiwen Mincho from the preserved source font.

Only characters in shipped text resources are retained. User-entered names
remain displayable through Godot's enabled system-font fallback.
"""

from hashlib import sha256
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont


ROOT = Path(__file__).resolve().parents[3]
SOURCE = Path(__file__).with_name("汇文明朝体-原始.ttf")
OUTPUT = ROOT / "Game/art/ui/fonts/汇文明朝体.ttf"
TEXT_EXTENSIONS = {".gd", ".tscn", ".tres", ".json", ".godot", ".csv", ".txt", ".md"}
SOURCE_SHA256 = "1ea5d0450c0d034c3e4077f2b533d74fbd1bf1f14d938477389338e64d3d8d9c"


def main() -> None:
    if sha256(SOURCE.read_bytes()).hexdigest() != SOURCE_SHA256:
        raise SystemExit("The preserved source font does not match the recorded original")
    characters = {ord(chr(codepoint)) for codepoint in range(32, 127)}
    for path in (ROOT / "Game").rglob("*"):
        if path.is_file() and path.suffix in TEXT_EXTENSIONS and ".godot" not in path.parts:
            characters.update(map(ord, path.read_text("utf-8", errors="ignore")))
    font = TTFont(SOURCE, recalcTimestamp=False)
    cutter = subset.Subsetter()
    cutter.populate(unicodes=characters)
    cutter.subset(font)
    font.save(OUTPUT)
    print(f"FONT_SUBSET glyphs={len(font.getBestCmap())} bytes={OUTPUT.stat().st_size} sha256={sha256(OUTPUT.read_bytes()).hexdigest()}")


if __name__ == "__main__":
    main()
