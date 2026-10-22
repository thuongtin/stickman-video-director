<!-- readme:hero -->

<div align="center">

[Tiếng Việt](README.vi.md) · [English](README.en.md) · [日本語](README.ja.md) · [**한국어**](README.ko.md) · [Português do Brasil](README.pt-BR.md)

# 모션 그래픽 스틱맨 애니메이션 스타일 모음

**아이디어 하나를, 일관된 그림체의 완성도 있는 영상으로.**

[![GitHub Stars](https://img.shields.io/github/stars/kaomei/stickman-video-director?style=flat-square)](https://github.com/kaomei/stickman-video-director/stargazers)
![MIT License](https://img.shields.io/badge/License-MIT-16a34a?style=flat-square)

</div>

<div align="center">

온라인에서 인기 있는 스틱맨 스타일을 하나씩 직접 테스트하고, 제작 방법을 무료로 공개하고 있습니다. Skill을 설치한 뒤 어시스턴트에게 주제만 알려 주세요. 대본, 스토리보드, 모션 그래픽으로 만들 구간별 사양서(segment spec), 내레이션과 효과음까지 한 번에 준비할 수 있습니다.

<strong>다음 스틱맨 영상은 여기서 그림체부터 골라 보세요.</strong> **YouTube 지식·정보 영상, TikTok, 직장 이야기와 동기부여 콘텐츠, 교육 영상, 일상의 감정을 담은 짧은 이야기**에 활용할 수 있습니다.

</div>

<table width="100%">
<tr>
<td width="50%" align="center">
<strong>스타일 2 주인공</strong><br>
<a href="#style-gallery"><img src="docs/lead-character/motion.gif" alt="스포츠머리에 안경을 쓴 스틱맨 남이 걸어 들어와 손을 흔든다" width="90%"></a>
</td>
<td width="50%" align="center">
<strong>동호 목판화</strong><br>
<a href="README.en.md#experimental-styles"><img src="docs/style-previews/dong-ho.gif" alt="동호 목판화 스타일의 모션 클립" width="90%"></a>
</td>
</tr>
<tr>
<td width="50%" align="center">
<strong>동자승</strong><br>
<a href="README.en.md#experimental-styles"><img src="docs/style-previews/chu-tieu.gif" alt="동자승 스타일의 모션 클립" width="90%"></a>
</td>
<td width="50%" align="center">
<strong>부드러운 테크 일러스트</strong><br>
<a href="README.en.md#experimental-styles"><img src="docs/style-previews/tech-illustration.gif" alt="부드러운 테크 일러스트 스타일의 모션 클립" width="90%"></a>
</td>
</tr>
</table>

<div align="center">

**4가지 스타일 · 6가지 비주얼 옵션 · 실제 제작 예시 · 무료 오픈소스**

⭐ **Star로 저장해 두세요. 다음 영상을 만들 때 빈 페이지에서 시작하지 않아도 됩니다.**

[시작하기](#quick-start) · [최근 업데이트](#recent-updates)

</div>

이 포크에서 추가한 실험적 스타일 23종, 자세 게이트, Golden Hook 세부 규칙은 [English](README.en.md#fork-additions)와 [Tiếng Việt](README.vi.md#fork-additions) README에 정리되어 있습니다.

<!-- readme:demos -->

<a id="style-gallery"></a>

## 원하는 스타일을 골라 보세요

### 스타일 1: 미니멀 흑백

적은 선으로도 큰 개념을 명확하게 전달할 수 있습니다. 새하얗거나 새까만 화면에서 인물, 소품, 강조색이 이야기를 이끕니다. 빠르고 이해하기 쉬운 설명 영상에 잘 어울립니다.

- **화면 특징:** 둥근 머리, 선으로 된 팔다리, 일정한 선 두께에 간단한 표정을 더할 수 있습니다. 선명한 강조색은 최대 3개로 감정, 위험, 행동을 구분합니다. 불안을 감옥으로, 집중력을 게이지로 표현하듯 추상적인 개념을 장면으로 풀어냅니다.
- **추천 주제:** 과학 상식, 심리, 자기관리, 동기부여, 비즈니스 분석, 개념 설명.
- **선택 기준:** 흰 배경은 깔끔하고 직관적입니다. 검은 배경은 대비가 강해 긴장감과 감정을 강조하기 좋습니다.

<table width="100%">
<tr>
<td width="50%" align="center"><img src="docs/core-previews/style-1-light.gif" alt="흰 배경: 걱정의 우리가 떨어지자 창살을 구부려 빠져나온다" width="360"><br><sub>흰 배경: 걱정의 우리가 떨어지자 창살을 구부려 빠져나온다</sub></td>
<td width="50%" align="center"><img src="docs/core-previews/style-1-dark.gif" alt="검은 배경: 진행 막대를 밀어 파란색으로 채운다" width="360"><br><sub>검은 배경: 진행 막대를 밀어 파란색으로 채운다</sub></td>
</tr>
</table>

<p align="center"><sub>코드 리그로 그렸고 자세 게이트를 통과했습니다.</sub></p>


---

### 스타일 2: 모던 팝

빨간 비니와 노란 티셔츠가 캐릭터의 트레이드마크입니다. 깔끔한 테크 공간에서 제품을 설명할 수도, 침실이나 거리, 자연 속에서 이야기를 펼칠 수도 있습니다.

- **화면 특징:** 한 캐릭터, 두 가지 무대입니다. 2A는 흰 공간과 은은한 격자, 떠 있는 유리 느낌의 UI, 청록·파랑 빛을 사용합니다. 2B는 컬러 배경과 영화 같은 조명, 공간감으로 이야기의 분위기를 만듭니다.
- **추천 주제:** 2A는 AI 도구, 테크 제품, 사용법, 기능 소개에 적합합니다. 2B는 성장 경험, 일상, 모험, 동기부여 이야기에 어울립니다.
- **선택 기준:** 도구나 방법을 설명하려면 2A, 캐릭터의 경험을 따라가는 이야기라면 2B를 선택하세요.


이 포크의 기본 주인공은 짧은 검은 스포츠머리, 검은 사각 안경, 흰 반소매 버튼 셔츠, 청바지 차림입니다. 체형은 업스트림 주인공과 같습니다([캐릭터 시트](docs/lead-character/sheet.png), [자세히](README.en.md#fork-additions)).

<p align="center"><img src="docs/lead-character/motion.gif" alt="스포츠머리에 안경, 흰 셔츠와 청바지를 입은 막대 인간이 걸어와 손을 흔든다" width="480"></p>

<p align="center"><img src="docs/lead-character/sheet.png" alt="남의 캐릭터 시트: 네 방향, 외형 고정, 표정, 포즈" width="760"></p>

---

### 스타일 3: 선사시대 손그림 / 블랙코미디

스마트폰도 사무실도 없던 시대에 오늘의 고민을 가져가면 어떨까요? 동굴, 가죽옷, 모닥불, 과장된 표정으로 직장과 인간관계의 익숙한 모순을 반전 있는 이야기로 만듭니다.

- **화면 특징:** 거친 손그림 선, 흰색으로 채운 머리, 가느다란 검은 팔다리, 가죽옷, 흙빛 배경. 인물 간 상호작용과 표정, 코미디의 타이밍을 살립니다. 성별과 나이는 이야기에 맞춰 정하며, 새 이야기마다 같은 얼굴을 쓸 필요는 없습니다.
- **추천 주제:** 선사시대 상상, 직장 풍자, 인간관계 관찰, 블랙코미디, 우화, 어린이 영어 이야기.
- **선택 기준:** 짧은 사건 뒤에 뜻밖의 결말을 보여 주고 싶을 때 좋습니다. 현대의 관계를 원시 부족으로 옮기면 낯설면서도 익숙한 웃음이 생깁니다.

<p align="center"><img src="docs/core-previews/style-3.gif" alt="동굴에서 족장이 구운 고기를 건네고 원시인이 받는다" width="480"></p>

<p align="center"><sub>동굴에서 족장이 구운 고기를 건네고 원시인이 받는다. 코드 리그로 그렸고 자세 게이트를 통과했습니다.</sub></p>


---

### 스타일 4: 따뜻한 일상 이야기

아까워서 못 쓰는 머그잔, 바로 답해야 할 것 같은 메시지, 모처럼 나를 위해 비워 둔 오후. 단순한 캐릭터가 색감 있는 일상 속으로 들어가 동작, 표정, 카메라로 공감 가는 순간을 전합니다.

- **화면 특징:** 흰색으로 채운 둥근 머리, 길고 가느다란 몸통, 검은 팔다리, 자연스러운 작은 표정과 컬러 2D 배경. 넓은 화면으로 장소를 보여 주고, 클로즈업으로 망설임이나 안도감을 담고, 이동 촬영으로 다음 장면에 연결합니다.
- **추천 주제:** 일상 공감, 마음의 성장, 인간관계, 따뜻한 이야기, 습관 만들기, 어린이 영어.
- **선택 기준:** 보는 사람이 “내 얘기 같다”고 느낄 생활 속 한 장면을 담고 싶을 때 선택하세요. 색과 빛은 주제에 따라 바뀌며, 따뜻함뿐 아니라 불안과 피로, 새로운 시작도 표현합니다.

<p align="center"><img src="docs/core-previews/style-4.gif" alt="길가 카페 테이블에서 커피를 한 모금 마신다" width="480"></p>

<p align="center"><sub>길가 카페 테이블에서 커피를 한 모금 마신다. 코드 리그로 그렸고 자세 게이트를 통과했습니다.</sub></p>


<!-- readme:advantages -->

## Skill이 도와주는 일

그림체만 정하는 것이 아니라, 대본과 화면을 함께 설계합니다.

| 항목 | 결과물 |
|---|---|
| **대본** | 도입, 전개, 마무리. 내레이션과 내용 확인용 번역. |
| **화면** | 인물의 동작, 소품, 카메라, 전환, 효과음. |
| **연속성** | 인물·소품·목소리 설정과 클립 사이의 연결. |
| **화면 비율** | 가로·세로 화면에 맞춘 구도와 샷. |
| **수정** | 먼저 기획안을 확인한 뒤 최종 사양서를 받는 방식. |

<!-- readme:output -->

먼저 **연출 기획안**에서 내레이션, 장면, 카메라, 사운드 디자인을 확인합니다. 승인하면 약 10초 구간마다 모션 그래픽으로 만들 수 있는 독립된 **segment spec(구간 사양서)**과 전환·편집·자막 안내를 받습니다.

Skill은 기획과 사양서를 담당합니다. 영상은 모션 그래픽으로 만듭니다. 캐릭터는 선택한 스타일로 그린 리그, 배경·소품·효과는 레이어이고, 내레이션은 별도 트랙으로 녹음하거나 음성 합성합니다. 마지막으로 편집 프로그램에서 이어 붙이고 음악과 자막을 넣습니다. Skill을 쓰기 위해 API나 MCP를 설정할 필요는 없습니다.

<!-- readme:install -->

<a id="quick-start"></a>

## 시작하기

### 1. Skill 설치하기

사용 중인 AI에게 아래 문장을 보내세요.

```text
이 Skill을 설치해 줘:
https://github.com/kaomei/stickman-video-director
```

<!-- readme:workflow -->

### 2. 주제 알려 주기

주제만 알려 줘도 되고, 작성한 글이나 기사를 그대로 전달해도 됩니다.

```text
「인류 최초의 일자리는 어떻게 생겼을까?」라는 스틱맨 영상을 만들어 줘.
```

### 3. 안내에 따라 설정하고 기획안 확인하기

**설정 선택 → 기획안 확인 → 필요한 부분 수정 → 승인 후 사양서 받기.**

화면 비율이나 스타일을 정하지 않았다면 Skill이 먼저 물어봅니다. 가로 `16:9` 또는 세로 `9:16`와 원하는 스타일을 고르면 됩니다. 이미 알려 준 설정은 다시 묻지 않습니다. 길이는 기본 60초이며, “먼저 30초로 해 보자”라고 요청해도 됩니다.

설정이 정해지면 이야기 구조, 구간별 내레이션, 인물 동작, 카메라와 소리를 담은 기획안이 나옵니다. 전체 흐름을 살펴보고 마음에 들지 않는 부분을 고친 뒤 승인하면 구간별 사양서를 받습니다.

**「인류 최초의 일자리는 어떻게 생겼을까?」 | 가로 16:9 · 스타일 3 · 30초**

승인된 스토리보드 예시입니다. 내레이션은 샘플 원문을 그대로 실었습니다.

| 시간 | 장면과 동작 | 내레이션 |
|---|---|---|
| **0–10초: 골칫거리는 밖으로** | 원시인이 돌 몽둥이를 끌고 동굴로 돌아와 짚 침대에 쓰러진다. 입구에 검치호의 거대한 그림자가 드리운다. 한쪽 눈을 뜨고 “또?”라는 표정을 짓는다. 큰 바위를 굴려 입구를 막고 손의 먼지를 턴 뒤 다시 눕는다. 만족스러운 얼굴로 마무리한다. | **“Ten thousand years ago, one man finally solved all his problems. He shut them outside.”** |
| **10–20초: 상사가 찾아왔다** | 눈을 감자 입구에서 세 번의 노크 소리가 난다. 바위가 조금 열리고 부족장이 웃으며 창을 내민다. 손사래를 치자 이번에는 구운 고기를 꺼낸다. 원시인이 킁킁 냄새를 맡고 눈을 크게 뜬다. 동굴 밖으로 전환하면 이미 창을 든 채 맹수의 발자국 쪽으로 떠밀리고 있다. | **“Then someone offered him food… in exchange for a small favor. Congratulations. Employment was invented.”** |
| **20–30초: 진보의 대가** | 먼지를 뒤집어쓰고 같은 동굴로 돌아와 창을 던지고 고기를 기다린다. 부족장은 영업용 미소로 작은 고기 한 조각을 주더니, 창 한 다발을 안겨 주고 어깨를 두드린 뒤 떠난다. 고기와 창을 번갈아 보고 천천히 카메라를 바라본다. 다시 누우려다 품에 안은 창이 몸에 배겨 벌떡 몸을 일으킨다. | **“The reward got smaller. The workload got bigger. And somehow… they called that progress.”** |

대사나 장면이 마음에 들지 않으면 바로 수정을 요청하세요. 최종 사양서는 승인한 뒤에만 출력됩니다. 이 30초 예시는 인물·동작·카메라·내레이션·사운드를 포함한 약 10초짜리 사양서 3개로 구성됩니다.

### 4. 구간을 만들고 편집하기

사양서에 따라 구간별로 만듭니다. 캐릭터 리그를 한 번 만들고, 세 개의 비트에 키를 넣어 렌더링합니다. 최종 렌더링 전에 캐릭터별 포즈 데이터를 내보내 자세 게이트를 통과시키세요. 내레이션은 영상 전체를 한 번에 녹음하고, CapCut 같은 편집 프로그램에서 클립을 이어 붙인 뒤 음악, 효과음, 자막을 넣습니다. 보통 30초는 약 10초 구간 3개, 60초는 6개로 만듭니다.

스타일 2 주인공에는 샘플 리그(`docs/lead-character/render.py`)가 있습니다. Skill은 무료입니다.

<!-- readme:reliability -->

## 제작할 때 알아두면 좋은 점

<!-- readme:platforms -->

**가로 영상과 세로 영상, 무엇을 고를까요?**

| 비율 | 추천 플랫폼 | 구도 |
|---|---|---|
| `9:16` | YouTube Shorts, TikTok, Instagram Reels | 세로 동작, 중앙 피사체, 모바일 화면 안전 영역 |
| `16:9` | YouTube, 가로형 교육·설명 영상 | 좌우 이동, 넓은 장면, 나란히 비교하는 구성 |

얼굴을 드러내지 않는 설명 영상, 역사·비즈니스, 심리와 성장, 일상 이야기, 제품 소개에 활용할 수 있습니다. 영어 내레이션에 나중에 두 언어의 자막을 넣으면 어린이 영어, 짧은 상황극, 문장 학습 콘텐츠로도 사용할 수 있습니다. 길이는 10초 단위로 30초, 60초, 90초, 3분 등으로 지정할 수 있습니다.

- 한 영상에서는 인물, 소품, 목소리 설정을 유지합니다. 목소리를 바꾸려면 먼저 기획안에서 정하세요.
- 특정 클립의 인물이나 소품이 달라졌다면 리그나 키를 고쳐 그 클립만 다시 렌더링하면 됩니다. 전부 다시 만들 필요는 없습니다.
- 대본의 재미를 살리되, 근거 없는 사실·수치·제품 효과를 만들어 넣지 않습니다.

<a id="recent-updates"></a>

## 최근 업데이트

- **2026-10-22:** 모션 그래픽 전용으로 바뀌었습니다. 승인 후 출력은 구간별 사양서이고, 자세 게이트는 렌더링 후 리그에서 내보낸 포즈 데이터로 실행하며, 내레이션은 영상 전체를 한 번에 녹음합니다. 예전 데모 클립은 첫 화면에서 뺐습니다.
- **2026-10-15:** 중국어 첫 화면, 설치 안내, 예시 설명을 정리하고 가벼운 미리보기와 Star History를 추가했습니다. Skill 규칙은 그대로입니다.
- **2026-10-14:** 스타일 4와 역·카페를 배경으로 한 예시 2개를 추가했습니다.
- **2026-10-13:** 스타일 1의 인물 묘사와 현재 자세에 관한 제약을 개선했습니다.
- **2026-10-12:** 모든 스타일에 공통으로 쓰는 목소리 일관성 규칙을 개선하고 선사시대·커뮤니티 예시를 추가했습니다.

페이지 구성만 달라졌다면 다시 설치하지 않아도 됩니다. 스타일 4가 필요하거나 인물·목소리 규칙이 바뀌기 전에 설치했다면 Skill을 업데이트하세요.

<!-- readme:contribute -->

## 다음에는 어떤 스타일이 좋을까요?

아래 스타일은 계획 중이며 아직 제공하지 않습니다.

- **다른 매체와 결합한 배경** — 2D 스틱맨을 더 풍부한 환경과 조합합니다.
- **스타일 5: 칠판 설명** — 칠판을 활용한 강의와 지식 전달.
- **스타일 6: 손그림 그림책** — 동화, 우화, 어린이 이야기.
- **스타일 7: 그래피티 액션** — 격투 장면, 연속 동작, 짧은 액션물.
- **스타일 8: 두 사람의 시트콤** — 티키타카, 일상의 오해, 직장 이야기의 반전.
- **스타일 9: 카드 게임 모험** — 레벨업, 몬스터 전투, 게임 형식의 이야기.

새 스타일 제안, 작품 공유, 문제 제보는 [Issues](https://github.com/kaomei/stickman-video-director/issues)에 남겨 주세요. 스타일 제안에는 참고 영상과 만들고 싶은 주제를, 작품 제출에는 영상·사용한 스타일·작가 링크를 함께 보내 주시면 소개와 크레딧 표기에 도움이 됩니다.

## Star 증가 추이

⭐ **대본을 짜거나 캐릭터 오류를 고치는 시간을 아끼셨다면 Star로 응원해 주세요. 다음 영상을 만들 때 다시 찾아오기에도 좋습니다.**

제작자 [Kaomei](https://x.com/CrazyKaomei)입니다. 앞으로도 새 스타일을 직접 테스트하고, 유용했던 스타일과 제작 방법, 시행착오를 무료로 정리하겠습니다. 도구와 씨름하는 시간은 줄이고, 정말 하고 싶은 이야기에 더 많은 시간을 쓰실 수 있으면 좋겠습니다.

<div align="center">
<a href="https://www.star-history.com/?repos=kaomei%2Fstickman-video-director&amp;type=date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=kaomei/stickman-video-director&amp;type=Date&amp;theme=dark">
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=kaomei/stickman-video-director&amp;type=Date">
    <img src="https://api.star-history.com/svg?repos=kaomei/stickman-video-director&amp;type=Date" alt="kaomei/stickman-video-director의 GitHub Star 증가 그래프" width="800">
  </picture>
</a>
</div>

## 라이선스

[MIT License](LICENSE)로 공개합니다. 무료 사용, 수정, 상업적 이용, 재배포가 가능합니다. 프로젝트 또는 주요 부분을 배포할 때는 저작권 표시와 라이선스 고지를 유지해 주세요.

프로젝트는 어떠한 보증 없이 현 상태로 제공됩니다. 전체 조건은 [LICENSE](LICENSE)를 확인해 주세요.
