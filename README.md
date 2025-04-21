# 📘 Language Reactor Quiz

**영어 자막 기반 단어 학습 & 퀴즈 앱**  
Language Reactor로 추출한 CSV 파일을 기반으로 퀴즈를 풀고 단어를 수집하고 복습할 수 있는 Python GUI 프로그램입니다.

---

## 🚀 시작하기

### 1. 환경 설치
Python 3.9 이상이 설치되어 있어야 합니다.

```bash
pip install -r requirements.txt
```

또는 직접 설치할 경우:

```bash
pip install ttkbootstrap pandas pillow
```

### 2. 실행

```bash
python main.py
```

---

## 📂 구성 파일

| 파일명 | 설명 |
|-------|------|
| `main.py` | 프로그램 실행 파일 |
| `background.jpg` | 홈 화면 배경 이미지 |
| `example.csv` | 예제 자막 CSV 파일 (Subtitle, Human Translation 컬럼 필요) |
| `favorites.json` | 즐겨찾기 자동 저장 파일 (앱 종료 시 생성됨) |
| `vocab.json` | 단어장 자동 저장 파일 (앱 종료 시 생성됨) |

---

## 💡 기능

- ✅ CSV 불러오기 (자막 + 번역)
- ✅ 퀴즈 풀이 & 유사도 채점
- ✅ 정답 단어 클릭 시 단어장 추가
- ✅ 즐겨찾기 기능 (퀴즈 문제 저장)
- ✅ 단어장 / 즐겨찾기 저장 및 삭제
- ✅ 홈 화면 배경 이미지 및 테마 설정


---

## 📝 예제 CSV 형식

```csv
Subtitle,Human Translation
I love you,사랑해
Where are you going?,어디 가?
```

---

## 🛠 기타

- `background.jpg`는 필수입니다. (없을 경우 오류 발생)
- 단어장은 `vocab.json`, 즐겨찾기는 `favorites.json`에 자동 저장됩니다.
