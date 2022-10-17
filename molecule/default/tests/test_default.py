
from ansible.parsing.dataloader import DataLoader
from ansible.template import Templar
import pytest
import os
import testinfra.utils.ansible_runner

import pprint
pp = pprint.PrettyPrinter()

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def base_directory():
    cwd = os.getcwd()
    pp.pprint(cwd)
    pp.pprint(os.listdir(cwd))

    if('group_vars' in os.listdir(cwd)):
        directory = "../.."
        molecule_directory = "."
    else:
        directory = "."
        molecule_directory = "molecule/{}".format(os.environ.get('MOLECULE_SCENARIO_NAME'))

    return directory, molecule_directory


@pytest.fixture()
def get_vars(host):
    """

    """
    base_dir, molecule_dir = base_directory()

    # pp.pprint(" => '{}' / '{}'".format(base_dir, molecule_dir))

    file_defaults = "file={}/defaults/main.yml name=role_defaults".format(base_dir)
    file_vars = "file={}/vars/main.yml name=role_vars".format(base_dir)
    file_molecule = "file={}/group_vars/all/vars.yml name=test_vars".format(molecule_dir)

    # pp.pprint(file_defaults)
    # pp.pprint(file_vars)
    # pp.pprint(file_molecule)

    defaults_vars = host.ansible("include_vars", file_defaults).get("ansible_facts").get("role_defaults")
    vars_vars = host.ansible("include_vars", file_vars).get("ansible_facts").get("role_vars")
    molecule_vars = host.ansible("include_vars", file_molecule).get("ansible_facts").get("test_vars")

    ansible_vars = defaults_vars
    ansible_vars.update(vars_vars)
    ansible_vars.update(molecule_vars)

    templar = Templar(loader=DataLoader(), variables=ansible_vars)
    result = templar.template(ansible_vars, fail_on_undefined=False)

    return result


def local_facts(host):
    """
    """
    facts = host.ansible("setup").get("ansible_facts", {}).get("ansible_local", {})
    # pp.pprint(facts)

    return facts


def version(host, get_vars):
    """
    """
    facts = local_facts(hosts)

    version = facts.get("java", {}).get("version", {})

    pp.pprint(version)

    if(not version):
        return -1

    major = version.get("major", -1)

    return major


def test_java_directory(host, get_vars):
    dir = host.file(get_vars.get('java_folder'))
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


def test_environment(host, get_vars):
    """
        test environment variables
    """
    content = host.file('/etc/profile.d/java.sh').content_string

    path = 'export PATH=$(path_append "${JAVA_HOME}/bin")'
    home = 'export JAVA_HOME="/usr/java/default"'
    ld_library = 'export LD_LIBRARY_PATH=$(library_path_append "${JAVA_HOME}/lib")'

    assert path in content
    assert home in content
    assert ld_library in content
