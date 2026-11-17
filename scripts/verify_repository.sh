#!/usr/bin/env bash
set -eu

repository_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$repository_root"

printf 'Checking required repository files...\n'
for required_path in \
  README.md \
  LICENSE \
  THIRD_PARTY.md \
  docs/PUBLISHING.md \
  docs/WORK_PLAN.md \
  schemas/scene-manifest-0.1.schema.json \
  apps/editor/UPSTREAM.md \
  services/core/pyproject.toml; do
  if [ ! -f "$required_path" ]; then
    printf 'Missing required file: %s\n' "$required_path" >&2
    exit 1
  fi
done

if [ -d experiments ] || [ -d .external ]; then
  printf 'Research-only directory found in app repository. Move it to sgd3dgs-research.\n' >&2
  exit 1
fi

printf 'Checking for accidentally tracked large files...\n'
large_files=""
while IFS= read -r -d '' path; do
  size=$(wc -c < "$path")
  if [ "$size" -gt 52428800 ]; then
    large_files="${large_files}${path}\n"
  fi
done < <(git ls-files -z)
if [ -n "$large_files" ]; then
  printf 'Tracked files larger than 50 MB found:\n%b' "$large_files" >&2
  exit 1
fi

printf 'Repository structure looks valid.\n'
