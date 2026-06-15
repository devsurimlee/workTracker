# 작업시간 관리 (Work Tracker)

- 간단한 데스크탑 작업시간 관리 앱입니다. 
- Python, Tkinter, SQLite

### 주요 기능
- 메인: 작업시간 타이머와 휴식기능(일시정지)
- 알림설정: 휴식 알림 온/오프, 간격, 알림방식, 알림음 선택
- 통계: 일자 별 작업시간, 휴식시간 안내

### 요구사항
- Python 3.8 이상
- Windows 권장 (토스트 알림 사용 시)
- 설치할 패키지:
  - `pygame`
  - `winotify`

### 설치

```powershell
python -m pip install pygame winotify
```

### 실행

```powershell
python main.py
```

### 빌드
```
pyinstaller --noconfirm --onedir --windowed --name "workTracker" --add-data "sounds;sounds" --add-data "screens;screens" main.py

- dist/workTracker 폴더째로 사용, workTracker.exe 파일 실행.
```

### 프로젝트 구조

- [main.py](main.py) — 앱 진입점, 윈도우/프레임 초기화, 스케일링 관리
- [database.py](database.py) — SQLite 연결/초기화 및 설정 저장/조회, `get_daily_totals()` 제공
- [screens/](screens/) — 화면 및 위젯
  - [screens/main_screen.py](screens/main_screen.py) — 메인 타이머, 시작/휴식/종료 버튼
  - [screens/settings_screen.py](screens/settings_screen.py) — 설정 메뉴
  - [screens/break_alarm_screen.py](screens/break_alarm_screen.py) — 휴식 알림 설정, `IosToggleButton` 사용
  - [screens/statistics_screen.py](screens/statistics_screen.py) — 통계, 날짜 네비게이터
  - [screens/header.py](screens/header.py) — 공통 헤더 생성 유틸
  - [screens/theme.py](screens/theme.py) — 테마/폰트/스타일 정의
  - [screens/widgets.py](screens/widgets.py) — `IosToggleButton` 커스텀 위젯
- [sounds/](sounds/) — 알림용 소리 파일(사용자 추가)


### 데이터 관리
- 실행 디렉터리에 `work_tracker.db` 파일이 생성.
