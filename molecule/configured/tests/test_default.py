
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
    """ """
    cwd = os.getcwd()

    if 'group_vars' in os.listdir(cwd):
        directory = "../.."
        molecule_directory = "."
    else:
        directory = "."
        molecule_directory = f"molecule/{os.environ.get('MOLECULE_SCENARIO_NAME')}"

    return directory, molecule_directory


def read_ansible_yaml(file_name, role_name):
    """
    """
    read_file = None

    for e in ["yml", "yaml"]:
        test_file = f"{file_name}.{e}"
        if os.path.isfile(test_file):
            read_file = test_file
            break

    return f"file={read_file} name={role_name}"


@pytest.fixture()
def get_vars(host):
    """
        parse ansible variables
        - defaults/main.yml
        - vars/main.yml
        - vars/${DISTRIBUTION}.yaml
        - molecule/${MOLECULE_SCENARIO_NAME}/group_vars/all/vars.yml
    """
    base_dir, molecule_dir = base_directory()
    distribution = host.system_info.distribution
    operation_system = None

    if distribution in ['debian', 'ubuntu']:
        operation_system = "debian"
    elif distribution in ['redhat', 'ol', 'centos', 'rocky', 'almalinux']:
        operation_system = "redhat"
    elif distribution in ['arch', 'artix']:
        operation_system = f"{distribution}linux"

    # print(" -> {} / {}".format(distribution, os))
    # print(" -> {}".format(base_dir))

    file_defaults      = read_ansible_yaml(f"{base_dir}/defaults/main", "role_defaults")
    file_vars          = read_ansible_yaml(f"{base_dir}/vars/main", "role_vars")
    file_distibution   = read_ansible_yaml(f"{base_dir}/vars/{operation_system}", "role_distibution")
    file_molecule      = read_ansible_yaml(f"{molecule_dir}/group_vars/all/vars", "test_vars")
    # file_host_molecule = read_ansible_yaml("{}/host_vars/{}/vars".format(base_dir, HOST), "host_vars")

    defaults_vars      = host.ansible("include_vars", file_defaults).get("ansible_facts").get("role_defaults")
    vars_vars          = host.ansible("include_vars", file_vars).get("ansible_facts").get("role_vars")
    distibution_vars   = host.ansible("include_vars", file_distibution).get("ansible_facts").get("role_distibution")
    molecule_vars      = host.ansible("include_vars", file_molecule).get("ansible_facts").get("test_vars")
    # host_vars          = host.ansible("include_vars", file_host_molecule).get("ansible_facts").get("host_vars")

    ansible_vars = defaults_vars
    ansible_vars.update(vars_vars)
    ansible_vars.update(distibution_vars)
    ansible_vars.update(molecule_vars)
    # ansible_vars.update(host_vars)

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
