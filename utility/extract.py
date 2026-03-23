from pathlib import Path

import yt_dlp


def download_audio(url: str, output_dir: str = "ref_audio"):
  output_path = Path(output_dir)
  output_path.mkdir(parents=True, exist_ok=True)

  output_template = str(output_path / "%(title)s.%(ext)s")

  ydl_opts = {
    "format": "bestaudio/best",
    "postprocessors": [
      {
        "key": "FFmpegExtractAudio",
        "preferredcodec": "wav",
        "preferredquality": "0",
      }
    ],
    "outtmpl": output_template,
  }

  with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    print(f"Downloading audio from: {url}")
    ydl.download([url])

  print(f"Audio saved to: {output_path}/")
  print_next_steps()


def print_next_steps():
  print()
  print("=== Next Steps ===")
  print("1. 추출된 WAV 파일에서 본인 목소리가 깨끗한 구간(5~15초)을 잘라내세요.")
  print(
    "   예: ffmpeg -i input.wav -ss 00:00:10"
    " -to 00:00:20 -c copy ref_audio/my_voice.wav"
  )
  print("2. 잘라낸 구간의 대사를 정확히 받아 적으세요 (ref-text로 사용).")
  print("3. clone 명령어를 실행하세요.")
