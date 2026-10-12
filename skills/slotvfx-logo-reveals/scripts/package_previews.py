#!/usr/bin/env python3
"""Validate and combine compatible silent H.264 previews without re-encoding."""

import argparse
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from fractions import Fraction
from urllib.parse import quote
import zipfile


def run(args):
    result = subprocess.run(args, capture_output=True, text=True, check=False)
    if result.returncode or result.stderr.strip():
        raise ValueError(f"{Path(args[0]).name} failed: {result.stderr.strip()}")
    return result.stdout


def inspect(path, ffprobe, fps):
    streams = json.loads(run([
        ffprobe, '-v', 'error', '-show_streams', '-show_data_hash', 'sha256',
        '-of', 'json', str(path),
    ])).get('streams', [])
    if len(streams) != 1 or streams[0].get('codec_type') != 'video':
        raise ValueError(f'{path.name}: expected one video stream and no audio/other streams')
    stream = streams[0]
    if stream.get('codec_name') != 'h264':
        raise ValueError(f'{path.name}: helper requires H.264 previews')
    for key in ('r_frame_rate', 'avg_frame_rate'):
        if Fraction(stream.get(key, '0/1')) != fps:
            raise ValueError(f'{path.name}: {key} is {stream.get(key)}, expected {fps} fps')
    frames = json.loads(run([
        ffprobe, '-v', 'error', '-select_streams', 'v:0', '-show_frames',
        '-show_entries', 'frame=best_effort_timestamp_time', '-of', 'json', str(path),
    ])).get('frames', [])
    if not frames:
        raise ValueError(f'{path.name}: no decoded video frames')
    times = [float(f['best_effort_timestamp_time']) for f in frames]
    if not all(math.isfinite(t) for t in times):
        raise ValueError(f'{path.name}: invalid frame timestamps')
    tolerance = max(0.00002, (1 / fps) * 0.002)
    if any(abs((b - a) - 1 / fps) > tolerance for a, b in zip(times, times[1:])):
        raise ValueError(f'{path.name}: frame timestamps are not a constant {fps} fps')
    signature_keys = (
        'codec_name', 'profile', 'level', 'codec_tag_string', 'width', 'height',
        'pix_fmt', 'sample_aspect_ratio', 'time_base', 'extradata_hash',
        'color_range', 'color_space', 'color_transfer', 'color_primaries',
    )
    if not stream.get('extradata_hash'):
        raise ValueError(f'{path.name}: missing codec-header hash; cannot verify stream-copy compatibility')
    return {
        'file': str(path), 'frames': len(frames), 'fps': fps,
        'duration_seconds': len(frames) / fps,
        'width': stream['width'], 'height': stream['height'],
        'signature': {key: stream.get(key) for key in signature_keys},
    }


def concat_path(path):
    value = str(path)
    if '\n' in value or '\r' in value:
        raise ValueError('Newlines in video paths are unsupported')
    return "file '" + value.replace("'", "'\\''") + "'\n"


