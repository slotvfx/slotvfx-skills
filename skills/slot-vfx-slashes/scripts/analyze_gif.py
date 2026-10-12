#!/usr/bin/env python3
"""Measure a local GIF's encoded timing and create a diagnostic contact sheet.

Requires Pillow. Example:
  python3 analyze_gif.py attack.gif --out work/attack-study --contact-sheet
Brightness is only a proxy for luminous effects on dark backgrounds.
"""

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw


def analyze(source, threshold=110, relative_threshold=0.03):
    frames, rows = [], []
    elapsed = 0
    with Image.open(source) as gif:
        if gif.format != "GIF":
            raise ValueError("Expected a GIF; do not infer GIF timing from another format.")
        size = list(gif.size)
        loop = gif.info.get("loop")
        for index in range(gif.n_frames):
            gif.seek(index)
            # Pillow seek handles GIF disposal/composition. Transparent pixels
            # contribute no light; composite them on black before measurement.
            rgba = gif.convert("RGBA")
            rgb = Image.new("RGB", rgba.size, "black")
            rgb.paste(rgba, mask=rgba.getchannel("A"))
            frames.append(rgb)
            sample = rgb.resize((128, 128), Image.Resampling.BICUBIC)
            pixels = (sample.get_flattened_data() if hasattr(sample, "get_flattened_data")
                      else sample.getdata())
            count = sum(max(pixel) > threshold for pixel in pixels)
            duration = gif.info.get("duration")
            rows.append({"index": index, "time_ms": elapsed,
                         "duration_ms": duration, "bright_pixels": count})
            # Unknown or zero duration is not silently replaced with an FPS.
            elapsed = (elapsed + duration if elapsed is not None
                       and duration is not None and duration > 0 else None)

    peak_count = max(row["bright_pixels"] for row in rows)
    peak = max(rows, key=lambda row: row["bright_pixels"]) if peak_count else None
    active = [row for row in rows if row["bright_pixels"] > peak_count * relative_threshold]
    last = active[-1] if active else None
    last_end = (last["time_ms"] + last["duration_ms"] if last
                and last["time_ms"] is not None and last["duration_ms"]
                and last["duration_ms"] > 0 else None)
    result = {
        "source": str(Path(source).resolve()), "size": size,
        "frame_count": len(rows), "encoded_cycle_ms": elapsed,
        "gif_loop_metadata": loop,
        "method": {"sample_size": [128, 128], "pixel_max_rgb_above": threshold,
                   "frame_count_above_fraction_of_peak": relative_threshold},
        "peak_frame": peak["index"] if peak else None,
        "peak_time_ms": peak["time_ms"] if peak else None,
        "first_active_frame": active[0]["index"] if active else None,
        "first_active_time_ms": active[0]["time_ms"] if active else None,
        "last_active_frame": last["index"] if last else None,
        "last_active_frame_start_ms": last["time_ms"] if last else None,
        "last_active_frame_end_ms": last_end,
        "notes": ["Encoded GIF timing is not proof of game or source timing.",
                  "Brightness thresholds do not judge motion, style or true visibility.",
                  "Null timing means a missing/zero duration prevents reliable accumulation."],
        "frames": rows,
    }
    return result, frames


def contact_sheet(frames, rows, destination):
    # Every frame is retained so a sparse selection cannot hide a discontinuity.
    columns, tile, label_height = 6, 160, 25
    sheet = Image.new("RGB", (columns * tile,
                     ((len(frames) + columns - 1) // columns) * (tile + label_height)), (24, 24, 24))
    draw = ImageDraw.Draw(sheet)
    for index, (frame, row) in enumerate(zip(frames, rows)):
        thumb = frame.copy()
        thumb.thumbnail((tile, tile), Image.Resampling.LANCZOS)
        x, y = (index % columns) * tile, (index // columns) * (tile + label_height)
        sheet.paste(thumb, (x + (tile - thumb.width) // 2, y + (tile - thumb.height) // 2))
        time = f'{row["time_ms"]}ms' if row["time_ms"] is not None else "time unknown"
        draw.text((x + 5, y + tile + 5), f"#{index}  {time}", fill="white")
    sheet.save(destination)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--threshold", type=int, default=110)
    parser.add_argument("--relative-threshold", type=float, default=0.03)
    parser.add_argument("--contact-sheet", action="store_true")
    args = parser.parse_args()
    if not 0 <= args.threshold <= 255 or not 0 <= args.relative_threshold < 1:
        parser.error("threshold must be 0..255 and relative-threshold 0..<1")
    try:
        result, frames = analyze(args.source, args.threshold, args.relative_threshold)
        args.out.mkdir(parents=True, exist_ok=True)
        report = args.out / (args.source.stem + "-timing.json")
        sheet = args.out / (args.source.stem + "-frames.jpg")
        if report.exists() or (args.contact_sheet and sheet.exists()):
            raise ValueError("Output already exists; choose a fresh output directory.")
        report.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        if args.contact_sheet:
            contact_sheet(frames, result["frames"], sheet)
        print(json.dumps({"report": str(report.resolve()),
                          "contact_sheet": str(sheet.resolve()) if args.contact_sheet else None,
                          "frames": result["frame_count"], "cycle_ms": result["encoded_cycle_ms"],
                          "peak_ms": result["peak_time_ms"]}))
    except (OSError, ValueError) as exc:
        parser.exit(1, f"Error: {exc}\n")


if __name__ == "__main__":
    main()
