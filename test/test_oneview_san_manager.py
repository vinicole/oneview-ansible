#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2016-2017) Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###

from ansible.compat.tests import unittest, mock
from oneview_module_loader import SanManagerModule
from hpe_test_utils import OneViewBaseTestCase

FAKE_MSG_ERROR = 'Fake message error'

DEFAULT_SAN_MANAGER_TEMPLATE = dict(
    name='172.18.15.1',
    providerDisplayName='Brocade Network Advisor',
    uri='/rest/fc-sans/device-managers/UUU-AAA-BBB',
    refreshState='OK',
    connectionInfo=[
        {
            'valueFormat': 'IPAddressOrHostname',
            'displayName': 'Host',
            'name': 'Host',
            'valueType': 'String',
            'required': False,
            'value': '172.18.15.1'
        }]
)


class SanManagerModuleSpec(unittest.TestCase,
                           OneViewBaseTestCase):
    PARAMS_FOR_PRESENT = dict(
        config='config.json',
        state='present',
        data=DEFAULT_SAN_MANAGER_TEMPLATE
    )

    PARAMS_FOR_CONNECTION_INFORMATION_SET = dict(
        config='config.json',
        state='connection_information_set',
        data=DEFAULT_SAN_MANAGER_TEMPLATE.copy()
    )

    PARAMS_WITH_CHANGES = dict(
        config='config.json',
        state='present',
        data=dict(name=DEFAULT_SAN_MANAGER_TEMPLATE['name'],
                  refreshState='RefreshPending')
    )

    PARAMS_FOR_ABSENT = dict(
        config='config.json',
        state='absent',
        data=dict(name=DEFAULT_SAN_MANAGER_TEMPLATE['name'])
    )

    def setUp(self):
        self.configure_mocks(self, SanManagerModule)
        self.resource = self.mock_ov_client.san_managers

    def test_should_add_new_san_manager(self):
        self.resource.get_by_name.return_value = []
        self.resource.get_provider_uri.return_value = '/rest/fc-sans/providers/123/device-managers'
        self.resource.add.return_value = DEFAULT_SAN_MANAGER_TEMPLATE

        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT

        SanManagerModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=SanManagerModule.MSG_CREATED,
            ansible_facts=dict(san_manager=DEFAULT_SAN_MANAGER_TEMPLATE)
        )

    def test_should_find_provider_uri_to_add(self):
        self.resource.get_by_name.return_value = []
        self.resource.get_provider_uri.return_value = '/rest/fc-sans/providers/123/device-managers'
        self.resource.add.return_value = DEFAULT_SAN_MANAGER_TEMPLATE

        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT

        SanManagerModule().run()

        provider_display_name = DEFAULT_SAN_MANAGER_TEMPLATE['providerDisplayName']
        self.resource.get_provider_uri.assert_called_once_with(provider_display_name)

    def test_should_not_update_when_data_is_equals(self):
        self.resource.get_by_name.return_value = DEFAULT_SAN_MANAGER_TEMPLATE
        self.resource.get_provider_uri.return_value = '/rest/fc-sans/providers/123/device-managers'

        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT

        SanManagerModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=SanManagerModule.MSG_ALREADY_PRESENT,
            ansible_facts=dict(san_manager=DEFAULT_SAN_MANAGER_TEMPLATE)
        )

    def test_update_when_data_has_modified_attributes(self):
        data_merged = DEFAULT_SAN_MANAGER_TEMPLATE.copy()
        data_merged['fabricType'] = 'DirectAttach'

        self.resource.get_by_name.return_value = DEFAULT_SAN_MANAGER_TEMPLATE
        self.resource.get_provider_uri.return_value = '/rest/fc-sans/providers/123/device-managers'

        self.resource.update.return_value = data_merged
        self.mock_ansible_module.params = self.PARAMS_WITH_CHANGES

        SanManagerModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=SanManagerModule.MSG_UPDATED,
            ansible_facts=dict(san_manager=data_merged)
        )

    def test_update_should_not_send_connection_info_when_not_informed_on_data(self):
        merged_data = DEFAULT_SAN_MANAGER_TEMPLATE.copy()
        merged_data['refreshState'] = 'RefreshPending'

        self.resource.get_by_name.return_value = DEFAULT_SAN_MANAGER_TEMPLATE
        self.resource.get_provider_uri.return_value = '/rest/fc-sans/providers/123/device-managers'

        self.resource.update.return_value = merged_data
        self.mock_ansible_module.params = self.PARAMS_WITH_CHANGES

        SanManagerModule().run()

        self.resource.update.assert_called_once_with(resource=merged_data, id_or_uri=merged_data['uri'])

    def test_should_remove_san_manager(self):
        self.resource.get_by_name.return_value = DEFAULT_SAN_MANAGER_TEMPLATE
        self.resource.get_provider_uri.return_value = '/rest/fc-sans/providers/123/device-managers'

        self.mock_ansible_module.params = self.PARAMS_FOR_ABSENT.copy()

        SanManagerModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=SanManagerModule.MSG_DELETED
        )

    def test_should_do_nothing_when_san_manager_not_exist(self):
        self.resource.get_by_name.return_value = []

        self.mock_ansible_module.params = self.PARAMS_FOR_ABSENT.copy()

        SanManagerModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=False,
            msg=SanManagerModule.MSG_ALREADY_ABSENT
        )

    def test_should_fail_when_name_not_found(self):
        self.resource.get_by_name.return_value = []
        self.resource.get_provider_uri.return_value = None

        self.mock_ansible_module.params = self.PARAMS_FOR_PRESENT

        SanManagerModule().run()

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg="The provider 'Brocade Network Advisor' was not found.")

    def test_should_fail_when_name_and_hosts_in_connectionInfo_missing(self):
        bad_params = self.PARAMS_FOR_PRESENT.copy()
        bad_params['data'] = self.PARAMS_FOR_PRESENT['data'].copy()
        bad_params['data'].pop('name')
        bad_params['data'].pop('connectionInfo')

        self.mock_ansible_module.params = bad_params

        SanManagerModule().run()

        msg = 'A "name" or "connectionInfo" must be provided inside the "data" field for this operation. '
        msg += 'If a "connectionInfo" is provided, the "Host" name is considered as the "name" for the resource.'

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg=msg)

    def test_connection_information_set_should_set_the_connection_information(self):
        data_merged = DEFAULT_SAN_MANAGER_TEMPLATE.copy()
        data_merged['fabricType'] = 'DirectAttach'

        self.resource.get_by_name.return_value = DEFAULT_SAN_MANAGER_TEMPLATE
        self.resource.get_provider_uri.return_value = '/rest/fc-sans/providers/123/device-managers'

        self.resource.update.return_value = data_merged
        self.mock_ansible_module.params = self.PARAMS_FOR_CONNECTION_INFORMATION_SET

        SanManagerModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=SanManagerModule.MSG_UPDATED,
            ansible_facts=dict(san_manager=data_merged)
        )

    def test_should_add_new_san_manager_when_connection_information_set_called_without_resource(self):
        self.resource.get_by_name.return_value = []
        self.resource.get_provider_uri.return_value = '/rest/fc-sans/providers/123/device-managers'
        self.resource.add.return_value = DEFAULT_SAN_MANAGER_TEMPLATE

        self.mock_ansible_module.params = self.PARAMS_FOR_CONNECTION_INFORMATION_SET

        SanManagerModule().run()

        self.mock_ansible_module.exit_json.assert_called_once_with(
            changed=True,
            msg=SanManagerModule.MSG_CREATED,
            ansible_facts=dict(san_manager=DEFAULT_SAN_MANAGER_TEMPLATE)
        )

    def test_should_fail_when_required_attribute_missing(self):
        bad_params = self.PARAMS_FOR_CONNECTION_INFORMATION_SET.copy()
        bad_params['data'] = self.PARAMS_FOR_CONNECTION_INFORMATION_SET['data'].copy()
        bad_params['data'].pop('connectionInfo')

        self.resource.get_by_name.return_value = DEFAULT_SAN_MANAGER_TEMPLATE
        self.resource.get_provider_uri.return_value = '/rest/fc-sans/providers/123/device-managers'

        self.mock_ansible_module.params = bad_params

        SanManagerModule().run()

        msg = 'A connectionInfo field is required for this operation.'

        self.mock_ansible_module.fail_json.assert_called_once_with(exception=mock.ANY, msg=msg)


if __name__ == '__main__':
    unittest.main()
