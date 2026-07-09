#!/usr/bin/env python3
"""Transcreve os áudios da degustação (dados/audios-degustacao/) pra texto.

Uso: python3 scripts/transcrever-audios.py [modelo] [pasta]
  modelo: tiny | base | small | medium | large-v3   (padrão: small)
  pasta:  diretório com os áudios                    (padrão: dados/audios-degustacao)

Roda 100% local (faster-whisper). Nenhum áudio sai da máquina.
Saída: saidas/transcricao-audios-degustacao.md
"""
import sys, os, glob, re
from faster_whisper import WhisperModel

EXTS = (".opus", ".ogg", ".m4a", ".mp3", ".wav", ".aac", ".mp4", ".flac")
OUT = "saidas/transcricao-audios-degustacao.md"


def natkey(path):
    """Ordena pelo número no nome (Audio Chedid - 1, ...4, ...10) e não alfabético."""
    nums = re.findall(r"\d+", os.path.basename(path))
    return (int(nums[-1]) if nums else 0, os.path.basename(path))


def main():
    model_size = sys.argv[1] if len(sys.argv) > 1 else "small"
    audio_dir = sys.argv[2] if len(sys.argv) > 2 else "dados/audios-degustacao"

    files = sorted((f for f in glob.glob(os.path.join(audio_dir, "*"))
                    if f.lower().endswith(EXTS)), key=natkey)
    if not files:
        sys.exit(f"Nenhum áudio em {audio_dir}/ (formatos aceitos: {', '.join(EXTS)})")

    print(f"Carregando modelo '{model_size}' (baixa na 1ª vez, ~1 min)...")
    model = WhisperModel(model_size, device="cpu", compute_type="int8")

    parts = [
        "# Transcrição — áudios da degustação (Henrique)",
        f"\n> Gerado localmente com faster-whisper (modelo `{model_size}`). {len(files)} áudios.",
        "> Ordem = ordem alfabética do nome do arquivo. Revisar nomes próprios/termos técnicos.\n",
    ]
    for i, f in enumerate(files, 1):
        name = os.path.basename(f)
        print(f"[{i}/{len(files)}] {name} ...", flush=True)
        segments, info = model.transcribe(f, language="pt", vad_filter=True)
        text = " ".join(s.text.strip() for s in segments).strip()
        dur = round(info.duration)
        parts.append(f"\n## {i}. {name}  ({dur}s)\n\n{text or '_(sem fala detectada)_'}\n")
        print(f"    -> {len(text)} chars", flush=True)

    os.makedirs("saidas", exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(parts))
    print(f"\n✅ {OUT} — {len(files)} áudios transcritos")


if __name__ == "__main__":
    main()
