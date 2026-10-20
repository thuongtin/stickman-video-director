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
demo_assets=(
  assets/readme/light-theme-demo.gif
  assets/readme/light-theme-demo.mp4
  assets/readme/dark-theme-demo.gif
  assets/readme/dark-theme-demo.mp4
  assets/readme/style-2a-demo.gif
  assets/readme/style-2a-demo.mp4
  assets/readme/style-2b-demo.gif
  assets/readme/style-2b-demo.mp4
  assets/readme/style-3-demo.gif
  assets/readme/style-3-demo.mp4
  assets/readme/style-3-community-fire.gif
  assets/readme/style-3-community-fire.mp4
  assets/readme/style-4-cozy-station.gif
  assets/readme/style-4-cozy-station.mp4
  assets/readme/style-4-cozy-cafe.gif
  assets/readme/style-4-cozy-cafe.mp4
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
  'assets/readme/light-theme-demo.gif'
  'assets/readme/dark-theme-demo.gif'
  'assets/readme/style-2a-demo.gif'
  'assets/readme/style-2b-demo.gif'
  'assets/readme/style-3-demo.gif'
  'YouTube Shorts'
  'TikTok'
  'Instagram Reels'
  'Gemini Omni Flash'
  '16:9'
  '9:16'
  'MIT'
)

if (( $# > 0 )); then
  readmes=("$@")
else
  readmes=("${default_readmes[@]}")
fi

for asset in "${demo_assets[@]}"; do
  [[ -f "$readme_root/$asset" ]] || {
    printf 'missing demo asset: %s\n' "$asset" >&2
    exit 1
  }
done

for readme in "${readmes[@]}"; do
  readme_path="$readme_root/$readme"
  preview_dir='assets/readme/previews'
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
    expected_token="$token"
    if [[ "$token" == assets/readme/*.gif ]]; then
      expected_token="$preview_dir/${token##*/}"
    fi
    rg -Fq "$expected_token" "$readme_path" || {
      printf '%s missing shared token: %s\n' "$readme" "$token" >&2
      exit 1
    }
  done

  # All published styles keep two lightweight inline previews in every locale.
  paired_demos=(
    'light-theme-demo dark-theme-demo'
    'style-2a-demo style-2b-demo'
    'style-3-demo style-3-community-fire'
    'style-4-cozy-station style-4-cozy-cafe'
  )
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
  if rg -n 'href="assets/readme/[^" ]+\.mp4"|git clone|cp -R skills/|\$skill-installer|\$directing-stickman-videos' "$readme_path"; then
    printf '%s contains obsolete preview or installation instructions\n' "$readme" >&2
    exit 1
  fi
  if [[ "$readme" == README.md || "$readme" == README.vi.md ]]; then
    for token in 'Phong cách 4: Chuyện đời thường ấm áp' 'assets/readme/previews/style-4-cozy-station.gif' 'assets/readme/previews/style-4-cozy-cafe.gif' 'assets/readme/previews/style-3-community-fire.gif' 'Ví dụ 1: “Con người có công việc đầu tiên như thế nào?”'; do
      rg -Fq "$token" "$readme_path" || {
        printf '%s missing Vietnamese homepage token: %s\n' "$readme" "$token" >&2
        exit 1
      }
    done
  fi
  for pair in "${paired_demos[@]}"; do
    read -r first_demo second_demo <<< "$pair"
    rg -q "src=\"${preview_dir}/${first_demo}\.gif\".*[|].*src=\"${preview_dir}/${second_demo}\.gif\"" "$readme_path" || {
      printf '%s missing paired examples: %s\n' "$readme" "$pair" >&2
      exit 1
    }
  done

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
rg -Fq '# AI Stickman Animation Style Library' "$readme_root/README.en.md" || {
  printf 'English README must remain available.\n' >&2
  exit 1
}

printf 'README contract passed for %s file(s).\n' "${#readmes[@]}"
