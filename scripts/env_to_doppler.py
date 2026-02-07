#!/usr/bin/env python3
"""
Scrub .env files and upload to Doppler
Works on Windows/Mac/Linux

Usage:
    python env_to_doppler.py [--project NAME] [--config CONFIG] [--dry-run]
"""

import os
import subprocess
import argparse
from pathlib import Path

SKIP_DIRS = {'node_modules', 'venv', '.venv', '__pycache__', '.git', 'dist', 'build'}

def find_env_files(root='.'):
    """Find all .env files recursively"""
    env_files = []
    for path in Path(root).rglob('*'):
        if any(skip in path.parts for skip in SKIP_DIRS):
            continue
        if path.name.endswith('.env') or path.name.startswith('.env'):
            env_files.append(path)
    return env_files

def parse_env_file(filepath):
    """Parse KEY=VALUE pairs from .env file"""
    secrets = {}
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                key, _, value = line.partition('=')
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if key and value and not value.startswith('${'):
                    secrets[key] = value
    return secrets

def upload_to_doppler(secrets, project, config, dry_run=False):
    """Upload secrets to Doppler"""
    for key, value in secrets.items():
        cmd = ['doppler', 'secrets', 'set', f'{key}={value}', 
               '--project', project, '--config', config]
        if dry_run:
            print(f"  [DRY-RUN] doppler secrets set {key}=*** --project {project} --config {config}")
        else:
            try:
                subprocess.run(cmd, check=True, capture_output=True)
                print(f"  ✓ {key}")
            except subprocess.CalledProcessError as e:
                print(f"  ✗ {key}: {e.stderr.decode()}")

def main():
    parser = argparse.ArgumentParser(description='Scrub .env files to Doppler')
    parser.add_argument('--project', '-p', default='factorylm', help='Doppler project name')
    parser.add_argument('--config', '-c', default='dev', help='Doppler config (dev/stg/prd)')
    parser.add_argument('--dry-run', '-n', action='store_true', help='Show what would be uploaded')
    parser.add_argument('--root', '-r', default='.', help='Root directory to scan')
    args = parser.parse_args()

    print(f"🔍 Scanning for .env files in {args.root}...")
    env_files = find_env_files(args.root)
    
    if not env_files:
        print("No .env files found!")
        return

    print(f"\n📄 Found {len(env_files)} .env files:")
    for f in env_files:
        print(f"  - {f}")

    all_secrets = {}
    for filepath in env_files:
        print(f"\n📦 Parsing: {filepath}")
        secrets = parse_env_file(filepath)
        for k, v in secrets.items():
            print(f"  • {k}")
            all_secrets[k] = v

    print(f"\n🔑 Total unique secrets: {len(all_secrets)}")
    
    if args.dry_run:
        print("\n[DRY-RUN MODE - not uploading]")
    else:
        confirm = input(f"\nUpload to Doppler ({args.project}/{args.config})? [y/N]: ")
        if confirm.lower() != 'y':
            print("Aborted.")
            return

    print(f"\n📤 Uploading to Doppler ({args.project}/{args.config})...")
    upload_to_doppler(all_secrets, args.project, args.config, args.dry_run)
    
    print("\n✅ Done!")

if __name__ == '__main__':
    main()
