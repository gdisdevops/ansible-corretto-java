import pytest
import os
import testinfra.utils.ansible_runner


testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.fixture()
def get_vars(host):
    defaults_files = "file=../../defaults/main.yml name=role_defaults"
    vars_files = "file=../../vars/main.yml name=role_vars"

    ansible_vars = host.ansible(
        "include_vars",
        defaults_files)["ansible_facts"]["role_defaults"]

    ansible_vars.update(host.ansible(
        "include_vars",
        vars_files)["ansible_facts"]["role_vars"])

    return ansible_vars


def test_java_directory(host, get_vars):
    dir = host.file(get_vars['java_folder'])
    assert dir.exists
    assert dir.is_directory


@pytest.mark.parametrize("dirs", [
    "/usr/java",
    "/usr/lib/jvm"
])
def test_directories(host, dirs):
    d = host.file(dirs)
    assert d.exists
    assert d.is_directory


@pytest.mark.parametrize("dirs", [
    "/usr/lib/jvm/java",
    "/usr/java/default"
])
def test_symlinks(host, dirs):
    d = host.file(dirs)
    assert d.exists
    assert d.is_symlink


@pytest.mark.parametrize("files", [
    "/usr/lib/jvm/java/bin/java",
    "/etc/profile.d/java.sh",
    "/etc/ansible/facts.d/java.fact"
])
def test_files(host, files):
    f = host.file(files)
    assert f.exists
    assert f.is_file
