# Scripts

- `check_system.sh`: non-mutating readiness check for laptops and GPU workers.
- `uv.sh`: runs uv in a repository-local `venv/` environment. The non-dot name
  avoids a macOS/iCloud filesystem flag that can disable editable installs.
- `verify_repository.sh`: checks required files and guards against accidentally
  adding very large assets.

Scripts should be small orchestration helpers, not hidden implementations of
application behavior. Product logic belongs in `apps/editor` or `services/core`
and should be covered by tests.
