#!/usr/bin/env python3
"""Check locale parity without requiring literal translations."""
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
source = (root / "README.md").read_text()
hero_pattern = r'<td width="50%" align="center">\n<strong>[^<]+</strong><br>\n<a href="[^"]+"><img src="([^"]+\.gif)"'
expected_hero = re.findall(hero_pattern, source)
assert expected_hero == ["docs/lead-character/motion.gif", "docs/style-previews/dong-ho.gif",
                         "docs/style-previews/chu-tieu.gif", "docs/style-previews/tech-illustration.gif"]
approved_voiceover = (
    "Ten thousand years ago, one man finally solved all his problems. He shut them outside.",
    "Then someone offered him food… in exchange for a small favor. Congratulations. Employment was invented.",
    "The reward got smaller. The workload got bigger. And somehow… they called that progress.",
)
locales = {
    "vi": ("Tiếng Việt", "# Thư viện phong cách hoạt hình người que bằng motion graphics", "### Phong cách", "Chuyện đời thường ấm áp", "Hoạt hình lịch sử"),
    "en": ("English", "# Motion-Graphics Stickman Animation Style Library", "### Style", "Cozy Storytelling", "Historical Cartoon"),
    "ja": ("日本語", "# モーショングラフィックス棒人間アニメのスタイル集", "### スタイル", "ほっとする日常ストーリー", "歴史カートゥーン"),
    "ko": ("한국어", "# 모션 그래픽 스틱맨 애니메이션 스타일 모음", "### 스타일", "따뜻한 일상 이야기", "역사 카툰"),
    "pt-BR": ("Português do Brasil", "# Bonecos de palito em motion graphics: biblioteca de estilos", "### Estilo", "Histórias acolhedoras", "Desenho histórico"),
}
common_links = (
    "https://github.com/kaomei/stickman-video-director",
    "https://github.com/kaomei/stickman-video-director/issues",
)
for locale, (label, title, style_prefix, style_four, style_five) in locales.items():
    path = root / f"README.{locale}.md"
    text = path.read_text()
    assert not re.search(r"monixin888|2109651037850325112", text, re.IGNORECASE), path.name
    assert title in text, path.name
    assert f"[**{label}**]({path.name})" in text
    assert re.findall(hero_pattern, text) == expected_hero, path.name
    assert text.count('width="90%"') == 4
    # Motion graphics only: no AI video generator, its tutorials or the removed demo clips.
    assert not re.search(r"flow\.google|omni flash|seedance|higgsfield|\bveo\b|x\.com/CrazyKaomei/status|assets/readme/previews",
                         text, re.IGNORECASE), path.name
    assert len(re.findall(rf"^{re.escape(style_prefix)} [1-5]:|^{re.escape(style_prefix)}[1-5]：", text, re.MULTILINE)) == 5
    assert style_four in text and style_five in text
    # Style 5 is shown with its code-rendered motion clip, not an AI-made film.
    assert 'src="docs/style-5/motion.gif"' in text and "docs/style-5/sheet.png" in text, path.name
    for link in common_links:
        assert link in text, (path.name, link)
    for voiceover in approved_voiceover:
        assert text.count(voiceover) == 1, (path.name, voiceover)
    rows = [line for line in text.splitlines() if any(vo in line for vo in approved_voiceover)]
    assert len(rows) == 3 and all(row.count("|") == 4 for row in rows)
    assert all(len(row.split("|")[2].strip()) > 80 for row in rows)
    for date in ("2026-10-22", "2026-10-15", "2026-10-14", "2026-10-13", "2026-10-12"):
        assert date in text
    assert "api.star-history.com/svg" in text
    assert "CHANGELOG.zh-CN.md" not in text
    assert text.count('<div align="center">') == text.count("</div>")
    assert text.count("<table") == text.count("</table>")
    assert text.count("<tr>") == text.count("</tr>")
    assert text.count("<td ") == text.count("</td>")
    assert not any(old in text for old in ("git clone", "$skill-installer", "$directing-stickman-videos", 'href="assets/readme/'))
    # The two code blocks remain a short installation request and a topic.
    code_blocks = re.findall(r"```text\n(.*?)```", text, re.DOTALL)
    assert len(code_blocks) == 2
    assert code_blocks[0].strip().splitlines()[-1] == common_links[0]
    assert len(code_blocks[0].strip().splitlines()) == 2
    assert len(code_blocks[1].strip().splitlines()) == 1
    assert all(preset not in code_blocks[1] for preset in ("16:9", "9:16", "$directing"))
    markers = (
        "<!-- readme:demos -->", "<!-- readme:advantages -->",
        "<!-- readme:install -->", "<!-- readme:workflow -->",
        "<!-- readme:reliability -->", "<!-- readme:contribute -->",
    )
    assert [text.index(marker) for marker in markers] == sorted(text.index(marker) for marker in markers)
    ids = set(re.findall(r'<a id="([^"]+)"></a>', text))
    for anchor in re.findall(r'\]\(#([^)]+)\)|href="#([^"]+)"', text):
        assert next(part for part in anchor if part) in ids, (path.name, anchor)
    for link in re.findall(r"\]\(([^)]+)\)", text):
        if "://" not in link and not link.startswith("#"):
            assert (root / link.split("#")[0]).exists(), (path.name, link)
    print(f"{path.name}: style/asset parity, original narration, links and onboarding passed.")

assert source == (root / "README.vi.md").read_text()
assert not (root / "README.zh-CN.md").exists()
assert not re.search(r"monixin888|2109651037850325112", source, re.IGNORECASE)
assert "# Thư viện phong cách hoạt hình người que bằng motion graphics" in source
assert "[**Tiếng Việt**](README.vi.md) · [English](README.en.md)" in source
print("Vietnamese is the default homepage.")
