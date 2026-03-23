# Agent Rules

## 프로젝트 구조

- `app/clone.py` — Qwen3-TTS 음성 복제 모듈 및 CLI 진입점
- `utility/` — 범용 유틸리티 (YouTube 오디오 추출 등, Qwen과 무관)

## 긴 텍스트 처리

- 긴 텍스트는 문장 단위로 자동 분할하여 생성한다.
- 문장별로 생성 후 하나의 WAV로 합친다.
- `voice_clone_prompt`를 재사용하여 문장 간 목소리 일관성을 유지한다.
- 텍스트 분할은 `app/clone.py`의 `split_sentences()`에서 처리한다.
- 생성 파라미터(`GEN_KWARGS`)는 공식 예제를 참조하여 설정했다.

## 참조

- [Qwen3-TTS 공식 예제 (test_model_12hz_base.py)](https://github.com/QwenLM/Qwen3-TTS/blob/main/examples/test_model_12hz_base.py) — `GEN_KWARGS` 파라미터 및 `generate_voice_clone` 사용법 참조
