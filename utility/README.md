# Utility

Qwen3-TTS와 직접 관련 없는 범용 유틸리티 모듈입니다.

## YouTube 오디오 추출

YouTube 영상에서 레퍼런스 오디오용 WAV 파일을 추출합니다. [ffmpeg](https://ffmpeg.org/) 설치가 필요합니다.

### 사용법

macOS / Linux:

```bash
uv run python clone_my_voice.py extract-audio \
    --url "https://youtu.be/YOUR_VIDEO_ID"
```

Windows (PowerShell):

```powershell
uv run python clone_my_voice.py extract-audio `
    --url "https://youtu.be/YOUR_VIDEO_ID"
```

`ref_audio/` 디렉터리에 WAV 파일이 생성됩니다.

### 레퍼런스 오디오 구간 자르기

추출된 전체 오디오에서 본인 목소리가 깨끗하게 들리는 **5~15초 구간**을 잘라냅니다.

macOS / Linux:

```bash
ffmpeg -i ref_audio/원본.wav -ss 00:00:10 -to 00:00:20 -c copy ref_audio/my_voice.wav
```

Windows (PowerShell):

```powershell
ffmpeg -i ref_audio\원본.wav -ss 00:00:10 -to 00:00:20 -c copy ref_audio\my_voice.wav
```

잘라낸 구간의 **대사를 정확히 받아 적으세요**. 이 텍스트가 `--ref-text`로 사용됩니다.

### 옵션

| 옵션 | 설명 | 기본값 |
|---|---|---|
| `--url` | YouTube URL (필수) | - |
| `--output` | 출력 디렉터리 | `ref_audio/` |
