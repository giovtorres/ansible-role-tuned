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


def test_tuned_active_profile(host):
    cmd = "/usr/sbin/tuned-adm active"
    assert "throughput-performance" in host.check_output(cmd)


def test_tuned_verify(host):
    cmd = host.run("/usr/sbin/tuned-adm verify")
    assert cmd.rc == 0
    assert "Verfication succeeded" in cmd.stdout
