# Language Reactor Quiz

📘 영어 자막 기반 학습용 퀴즈 프로그램입니다.  
번역을 보고 영어 문장을 입력하면 유사도를 채점해줍니다.  
즐겨찾기 및 단어장 기능을 통해 반복 학습이 가능합니다.

---

## 📦 포함 파일

| 파일명                | 설명                                 |
|-----------------------|--------------------------------------|
| `LanguageReactorQuiz.exe` | 실행 파일 (Python 없이 실행 가능)     |
| `example.csv`         | 예제 자막 CSV                        |
| `background.jpg`      | 홈 화면 배경 이미지                  |

---

## 🚀 사용 방법

1. `LanguageReactorQuiz.exe` 실행  
2. `📁 CSV 불러오기` 버튼 클릭 → `example.csv` 선택  
3. 퀴즈 시작

> ⛔ 실행 후 CSV를 불러오기 전까지는 퀴즈가 시작되지 않습니다.

---

## 📄 CSV 형식 설명

CSV 파일은 아래와 같은 두 열이 필수입니다:

- `Subtitle`: 원문 영어 자막  
- `Human Translation`: 번역된 문장  

```csv
Subtitle,Human Translation
I'm on my way.,가는 중이야.
It's my favorite place.,여기가 내가 제일 좋아하는 곳이야.
```

---

## 🧠 기능 요약

- 🔠 번역 → 영어 입력 → 유사도 점수 확인
- ⭐ 즐겨찾기 / 📚 단어장 (자동 저장)
- 🎨 테마, 정답 보기, 문제 랜덤 설정
- 🔄 종료 시 자동 저장: `favorites.json`, `vocab.json`

---

## 💡 팁

- 정답이 궁금하면 `정답 보기 ON/OFF`를 눌러보세요.
- 키워드를 클릭해 단어장에 추가하거나 제거할 수 있습니다.
- 즐겨찾기나 단어는 더블클릭으로 삭제할 수 있습니다.

---

## 🛠 제작 환경

- Python 3.9+
- tkinter + ttkbootstrap
- pandas, PIL, difflib