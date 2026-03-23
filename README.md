# CloneVoiceFromQwen3TTS

Qwen3-TTS를 활용한 음성 복제(Voice Cloning) 프로젝트입니다.

## 요구사항

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (패키지 관리)
- NVIDIA GPU + CUDA (음성 복제 실행에 필요)

> macOS는 오디오 추출 등 GPU가 필요 없는 작업만 가능합니다. 음성 복제는 NVIDIA GPU가 있는 Linux/Windows 머신에서 실행하세요.

## 환경 설정

### macOS (오디오 추출 전용)

```bash
git clone https://github.com/YOUR_USERNAME/CloneVoiceFromQwen3TTS.git
cd CloneVoiceFromQwen3TTS
uv sync
```

### Linux / Windows (음성 복제)

Windows PowerShell의 경우 실행 정책 설정이 필요합니다:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

프로젝트 설정:

```bash
git clone https://github.com/YOUR_USERNAME/CloneVoiceFromQwen3TTS.git
cd CloneVoiceFromQwen3TTS
uv sync
```

## 음성 복제

레퍼런스 오디오 파일(WAV)과 해당 대사 텍스트를 준비한 뒤 실행합니다.

> 레퍼런스 오디오가 없다면 [YouTube에서 추출](utility/README.md)할 수 있습니다. 단, 타인의 음성을 사용할 경우 저작권 및 초상권 문제가 발생할 수 있으니 주의하세요.

macOS / Linux:

```bash
uv run python -m app.clone clone \
    --ref-audio ref_audio/my_voice.wav \
    --ref-text "레퍼런스 구간의 정확한 대사" \
    --text "복제된 목소리로 말할 텍스트" \
    --language Korean
```

Windows (PowerShell):

```powershell
uv run python -m app.clone clone `
    --ref-audio ref_audio\my_voice.wav `
    --ref-text "레퍼런스 구간의 정확한 대사" `
    --text "복제된 목소리로 말할 텍스트" `
    --language Korean
```

`output/` 디렉터리에 복제된 음성 WAV 파일이 생성됩니다.

## 긴 텍스트 생성

긴 텍스트를 입력하면 자동으로 문장 단위로 분할하여 생성한 뒤 하나의 WAV 파일로 합칩니다. 1분~7분 이상의 긴 오디오도 안정적으로 생성할 수 있습니다.

```bash
uv run python -m app.clone clone \
    --ref-audio ref_audio/my_voice.wav \
    --ref-text "레퍼런스 대사" \
    --text "긴 텍스트를 입력하세요. 여러 문장이 포함되어도 됩니다. 자동으로 분할되어 생성됩니다." \
    --language Korean
```

진행 상황이 문장별로 출력됩니다:

```
[Text 1/1] 3 sentence(s)
  [1/3] 긴 텍스트를 입력하세요...       2.1s
  [2/3] 여러 문장이 포함되어도 됩니다...   1.8s
  [3/3] 자동으로 분할되어 생성됩니다...    1.5s
Saved: output/cloned_voice_000.wav (12.3s audio, 5.4s elapsed)
```

## 여러 텍스트를 한 번에 생성

`--text`에 여러 텍스트를 전달하면 각각 별도의 WAV 파일로 생성됩니다.

```bash
uv run python -m app.clone clone \
    --ref-audio ref_audio/my_voice.wav \
    --ref-text "레퍼런스 대사" \
    --text "첫 번째 텍스트" "두 번째 텍스트" "세 번째 텍스트" \
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
