# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is an Ansible role that installs and configures the `tuned` daemon for setting system tuning profiles on Linux systems. The role supports both built-in tuned profiles and custom profiles.

## Requirements

- Ansible >= 2.16
- Molecule >= 6.0 with Podman driver
- Python >= 3.12
- Podman (for local testing)

Install dependencies:
```bash
pip install -r requirements.txt
```

## Key Commands

### Testing

**Single Distribution Testing:**
```bash
# Test with Rocky Linux 9 (default)
molecule test -s default

# Test specific distribution
MOLECULE_DISTRO=rockylinux10 molecule test -s default
MOLECULE_DISTRO=ubuntu2204 molecule test -s default

# Test with custom profile scenario
MOLECULE_DISTRO=rockylinux9 molecule test -s with_custom_profile
```

**Test All Distributions (CI/CD equivalent):**
```bash
# Sequential testing (recommended for debugging)
for distro in rockylinux9 rockylinux10 ubuntu2004 ubuntu2204 ubuntu2404; do
  for scenario in default with_custom_profile; do
    echo "Testing $distro with $scenario..."
    MOLECULE_DISTRO=$distro molecule test -s $scenario || exit 1
  done
done
```

**Other Useful Commands:**
- `molecule converge` - Create and provision test instances without destroying them
- `molecule verify` - Run test suite against existing instances
- `molecule login` - SSH into the test container
- `molecule destroy` - Destroy test instances

### Linting
- `yamllint .` - Lint YAML files (configuration in `.yamllint`)
- `ansible-lint` - Lint Ansible playbooks and roles

## Architecture

### Role Structure
- `defaults/main.yml` - Default variables for the role
- `tasks/main.yml` - Main task file that installs tuned and sets profiles
- `tasks/configure-custom-profile.yml` - Tasks for creating and activating custom tuned profiles
- `handlers/main.yml` - Handlers for service management
- `templates/custom_profile.conf.j2` - Template for generating custom tuned profile configurations
- `meta/main.yml` - Role metadata and dependencies

### Key Variables
- `tuned_active_builtin_profile` - Sets one of the built-in tuned profiles (default: "throughput-performance")
- `tuned_active_custom_profile` - Dictionary for creating custom tuned profiles with name and sections

### Testing Scenarios
- `molecule/default/` - Tests basic role functionality with built-in profiles
- `molecule/with_custom_profile/` - Tests custom profile creation and activation

### Testing Infrastructure
The project uses **Molecule with Podman driver** for testing, providing:
- **Custom systemd-enabled containers** built from Dockerfiles in `molecule/resources/images/`
- **Supported distributions**:
  - Rocky Linux 9 (EL 9) - UBI-init base
  - Rocky Linux 10 (EL 10) - UBI-init base
  - Ubuntu 20.04 LTS (Focal)
  - Ubuntu 22.04 LTS (Jammy)
  - Ubuntu 24.04 LTS (Noble)
- **Full systemd functionality** for testing service management (required for tuned daemon)
- **GitHub Actions integration** with ubuntu-24.04 runners (Podman pre-installed)
- **No external dependencies** - all container images are built locally from official base images

**Notes**:
- EL 7 removed (EOL June 2024, incompatible with modern Ansible)
- EL 8 not supported (Python 3.6 base incompatible with Ansible 2.16+)
- Rocky Linux images use UBI-init variants for optimal systemd support

### Profile Management
The role uses conditional logic to either:
1. Set a built-in profile via `tuned-adm profile <profile_name>`
2. Create a custom profile directory, template the configuration, and activate it

Custom profiles are structured with sections (main, sysctl, vm, etc.) and support hierarchical configuration through the `include` parameter.

## Troubleshooting

### Podman and systemd issues
If you encounter systemd-related errors when running locally:
- Ensure Podman is installed and configured for rootless operation
- Enable user linger: `loginctl enable-linger $USER`
- Verify cgroup v2 is enabled: `mount | grep cgroup2`

### GitHub Actions failures
- Check that systemd linger is enabled in the workflow (it is configured automatically)
- Verify container images are accessible from GitHub Container Registry