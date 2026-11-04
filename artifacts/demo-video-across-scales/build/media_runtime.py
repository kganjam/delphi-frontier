"""Shared fonts, input pins and directly capped media processes."""
from functools import lru_cache
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

from PIL import ImageFont


def sha256_file(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def resolve_pin(root, pin):
    relative = Path(pin['path'])
    if relative.is_absolute() or '..' in relative.parts:
        raise ValueError(f'Asset path must stay inside its source directory: {relative}')
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()) or not path.is_file():
        raise ValueError(f'Missing or escaping asset: {relative}')
    return path


def check_pin(root, pin):
    path = resolve_pin(root, pin)
    if path.stat().st_size != pin['bytes'] or sha256_file(path) != pin['sha256']:
        raise ValueError(f'Asset bytes do not match their pin: {pin["path"]}')
    return path


def load_assets(manifest_path):
    manifest = json.loads(manifest_path.read_text())
    if manifest.get('schema') != 'delphi-bio.video-assets/1':
        raise ValueError('Unsupported asset map')
    sources, posters = {}, {}
    for name, pin in manifest['assets'].items():
        sources[name] = resolve_pin(manifest_path.parent, pin)
        if 'poster' in pin:
            posters[name] = resolve_pin(manifest_path.parent, pin['poster'])
        elif sources[name].suffix == '.mp4':
            raise ValueError(f'Video {name} needs an explicit pinned preview poster')
    return manifest['assets'], sources, posters


def process_command(program, arguments=(), memory_mib=768):
    executable = shutil.which(program)
    if not executable:
        raise RuntimeError(f'{program} is required on PATH')
    if sys.platform == 'darwin':
        wrapper = shutil.which('taskpolicy')
        if not wrapper:
            raise RuntimeError('macOS taskpolicy is required for the memory cap')
        prefix = [wrapper, '-m', str(memory_mib)]
    elif sys.platform.startswith('linux'):
        wrapper = shutil.which('systemd-run')
        if not wrapper:
            raise RuntimeError('Linux requires systemd-run and a working user manager for bounded processes')
        prefix = [wrapper, '--user', '--scope', '--quiet', '-p',
                  f'MemoryMax={memory_mib}M', '-p', 'MemorySwapMax=0',
                  '-p', 'TasksMax=32']
    else:
        raise RuntimeError('Resource caps are configured for macOS and Linux only')
    return [*prefix, executable, *map(str, arguments)]


def ffmpeg_command(arguments, loglevel='error'):
    return process_command('ffmpeg', ['-v', loglevel, '-y', '-threads', '2',
        '-filter_threads', '1', '-filter_complex_threads', '1',
        '-filter_buffered_frames', '24', *arguments])


def probe(path):
    command = process_command('ffprobe', ['-v', 'error', '-show_streams',
        '-show_format', '-of', 'json', path], memory_mib=256)
    return json.loads(subprocess.check_output(command))


class Fonts:
    """Licensed system fonts are external inputs, never bundled silently."""
    def __init__(self, config_path=None):
        if config_path is None and os.environ.get('DELPHI_VIDEO_FONT_CONFIG'):
            config_path = Path(os.environ['DELPHI_VIDEO_FONT_CONFIG']).expanduser()
        if config_path is None:
            if sys.platform != 'darwin':
                raise RuntimeError('Supply --font-config with legally available font paths; see build/README.md')
            config_path = Path(__file__).with_name('font-config.example.json')
        config_path = Path(config_path).resolve()
        self.records = json.loads(config_path.read_text())
        for record in self.records.values():
            path = Path(os.path.expandvars(record['path'])).expanduser()
            if not path.is_absolute():
                path = config_path.parent / path
            if not path.is_file():
                raise RuntimeError(f'Font unavailable: {path}. Supply --font-config; font binaries are not redistributed.')
            record['path'] = str(path.resolve())

    @lru_cache(maxsize=128)
    def get(self, size, bold=False, serif=False, italic=False):
        key = 'serif' if serif else 'sans'
        if bold:
            key += '_bold'
        if italic:
            key += '_italic'
        record = self.records[key]
        return ImageFont.truetype(record['path'], size, index=record.get('index', 0))

    def pins(self):
        return {name: {'filename': Path(r['path']).name,
                      'index': r.get('index', 0),
                      'sha256': sha256_file(r['path'])}
                for name, r in self.records.items()}
