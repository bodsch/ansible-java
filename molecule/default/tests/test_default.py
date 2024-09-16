
from ansible.parsing.dataloader import DataLoader
from ansible.template import Templar

import json
import pytest
import os

import testinfra.utils.ansible_runner


testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def pp_json(json_thing, sort=True, indents=2):
    if type(json_thing) is str:
        print(json.dumps(json.loads(json_thing), sort_keys=sort, indent=indents))
    else:
        print(json.dumps(json_thing, sort_keys=sort, indent=indents))
    return None


def base_directory():
    cwd = os.getcwd()

    if ('group_vars' in os.listdir(cwd)):
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
    distribution = host.system_info.distribution

    if distribution in ['debian', 'ubuntu']:
        os = "debian"
    elif distribution in ['redhat', 'ol', 'centos', 'rocky', 'almalinux']:
        os = "redhat"
    elif distribution in ['arch']:
        os = "archlinux"

    print(" -> {} / {}".format(distribution, os))

    file_defaults = "file={}/defaults/main.yml name=role_defaults".format(base_dir)
    file_vars = "file={}/vars/main.yml name=role_vars".format(base_dir)
    file_molecule = "file={}/group_vars/all/vars.yml name=test_vars".format(molecule_dir)
    file_distibution = "file={}/vars/{}.yaml name=role_distibution".format(base_dir, os)

    defaults_vars = host.ansible("include_vars", file_defaults).get("ansible_facts").get("role_defaults")
    vars_vars = host.ansible("include_vars", file_vars).get("ansible_facts").get("role_vars")
    distibution_vars = host.ansible("include_vars", file_distibution).get("ansible_facts").get("role_distibution")
    molecule_vars = host.ansible("include_vars", file_molecule).get("ansible_facts").get("test_vars")

    ansible_vars = defaults_vars
    ansible_vars.update(vars_vars)
    ansible_vars.update(distibution_vars)
    ansible_vars.update(molecule_vars)

    templar = Templar(loader=DataLoader(), variables=ansible_vars)
    result = templar.template(ansible_vars, fail_on_undefined=False)

    return result


def java_fact(host):
    """
    """
    return host.ansible("setup").get("ansible_facts", {}).get("ansible_local", {}).get("java", {})


def install_path(host, version):
    """
        return install path for version
    """
    fact = java_fact(host)
    return fact.get(version, {}).get('install_path')


def all_versions(host):
    """
        return version from ansible fact
    """
    fact = java_fact(host)
    return list(fact.keys())


@pytest.mark.parametrize("dirs", [
    "/opt/java",
])
def test_directories(host, dirs):
    """
      test array of directories
    """
    d = host.file(dirs)
    assert d.is_directory


@pytest.mark.parametrize("files", [
    "/etc/ansible/facts.d/java.fact"
])
def test_files(host, files):
    """
      test array of files
    """
    f = host.file(files)
    assert f.is_file


def test_jdk_path(host, get_vars):
    """
      test existing jdk path and files into bin directory
    """
    versions = all_versions(host)

    for version in versions:
        p = install_path(host, version)

        d = host.file(p)
        assert d.is_directory

        files = [
            'profile.sh',
            'bin/java']

        #    'bin/javap',
        #    'bin/javac',
        #    'bin/jcmd',
        #    'bin/jconsole',
        #    'bin/jdb',
        #    'bin/jdeps',
        #    'bin/jinfo',
        #    'bin/jarsigner',
        #    'bin/jmap'
        #    'bin/jar',

        for i in files:
            fl = f"{p}/{i}"
            f = host.file(fl)
            assert f.is_file


def test_installed_versions(host, get_vars):
    """
      test version between ansible facts and configured
    """
    wanted_versions = get_vars.get('java_versions')
    versions = all_versions(host)
    fact = java_fact(host)

    for version in versions:
        major_version = fact.get(version, {}).get('major_version')
        # pp.pprint(major_version)
        assert major_version in wanted_versions


def test_environment(host, get_vars):
    """
      test environment variables
    """
    versions = all_versions(host)

    for version in versions:
        p = install_path(host, version)

        content = host.file(f'{p}/profile.sh').content_string

        # path = 'PATH="${{PATH:+${{PATH}}:}}${{JAVA_HOME}}/bin"'
        home = f'export JAVA_HOME="{p}"'

        # assert path in content
        assert home in content
