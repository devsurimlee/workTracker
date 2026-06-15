# 작업시간 관리 (Work Tracker)

간단한 데스크탑 작업 시간 관리 앱입니다. Python + Tkinter로 작성되었으며, 세션을 SQLite에 저장하고 휴식 알림(Windows 알림 또는 소리)을 지원 전체 UI는 iOS 스타일의 간결한 테마(ttk 스타일 및 커스텀 토글)를 적용했습니다.


주요 기능
- 작업 시작/휴식/재시작/종료 및 세션 저장 (SQLite)
- 휴식 알림: Windows 토스트(`winotify`) 또는 소리(`pygame`) 선택 가능
- 설정 화면에서 휴식 알림 온/오프, 간격, 알림 방식 선택
- 통계 화면의 일자 선택 및 일별 합계 확인

요구 사항
- Python 3.8 이상
- Windows 권장 (토스트 알림 사용 시)
- 설치할 패키지:
  - `pygame`
  - `winotify`

설치

```powershell
python -m pip install pygame winotify
```

실행

```powershell
python main.py
```

배포
```
pyinstaller --noconfirm --onedir --windowed --name "workTracker" --add-data "sounds;sounds" --add-data "screens;screens" main.py
- dist/workTracker 폴더째로 사용
```

프로젝트 구조 (주요 파일)
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

데이터베이스
- 실행 디렉터리에 `work_tracker.db` 파일이 생성됩니다.