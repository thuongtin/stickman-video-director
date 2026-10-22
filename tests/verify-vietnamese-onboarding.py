#!/usr/bin/env python3
"""Check the Vietnamese default homepage, its fork section, section layout, and preview budgets."""
from pathlib import Path
import re
import struct

root = Path(__file__).resolve().parents[1]
vi = (root / "README.md").read_text()
assert vi == (root / "README.vi.md").read_text()
assert not (root / "README.zh-CN.md").exists(), "The Chinese README was replaced by the Vietnamese one"
assert "# Thư viện phong cách hoạt hình người que bằng AI" in vi
for heading in ("## Chọn phong cách", "## Bản fork này thêm gì", "## Skill làm được gì", "## Bắt đầu",
                "## Vài mẹo thực tế", "## Cập nhật mới", "## Nên thêm gì tiếp theo?", "## Star History"):
    assert heading in vi, heading
install = vi.split("### 1. Cài Skill", 1)[1].split("<!-- readme:workflow -->", 1)[0]
assert "Cài Skill này giúp tôi:\nhttps://github.com/kaomei/stickman-video-director" in install
assert len(install.strip()) < 130, "Keep the installation entry short"
guided_demo = vi.split("### 3. Làm theo hướng dẫn và duyệt kế hoạch", 1)[1].split("### 4.", 1)[0]
storyboard_rows = re.findall(r"^\| \*\*(?:0–10|10–20|20–30)s: .*$", guided_demo, re.MULTILINE)
assert len(storyboard_rows) == 3 and all(row.count("|") == 4 for row in storyboard_rows)
approved_voiceover = (
    "Ten thousand years ago, one man finally solved all his problems. He shut them outside.",
    "Then someone offered him food… in exchange for a small favor. Congratulations. Employment was invented.",
    "The reward got smaller. The workload got bigger. And somehow… they called that progress.",
)
for row, voiceover in zip(storyboard_rows, approved_voiceover):
    assert voiceover in row, "Preserve the approved sample narration verbatim"

# The fork section lists every experimental style in the catalog and how to run the checks.
catalog = (root / "skills/directing-stickman-videos/references/style-catalog.md").read_text()
slugs = re.findall(r"^\| `([a-z0-9-]+)` \|", catalog.split("### Experimental styles", 1)[1], re.MULTILINE)
assert len(slugs) == 24
for lang in ("vi", "en"):
    text = (root / f"README.{lang}.md").read_text()
    fork = text.split('<a id="fork-additions"></a>', 1)[1].split("<!-- readme:advantages -->", 1)[0]
    gallery = text.split('<a id="experimental-styles"></a>', 1)[1].split('<a id="fork-additions"></a>', 1)[0]
    assert text.index('<a id="experimental-styles"></a>') < text.index("<!-- readme:advantages -->"), "Styles sit in the style section"
    for slug in slugs:
        assert f"| `{slug}` |" in fork, (lang, slug)
        assert f'src="docs/style-previews/{slug}.gif"' in gallery and f"<code>{slug}</code>" in gallery, (lang, slug)
        assert f'href="docs/style-previews/{slug}.jpg"' in gallery, (lang, slug, "link the cast picture")
        preview = root / "docs/style-previews" / f"{slug}.jpg"
        assert preview.exists() and preview.stat().st_size < 60_000, (slug, "keep previews small")
        # Motion previews follow upstream's GIF demos: 400x225, a few seconds, rendered from the style's own rigs.
        motion = root / "docs/style-previews" / f"{slug}.gif"
        data = motion.read_bytes()
        assert data[:6] in (b"GIF87a", b"GIF89a") and len(data) < 2_500_000, (slug, "motion GIF missing or too large")
        assert int.from_bytes(data[6:8], "little") == 400 and int.from_bytes(data[8:10], "little") == 225, (slug, "400x225")
    for command in ("tools/posture_gate/hand_ledger.py", "tools/package_lint/package_lint.py",
                    "tools/posture_gate/posture_gate.py check", "tools/risk_sheet/risk_sheet.py", "references/storyboard-template.md"):
        assert command in fork, (lang, command)
    for stale in ("Opening hook:", "opening-hook.md", "flow-tested"):
        assert stale not in text, (lang, stale)
assert vi.count('<div align="center">') == vi.count("</div>")

for link in re.findall(r"\]\(([^)]+)\)", vi):
    if "://" not in link and not link.startswith("#"):
        assert (root / link.split("#")[0]).exists(), link

previews = sorted(set(re.findall(r'src="(assets/readme/previews/[^" ]+\.gif)"', vi)))
assert len(previews) == 8
old_bytes = new_bytes = 0
for preview in previews:
    optimized = root / preview
    original = root / "assets/readme" / optimized.name
    assert optimized.exists()
    header = optimized.read_bytes()[:10]
    assert header[:6] in (b"GIF87a", b"GIF89a")
    assert struct.unpack("<HH", header[6:10]) == (400, 225)
    assert optimized.stat().st_size < original.stat().st_size
    old_bytes += original.stat().st_size
    new_bytes += optimized.stat().st_size
assert new_bytes < old_bytes * 0.6, "Preview total should shrink by at least 40%"

for lang in ("en", "ja", "ko", "pt-BR"):
    text = (root / f"README.{lang}.md").read_text()
    assert "assets/readme/previews/" in text, "Localized pages use the same lightweight previews"

print(f"Vietnamese onboarding passed; previews {old_bytes:,} -> {new_bytes:,} bytes ({1-new_bytes/old_bytes:.1%} smaller).")
