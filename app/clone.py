import argparse
import re
import sys
import time
from pathlib import Path

import numpy as np
import soundfile as sf
import torch
from qwen_tts import Qwen3TTSModel

from utility.extract import download_audio

GEN_KWARGS = {
  "max_new_tokens": 2048,
  "do_sample": True,
  "top_k": 50,
  "top_p": 1.0,
  "temperature": 0.9,
  "repetition_penalty": 1.05,
  "subtalker_dosample": True,
  "subtalker_top_k": 50,
  "subtalker_top_p": 1.0,
  "subtalker_temperature": 0.9,
}


def read_text(value: str) -> str:
  if value.startswith("@"):
    file_path = Path(value[1:]).expanduser()
    if not file_path.exists():
      print(f"ERROR: 파일을 찾을 수 없습니다: {file_path}")
      sys.exit(1)
    if not file_path.is_file():
      print(f"ERROR: 파일이 아닙니다: {file_path}")
      sys.exit(1)
    return file_path.read_text(encoding="utf-8").strip()
  return value


def detect_attn_implementation():
  try:
    import flash_attn  # noqa: F401

    return "flash_attention_2"
  except ImportError:
    return "sdpa"


def load_model(model_name: str) -> Qwen3TTSModel:
  if not torch.cuda.is_available():
    print("ERROR: CUDA GPU가 필요합니다. NVIDIA GPU가 있는 머신에서 실행하세요.")
    sys.exit(1)

  attn_impl = detect_attn_implementation()
  print(f"Loading model: {model_name} (attn: {attn_impl})")
  return Qwen3TTSModel.from_pretrained(
    model_name,
    device_map="cuda:0",
    dtype=torch.bfloat16,
    attn_implementation=attn_impl,
  )


def split_sentences(text: str, language: str = "Korean") -> list[str]:
  if language == "Korean":
    parts = re.split(r"(?<=[.!?。！？])\s*", text)
  else:
    parts = re.split(r"(?<=[.!?])\s+", text)

  sentences = [s.strip() for s in parts if s.strip()]
  return sentences


def generate_chunks(model, sentences, language, voice_prompt):
  all_wavs = []
  sr = None
  total = len(sentences)

  for i, sentence in enumerate(sentences):
    torch.cuda.synchronize()
    start = time.time()
    print(f"  [{i + 1}/{total}] {sentence[:40]}...")

    wavs, sr = model.generate_voice_clone(
      text=sentence,
      language=language,
      voice_clone_prompt=voice_prompt,
      **GEN_KWARGS,
    )
    all_wavs.append(wavs[0])

    torch.cuda.synchronize()
    elapsed = time.time() - start
    print(f"           {elapsed:.1f}s")

  return all_wavs, sr


def concatenate_wavs(wav_list, sr, pause_sec=0.3):
  if not wav_list:
    return np.array([], dtype=np.float32)
  pause = np.zeros(int(sr * pause_sec), dtype=wav_list[0].dtype)
  pieces = []
  for i, wav in enumerate(wav_list):
    pieces.append(wav)
    if i < len(wav_list) - 1:
      pieces.append(pause)
  return np.concatenate(pieces)


def clone_voice(
  ref_audio: str,
  ref_text: str,
  texts: list[str],
  language: str = "Korean",
  model_name: str = "Qwen/Qwen3-TTS-12Hz-1.7B-Base",
  output_dir: str = "output",
):
  model = load_model(model_name)
  output_path = Path(output_dir)
  output_path.mkdir(parents=True, exist_ok=True)

  print(f"Reference audio: {ref_audio}")
  print(f"Reference text: {ref_text}")

  voice_prompt = model.create_voice_clone_prompt(
    ref_audio=ref_audio,
    ref_text=ref_text,
    x_vector_only_mode=False,
  )

  for text_idx, text in enumerate(texts):
    sentences = split_sentences(text, language)
    if not sentences:
      print(f"\n[Text {text_idx + 1}/{len(texts)}] 빈 입력, 건너뜀")
      continue
    print(f"\n[Text {text_idx + 1}/{len(texts)}] {len(sentences)} sentence(s)")

    torch.cuda.synchronize()
    total_start = time.time()

    if len(sentences) == 1:
      wavs, sr = model.generate_voice_clone(
        text=sentences[0],
        language=language,
        voice_clone_prompt=voice_prompt,
        **GEN_KWARGS,
      )
      combined = wavs[0]
    else:
      wav_list, sr = generate_chunks(model, sentences, language, voice_prompt)
      combined = concatenate_wavs(wav_list, sr)

    torch.cuda.synchronize()
    total_elapsed = time.time() - total_start
    duration = len(combined) / sr

    file_path = output_path / f"cloned_voice_{text_idx:03d}.wav"
    sf.write(str(file_path), combined, sr)
    print(f"Saved: {file_path} ({duration:.1f}s audio, {total_elapsed:.1f}s elapsed)")

  print("Done!")


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
    help="레퍼런스 대사 텍스트 또는 @파일경로",
  )
  clone_parser.add_argument(
    "--text",
    required=True,
    nargs="+",
    help="생성할 텍스트 또는 @파일경로 (여러 개 가능)",
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
      ref_text=read_text(args.ref_text),
      texts=[read_text(t) for t in args.text],
      language=args.language,
      model_name=args.model,
      output_dir=args.output,
    )


if __name__ == "__main__":
  main()