def markdown_label(value):
    return str(value).replace('\n', ' ').replace('|', '\\|').replace('[', '\\[').replace(']', '\\]')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--fps', type=int, default=60)
    parser.add_argument('--zip', dest='archive', type=Path)
    parser.add_argument('--index', type=Path)
    parser.add_argument('--report', type=Path)
    parser.add_argument('--ffmpeg', default=shutil.which('ffmpeg'))
    parser.add_argument('--ffprobe', default=shutil.which('ffprobe'))
    args = parser.parse_args()
    if args.fps <= 0 or not args.ffmpeg or not args.ffprobe:
        parser.error('A positive fps and installed ffmpeg/ffprobe are required')
    manifest = args.manifest.resolve(strict=True)
    data = json.loads(manifest.read_text())
    clips = data.get('clips') if isinstance(data, dict) else data
    if not isinstance(clips, list) or not clips:
        parser.error('Manifest must contain a nonempty clips array')
    outputs = {'video': args.output, 'zip': args.archive, 'index': args.index, 'report': args.report}
    outputs = {key: value.resolve() for key, value in outputs.items() if value is not None}
    if len(set(outputs.values())) != len(outputs):
        parser.error('Output paths must be distinct')
    if outputs['video'].suffix.lower() != '.mp4':
        parser.error('Combined video output must use .mp4')
    for path in outputs.values():
        if path.exists():
            raise ValueError(f'Refusing to overwrite {path}')
    checks = []
    for clip in clips:
        source = Path(clip['file'])
        source = (manifest.parent / source).resolve(strict=True)
        if source in outputs.values():
            raise ValueError('An output path points to an input video')
        check = inspect(source, args.ffprobe, args.fps)
        check['name'] = str(clip.get('name') or source.stem)
        if 'expected_frames' in clip and check['frames'] != int(clip['expected_frames']):
            raise ValueError(f"{source.name}: {check['frames']} frames; expected {clip['expected_frames']}")
        if checks and check['signature'] != checks[0]['signature']:
            raise ValueError(f'{source.name}: incompatible codec settings/dimensions; explicit normalization is needed')
        checks.append(check)
    expected_frames = sum(c['frames'] for c in checks)
    with tempfile.TemporaryDirectory(prefix='slotvfx-package-', dir=manifest.parent) as temp_dir:
        temp = Path(temp_dir)
        concat = temp / 'concat.txt'
        concat.write_text(''.join(concat_path(Path(c['file'])) for c in checks))
        staged = {'video': temp / 'combined.mp4'}
        run([args.ffmpeg, '-v', 'error', '-nostdin', '-n', '-f', 'concat', '-safe', '0',
             '-i', str(concat), '-map', '0:v:0', '-c', 'copy', '-movflags', '+faststart', str(staged['video'])])
        combined = inspect(staged['video'], args.ffprobe, args.fps)
        if combined['frames'] != expected_frames:
            raise ValueError(f"Combined file has {combined['frames']} frames; expected {expected_frames}")
        run([args.ffmpeg, '-v', 'error', '-nostdin', '-xerror', '-err_detect', 'explode',
             '-i', str(staged['video']), '-map', '0:v:0', '-f', 'null', '-'])
        combined['file'] = str(outputs['video'])
        report = {'clips': checks, 'combined': combined, 'decoded_without_errors': True,
                  'stream_copy': True, 'outputs': {k: str(v) for k, v in outputs.items()}}
        if 'zip' in outputs:
            staged['zip'] = temp / 'individuals.zip'
            with zipfile.ZipFile(staged['zip'], 'w', compression=zipfile.ZIP_STORED) as archive:
                for number, check in enumerate(checks, 1):
                    slug = re.sub(r'[^A-Za-z0-9_-]+', '-', check['name']).strip('-') or 'reveal'
                    archive.write(check['file'], f'{number:02d}-{slug[:90]}.mp4')
        if 'index' in outputs:
            staged['index'] = temp / 'index.md'
            rows = ['# Reveal recordings', '',
                    f"{combined['width']} × {combined['height']} · {args.fps} fps · silent video", '',
                    '| # | Reveal | Start | Duration |', '| --- | --- | --- | --- |']
            elapsed = 0
            for number, check in enumerate(checks, 1):
                target = quote(os.path.relpath(check['file'], outputs['index'].parent), safe='/')
                start = f'{int(elapsed // 60)}:{elapsed % 60:06.3f}'
                rows.append(f"| {number} | [{markdown_label(check['name'])}]({target}) | {start} | {check['duration_seconds']:.3f} s |")
                elapsed += check['duration_seconds']
            staged['index'].write_text('\n'.join(rows) + '\n')
        if 'report' in outputs:
            staged['report'] = temp / 'verification.json'
            staged['report'].write_text(json.dumps(report, indent=2) + '\n')
        created = []
        try:
            for kind, destination in outputs.items():
                destination.parent.mkdir(parents=True, exist_ok=True)
                with destination.open('xb') as dest:
                    created.append(destination)
                    with staged[kind].open('rb') as source:
                        shutil.copyfileobj(source, dest)
        except Exception:
            for path in created:
                path.unlink(missing_ok=True)
            raise
    print(json.dumps({'clips': len(checks), 'frames': expected_frames,
                      'fps': args.fps, 'duration_seconds': expected_frames / args.fps,
                      'outputs': report['outputs']}, indent=2))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, OSError, json.JSONDecodeError) as error:
        raise SystemExit(f'Error: {error}') from error
