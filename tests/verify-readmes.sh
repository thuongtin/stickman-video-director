#!/usr/bin/env bash
set -euo pipefail

readme_root=$(git rev-parse --show-toplevel)
default_readmes=(
  README.md
  README.en.md
  README.vi.md
  README.ja.md
  README.ko.md
  README.pt-BR.md
)
hero_assets=(
  docs/lead-character/motion.gif
  docs/style-previews/dong-ho.gif
  docs/style-previews/chu-tieu.gif
  docs/style-previews/tech-illustration.gif
)
section_markers=(
  '<!-- readme:hero -->'
  '<!-- readme:demos -->'
  '<!-- readme:advantages -->'
  '<!-- readme:platforms -->'
  '<!-- readme:workflow -->'
  '<!-- readme:output -->'
  '<!-- readme:install -->'
  '<!-- readme:reliability -->'
  '<!-- readme:contribute -->'
)
shared_tokens=(
  'README.en.md'
  'README.vi.md'
  'fork-additions'
  'README.ja.md'
  'README.ko.md'
  'README.pt-BR.md'
  'docs/lead-character/motion.gif'
  'docs/style-previews/dong-ho.gif'
  'docs/style-previews/chu-tieu.gif'
  'docs/style-previews/tech-illustration.gif'
  'YouTube Shorts'
  'TikTok'
  'Instagram Reels'
  'segment spec'
  '16:9'
  '9:16'
  'MIT'
)

if (( $# > 0 )); then
  readmes=("$@")
else
  readmes=("${default_readmes[@]}")
fi

for asset in "${hero_assets[@]}"; do
  [[ -f "$readme_root/$asset" ]] || {
    printf 'missing hero asset: %s\n' "$asset" >&2
    exit 1
  }
done

for readme in "${readmes[@]}"; do
  readme_path="$readme_root/$readme"
  [[ -f "$readme_path" ]] || {
    printf 'missing README: %s\n' "$readme" >&2
    exit 1
  }

  for marker in "${section_markers[@]}"; do
    rg -Fq "$marker" "$readme_path" || {
      printf '%s missing section marker: %s\n' "$readme" "$marker" >&2
      exit 1
    }
  done

  for token in "${shared_tokens[@]}"; do
    rg -Fq "$token" "$readme_path" || {
      printf '%s missing shared token: %s\n' "$readme" "$token" >&2
      exit 1
    }
  done

  for token in 'id="quick-start"' 'id="style-gallery"' 'id="recent-updates"'; do
    rg -Fq "$token" "$readme_path" || {
      printf '%s missing synchronized content: %s\n' "$readme" "$token" >&2
      exit 1
    }
  done
  if rg -ni 'monixin888|2109651037850325112' "$readme_path"; then
    printf '%s contains removed community attribution\n' "$readme" >&2
    exit 1
  fi
  # The repo builds videos as motion graphics only; no AI video generator is named.
  if rg -ni 'flow\.google|omni flash|gemini omni|seedance|higgsfield|\bveo\b|assets/readme/previews' "$readme_path"; then
    printf '%s mentions an AI video generator or the removed demo clips\n' "$readme" >&2
    exit 1
  fi
  if rg -n 'href="assets/readme/[^" ]+\.mp4"|git clone|cp -R skills/|\$skill-installer|\$directing-stickman-videos' "$readme_path"; then
    printf '%s contains obsolete preview or installation instructions\n' "$readme" >&2
    exit 1
  fi
  if [[ "$readme" == README.md || "$readme" == README.vi.md ]]; then
    for token in 'Phong cách 4: Chuyện đời thường ấm áp' 'docs/lead-character/sheet.png' '“Con người có công việc đầu tiên như thế nào?” | Khổ ngang 16:9'; do
      rg -Fq "$token" "$readme_path" || {
        printf '%s missing Vietnamese homepage token: %s\n' "$readme" "$token" >&2
        exit 1
      }
    done
  fi
  forbidden_identity='eva''2050|240669''650|/Users/''eva'
  forbidden_claims='guaranteed ''viral|guaranteed ''views'
  if rg -n "${forbidden_identity}|${forbidden_claims}" "$readme_path"; then
    printf '%s contains forbidden identity or unsupported claim\n' "$readme" >&2
    exit 1
  fi
done

cmp -s "$readme_root/README.md" "$readme_root/README.vi.md" || {
  printf 'Default homepage must match the Vietnamese README.\n' >&2
  exit 1
}
rg -Fq '[**Tiếng Việt**](README.vi.md) · [English](README.en.md)' "$readme_root/README.md" || {
  printf 'Default homepage missing Vietnamese/English language navigation.\n' >&2
  exit 1
}
rg -Fq '# Motion-Graphics Stickman Animation Style Library' "$readme_root/README.en.md" || {
  printf 'English README must remain available.\n' >&2
  exit 1
}

printf 'README contract passed for %s file(s).\n' "${#readmes[@]}"
