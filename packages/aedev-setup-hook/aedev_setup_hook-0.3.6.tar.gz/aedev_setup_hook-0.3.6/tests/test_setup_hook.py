""" unit tests for aedev.setup_hook portion. """
import os
import pytest

from ae.base import PY_EXT, TESTS_FOLDER, in_wd
from aedev.setup_hook import NAMESPACE_EXTEND_ENTRY_POINT, hooked_project_env_vars, pev_update_hook
from aedev.setup_project import project_env_vars


@pytest.fixture
def ext_ns_file():
    """ prepare NAMESPACE_EXTEND_ENTRY_POINT and remove after test """
    mod_name, func_name = NAMESPACE_EXTEND_ENTRY_POINT.split(':')
    hook_file = os.path.join(TESTS_FOLDER, mod_name + PY_EXT)
    assert not os.path.exists(hook_file), f"TEST RUN PREVENTED TO OVERWRITE {hook_file}"
    file_handle = open(hook_file, 'w')
    file_handle.write(f"""def {func_name}(pev):\n    """)

    yield file_handle

    os.remove(hook_file)


class TestProjectEnvVars:
    """ test project_env_vars() function """
    def test_declaration(self):
        assert NAMESPACE_EXTEND_ENTRY_POINT == 'setup_hooks:extend_project_env_vars'

    def test_add_env_hooked(self, ext_ns_file):
        test_env_key = 'test_env_key'
        test_env_val = 'test_env_val'
        ext_ns_file.write(f"""pev['{test_env_key}'] = '{test_env_val}'\n""")
        ext_ns_file.close()

        pev = hooked_project_env_vars(TESTS_FOLDER)

        assert test_env_key in pev
        assert pev[test_env_key] == test_env_val

    def test_add_env_explicit_hook(self, ext_ns_file):
        test_env_key = 'test_env_key'
        test_env_val = 'test_env_val'
        ext_ns_file.write(f"""pev['{test_env_key}'] = '{test_env_val}'\n""")
        ext_ns_file.close()

        pev = project_env_vars(TESTS_FOLDER)
        pev['NAMESPACE_EXTEND_ENTRY_POINT'] = NAMESPACE_EXTEND_ENTRY_POINT

        with in_wd(TESTS_FOLDER):
            if pev_update_hook(pev):   # skip tests directly after upgrade of ae.setup and not yet deployed
                assert test_env_key in pev
                assert pev[test_env_key] == test_env_val

    def test_change_env(self, ext_ns_file):
        test_env_val = 'test_env_val'
        ext_ns_file.write(f"""pev['install_require'].append('{test_env_val}')\n""")
        ext_ns_file.close()

        pev = hooked_project_env_vars(TESTS_FOLDER)

        install_req_len = len(pev['install_require'])
        assert install_req_len >= 1
        assert test_env_val in pev['install_require']
        assert pev['install_require'].count(test_env_val) == 1

        with in_wd(TESTS_FOLDER):
            assert pev_update_hook(pev)
        assert len(pev['install_require']) == install_req_len + 1
        assert pev['install_require'].count(test_env_val) == 2

    def test_change_env_double(self, ext_ns_file):
        test_val = 'test_env_val'
        redirected_hook = NAMESPACE_EXTEND_ENTRY_POINT + '2'
        ext_ns_file.write(f"""pev['NAMESPACE_EXTEND_ENTRY_POINT'] = '{redirected_hook}'""")
        ext_ns_file.write(f"""\n\n""")
        ext_ns_file.write(f"""def extend_project_env_vars2(pev):\n    pev['install_require'].append('{test_val}')""")
        ext_ns_file.close()

        pev = hooked_project_env_vars(TESTS_FOLDER)

        assert test_val in pev['install_require']
        assert pev['install_require'].count(test_val) == 1
