# 근무시간 관리 (Work Tracker)

간단한 데스크탑 근무 시간 관리 앱입니다. Tkinter 기반 UI로 근무 시작/휴식/종료를 기록하고, SQLite 데이터베이스에 세션을 저장합니다. Windows 알림과 소리 알림을 지원합니다.

**주요 기능**
- 근무 시작/휴식/재시작/종료
- 휴식 알림(윈도우 알림 또는 소리)
- 세션 기록 저장 (SQLite)
- 간단한 통계/설정 화면

**요구 사항**
- Python 3.8 이상
- Windows 권장(윈도우 알림 사용 시)
- 필요한 패키지:
  - `pygame`
  - `winotify`

설치:

```powershell
python -m pip install pygame winotify
```

실행:

```powershell
python main.py
```

프로젝트 구조
- [main.py](main.py) : 애플리케이션 진입점, 윈도우 및 프레임 초기화
- [database.py](database.py) : SQLite 초기화 및 설정/조회 유틸
- [screens/](screens/) : 화면별 UI 컴포넌트
  - [screens/main_screen.py](screens/main_screen.py) : 메인 화면, 타이머 및 세션 저장
  - [screens/settings_screen.py](screens/settings_screen.py) : 설정 화면
  - [screens/break_alarm_screen.py](screens/break_alarm_screen.py) : 휴식 알림 설정 및 툴팁
  - [screens/statistics_screen.py](screens/statistics_screen.py) : 통계 화면(간단 표시)
- [sounds/](sounds/) : 소리 알림을 위한 파일을 넣을 디렉터리(비어있음)

노트 및 개선 제안
- `winotify`는 Windows 전용 알림 라이브러리입니다. 다른 플랫폼 지원이 필요하면 대체 라이브러리를 고려하세요.
- 소리 파일을 `sounds/`에 추가하면 소리 알림을 사용할 수 있습니다.
- 데이터베이스 파일은 실행 디렉터리에 `work_tracker.db`로 생성됩니다.

라이센스
- 개인/내부 용도로 자유롭게 사용하세요.
