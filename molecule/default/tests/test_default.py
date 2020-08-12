import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize('package', [
    'ferm',
    'iptables',
    'patch'
])
def test_pkg_installed(host, package):
    package = host.package(package)

    assert package.is_installed


@pytest.mark.parametrize('service', [
    'ferm'
])
def test_service_is_enabled(host, service):
    service = host.service(service)

    assert service.is_enabled


def test_config_exists(host):
    file = host.file('/etc/ferm/ferm.conf')

    assert file.exists
    assert file.user == 'root'
    assert file.group == 'root'

    print(file.content)


def test_config_is_valid(host):
    cmd = host.run('ferm --noexec /etc/ferm/ferm.conf')

    assert not cmd.rc


def test_iptables_rules(host):
    assert host.check_output('iptables --list-rules').split("\n") == [
        '-P INPUT ACCEPT',
        '-P FORWARD ACCEPT',
        '-P OUTPUT ACCEPT'
    ]
