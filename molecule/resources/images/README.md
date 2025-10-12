# Container Images for Testing

This directory contains Dockerfiles for building systemd-enabled containers used in Molecule tests.

## Available Images

- **Dockerfile.rockylinux9** - Rocky Linux 9 with systemd (EL 9) - Uses UBI-init base
- **Dockerfile.rockylinux10** - Rocky Linux 10 with systemd (EL 10) - Uses UBI-init base
- **Dockerfile.ubuntu2004** - Ubuntu 20.04 LTS with systemd
- **Dockerfile.ubuntu2204** - Ubuntu 22.04 LTS with systemd
- **Dockerfile.ubuntu2404** - Ubuntu 24.04 LTS with systemd

## Features

All containers include:
- Full systemd support with `/usr/sbin/init` or `/lib/systemd/systemd` as entrypoint
- Python 3 for Ansible compatibility
- Minimal systemd services (unnecessary services removed for container efficiency)
- Proper cgroup configuration for Podman

## Usage

These containers are automatically built by Molecule when running tests. You can specify which distro to test with the `MOLECULE_DISTRO` environment variable:

```bash
# Test with Rocky Linux 9 (default)
molecule test -s default

# Test with Rocky Linux 10
MOLECULE_DISTRO=rockylinux10 molecule test -s default

# Test with Ubuntu 20.04
MOLECULE_DISTRO=ubuntu2004 molecule test -s default

# Test with Ubuntu 22.04
MOLECULE_DISTRO=ubuntu2204 molecule test -s default

# Test with Ubuntu 24.04
MOLECULE_DISTRO=ubuntu2404 molecule test -s default
```

### Testing All Distributions

Test all distributions and scenarios (mirrors CI/CD behavior):

```bash
for distro in rockylinux9 rockylinux10 ubuntu2004 ubuntu2204 ubuntu2404; do
  for scenario in default with_custom_profile; do
    echo "Testing $distro with scenario $scenario..."
    MOLECULE_DISTRO=$distro molecule test -s $scenario || exit 1
  done
done
```

## Building Manually

You can also build the containers manually with Podman:

```bash
# Build Rocky Linux 9 image
podman build -t ansible-role-tuned-rockylinux9:latest -f Dockerfile.rockylinux9 .

# Build Ubuntu 22.04 image
podman build -t ansible-role-tuned-ubuntu2204:latest -f Dockerfile.ubuntu2204 .
```

