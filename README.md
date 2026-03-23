# CloneVoiceFromQwen3TTS

Qwen3-TTS를 활용한 음성 복제(Voice Cloning) 프로젝트입니다.

## 요구사항

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (패키지 관리)
- NVIDIA GPU + CUDA

## 환경 설정

### macOS

```bash
git clone https://github.com/YOUR_USERNAME/CloneVoiceFromQwen3TTS.git
cd CloneVoiceFromQwen3TTS
uv sync
```

### Windows (PowerShell)

실행 정책 설정 (가상환경 활성화에 필요):

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

프로젝트 설정:

```powershell
git clone https://github.com/YOUR_USERNAME/CloneVoiceFromQwen3TTS.git
cd CloneVoiceFromQwen3TTS
uv sync
```

## 음성 복제

레퍼런스 오디오 파일(WAV)과 해당 대사 텍스트를 준비한 뒤 실행합니다.

> 레퍼런스 오디오가 없다면 [YouTube에서 추출](utility/README.md)할 수 있습니다.

macOS / Linux:

```bash
uv run python clone_my_voice.py clone \
    --ref-audio ref_audio/my_voice.wav \
    --ref-text "레퍼런스 구간의 정확한 대사" \
    --text "복제된 목소리로 말할 텍스트" \
    --language Korean
```

Windows (PowerShell):

```powershell
uv run python clone_my_voice.py clone `
    --ref-audio ref_audio\my_voice.wav `
    --ref-text "레퍼런스 구간의 정확한 대사" `
    --text "복제된 목소리로 말할 텍스트" `
    --language Korean
```

`output/` 디렉터리에 복제된 음성 WAV 파일이 생성됩니다.

## 여러 문장을 한 번에 생성

`--text`에 여러 텍스트를 전달하면 배치로 생성됩니다.

```bash
uv run python clone_my_voice.py clone \
    --ref-audio ref_audio/my_voice.wav \
    --ref-text "레퍼런스 대사" \
    --text "첫 번째 문장" "두 번째 문장" "세 번째 문장" \
    --language Korean
```

## 옵션

| 옵션 | 설명 | 기본값 |
|---|---|---|
| `--ref-audio` | 레퍼런스 오디오 파일 경로 (필수) | - |
| `--ref-text` | 레퍼런스 오디오의 대사 텍스트 (필수) | - |
| `--text` | 생성할 텍스트, 여러 개 가능 (필수) | - |
| `--language` | 언어 | `Korean` |
| `--model` | Qwen3-TTS 모델 | `Qwen/Qwen3-TTS-12Hz-1.7B-Base` |
| `--output` | 출력 디렉터리 | `output/` |

## 모델 선택

| 모델 | 파라미터 | 용도 |
|---|---|---|
| `Qwen/Qwen3-TTS-12Hz-1.7B-Base` | 1.7B | 고품질 음성 복제 (기본값) |
| `Qwen/Qwen3-TTS-12Hz-0.6B-Base` | 0.6B | 경량 음성 복제 |
