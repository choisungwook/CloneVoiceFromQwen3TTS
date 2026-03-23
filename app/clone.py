import sys
from pathlib import Path

import soundfile as sf
import torch
from qwen_tts import Qwen3TTSModel


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


def generate_single(model, text, language, ref_audio, ref_text):
  return model.generate_voice_clone(
    text=text,
    language=language,
    ref_audio=ref_audio,
    ref_text=ref_text,
  )


def generate_batch(model, texts, languages, ref_audio, ref_text):
  prompt_items = model.create_voice_clone_prompt(
    ref_audio=ref_audio,
    ref_text=ref_text,
    x_vector_only_mode=False,
  )
  return model.generate_voice_clone(
    text=texts,
    language=languages,
    voice_clone_prompt=prompt_items,
  )


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

  languages = [language] * len(texts)

  print(f"Reference audio: {ref_audio}")
  print(f"Reference text: {ref_text}")
  print(f"Generating {len(texts)} utterance(s)...")

  if len(texts) == 1:
    wavs, sr = generate_single(model, texts[0], languages[0], ref_audio, ref_text)
  else:
    wavs, sr = generate_batch(model, texts, languages, ref_audio, ref_text)

  save_outputs(wavs, sr, output_path)


def save_outputs(wavs, sr, output_path: Path):
  for i, wav in enumerate(wavs):
    file_path = output_path / f"cloned_voice_{i:03d}.wav"
    sf.write(str(file_path), wav, sr)
    print(f"Saved: {file_path}")

  print("Done!")
