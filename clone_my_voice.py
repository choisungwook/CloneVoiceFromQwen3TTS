import argparse

from app.clone import clone_voice
from utility.extract import download_audio


def build_parser():
  parser = argparse.ArgumentParser(
    description="Qwen3-TTS Voice Cloning Tool",
  )
  subparsers = parser.add_subparsers(dest="command", required=True)

  extract_parser = subparsers.add_parser(
    "extract-audio", help="YouTube 영상에서 오디오 추출"
  )
  extract_parser.add_argument("--url", required=True, help="YouTube URL")
  extract_parser.add_argument(
    "--output",
    default="ref_audio",
    help="출력 디렉터리 (default: ref_audio/)",
  )

  clone_parser = subparsers.add_parser("clone", help="음성 복제")
  clone_parser.add_argument(
    "--ref-audio",
    required=True,
    help="레퍼런스 오디오 파일 경로",
  )
  clone_parser.add_argument(
    "--ref-text",
    required=True,
    help="레퍼런스 오디오의 대사 텍스트",
  )
  clone_parser.add_argument(
    "--text",
    required=True,
    nargs="+",
    help="생성할 텍스트 (여러 개 가능)",
  )
  clone_parser.add_argument(
    "--language",
    default="Korean",
    help="언어 (default: Korean)",
  )
  clone_parser.add_argument(
    "--model",
    default="Qwen/Qwen3-TTS-12Hz-1.7B-Base",
    help="모델 (default: Qwen/Qwen3-TTS-12Hz-1.7B-Base)",
  )
  clone_parser.add_argument(
    "--output",
    default="output",
    help="출력 디렉터리 (default: output/)",
  )

  return parser


def main():
  args = build_parser().parse_args()

  if args.command == "extract-audio":
    download_audio(url=args.url, output_dir=args.output)
  elif args.command == "clone":
    clone_voice(
      ref_audio=args.ref_audio,
      ref_text=args.ref_text,
      texts=args.text,
      language=args.language,
      model_name=args.model,
      output_dir=args.output,
    )


if __name__ == "__main__":
  main()
