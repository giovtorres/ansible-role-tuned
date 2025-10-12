import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_tuned_is_installed(host):
    p = host.package("tuned")
    assert p.is_installed


def test_tuned_running_and_enabled(host):
    s = host.service("tuned")
    assert s.is_running
    assert s.is_enabled


def test_tuned_profile_file(host):
    # Rocky 10 uses /etc/tuned/profiles/, others use /etc/tuned/
    dist = host.system_info.distribution.lower()
    version = host.system_info.release

    if 'rocky' in dist and version.startswith('10'):
        profile_path = "/etc/tuned/profiles/my_custom_profile/tuned.conf"
    else:
        profile_path = "/etc/tuned/my_custom_profile/tuned.conf"

    f = host.file(profile_path)
    assert f.exists
    assert f.is_file
    assert f.user == "root"
    assert f.group == "root"
    assert f.mode == 0o644


def test_tuned_active_profile(host):
    cmd = "/usr/sbin/tuned-adm active"
    output = host.check_output(cmd)
    assert "my_custom_profile" in output
    assert "Current active profile:" in output
