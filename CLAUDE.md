# 뿌요 대본 보드 — 저장소 규칙 (Claude Code용)

GitHub Pages 배포. 새 회차 추가 순서:
1. `scripts/NN_제목.md` 작성 (NN 두 자리)
2. `episodes.json` 의 episodes 배열에 항목 추가 — n, title, given(YYYY-MM-DD, 반드시 수요일, 이전 회차 +7), status, hook, file, memo, sources([[제목, URL], ...])
3. `python3 build.py` 실행 → 루트 index.html + epNN/index.html 재생성
4. push (커밋 메시지 한글, 바뀐 것 목록)

## md 형식
- `## 0:00 훅` 처럼 `## 시간 구간명` 으로 구간 시작
- 낭독 문장은 한 줄에 한 호흡 · 화면 지시는 `[화면: ...]` 한 줄 · 뿌요가 채울 값은 【 】
- 인포그래픽은 `assets/epNN_이름.svg` (viewBox 900×260~300, 배경 #0F172A, 강조 #F59E0B/#FDE68A) → `![설명](assets/epNN_이름.svg)`
- 상단 `> ` 메모는 음절 계산 제외. 목표 2,800~3,100음절

## 주제 후보
- `topics.json` 에 3~20화 후보(단계별). 회차 확정 시 episodes.json으로 옮기고 topics 항목은 그대로 둔다(자동으로 "대본 완료" 표시).

## 페이지 규칙
- 각 페이지 self-contained (CSS·JS 인라인, 외부는 구글 폰트만). 수정은 build.py의 CSS/템플릿을 통째로 다시 쓴다.
- 촬영일(+2)·공개일(+10)은 build.py가 계산. status: 시작 전/대본 작성 중/대본 완료/촬영 완료/공개 완료

## 톤·구조
- 전문가 톤. 감탄사·'여러분'·'~잖아요' 금지. 훅 = 숫자+반전+약속. 매 회차 솔직 구간 1개. CTA는 마지막 한 번, 고정 문장: "앞으로도 이런 정보 원하시는 분들은 구독, 좋아요, 알림 설정 부탁드립니다." 그다음 "뿌요였습니다."
- 숫자·금리·상품 조건은 검색으로 확인된 것만, 미확인은 "확인 필요". sources에 실제 URL.
