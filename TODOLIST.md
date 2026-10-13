# TODO: Dependency Updates & Cleanup

## Phase 1 — Dependency Updates (no behavioral changes)
- [x] Update `requirements.txt` to match current ecosystem versions
- [x] Update `ansible.posix` version in both `collections.yml` files

## Phase 2 — Retire Ubuntu 20.04
- [x] Remove `Dockerfile.ubuntu2004`
- [x] Remove `focal` from `meta/main.yml`
- [x] Remove Ubuntu 20.04 from `README.md`
- [x] Update `molecule/resources/images/README.md`

## Phase 3 — Cleanup dead/legacy code
- [x] Remove `.molecule/` directory (legacy v1 artifacts)
- [x] Remove dead handler (`handlers/main.yml`)
- [x] Remove `CLAUDE.md` from `.gitignore`
- [x] Fix trailing blank line in `templates/custom_profile.conf.j2`

## Phase 4 — Logic improvements
- [x] Fix hardcoded Rocky 10 path in `tasks/configure-custom-profile.yml`
- [x] Update `with_custom_profile/tests/test_default.py` to match

## Phase 5 — Documentation / support alignment
- [x] Add AlmaLinux to `meta/main.yml`

## Phase 6 — CI
- [x] Create `.github/workflows/ci.yml`

## Phase 7 — Molecule v26 compatibility fixes (discovered during testing)
- [x] Remove `cgroupns_mode` from molecule.yml (removed from podman driver schema)
- [x] Remove `community.general.yaml` callback (removed in community.general 12+)

## Post-Review Fixes (2025-10-13)
- [x] Replace hardcoded distribution whitelist with `ansible_os_family == "RedHat"` in `tasks/configure-custom-profile.yml` (covers Oracle Linux, CentOS Stream, Fedora, etc.)
- [x] Add `changed_when: active_link.changed` to symlink task in `tasks/configure-custom-profile.yml` for proper idempotency reporting
- [x] Confirm CI workflow `.github/workflows/ci.yml` exists and is functional
- [x] Remove duplicate blank line in `templates/custom_profile.conf.j2`
- [ ] yamllint is redundant with ansible-lint's built-in yamllint rule (no action needed)
