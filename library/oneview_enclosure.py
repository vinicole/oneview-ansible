#!/usr/bin/python
# -*- coding: utf-8 -*-
###
# Copyright (2016-2020) Hewlett Packard Enterprise Development LP
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

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['stableinterface'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: oneview_enclosure
short_description: Manage OneView Enclosure resources.
description:
    - Provides an interface to manage Enclosure resources.
version_added: "2.3"
requirements:
    - "python >= 2.7.9"
    - "hpeOneView >= 5.0.0"
author: "Mariana Kreisig (@marikrg)"
options:
    state:
      description:
        - Indicates the desired state for the Enclosure resource.
          C(present) will ensure data properties are compliant with OneView. You can rename the enclosure providing an
          attribute C(newName). You can also rename the rack providing an attribute C(rackName).
          C(absent) will remove the resource from OneView, if it exists.
          C(reconfigured) will reapply the appliance's configuration on the enclosure. This includes
          running the same configuration steps that were performed as part of the enclosure add.
          C(refreshed) will refresh the enclosure along with all of its components, including interconnects and
          servers. Any new hardware is added, and any hardware that is no longer present within the enclosure is
          removed.
          C(appliance_bays_powered_on) will set the appliance bay power state on.
          C(uid_on) will set the UID state on.
          C(uid_off) will set the UID state off.
          C(manager_bays_uid_on) will set the UID state on for the Synergy Frame Link Module.
          C(manager_bays_uid_off) will set the UID state off for the Synergy Frame Link Module.
          C(manager_bays_power_state_e_fuse) will E-Fuse the Synergy Frame Link Module bay in the path.
          C(manager_bays_power_state_reset) will Reset the Synergy Frame Link Module bay in the path.
          C(appliance_bays_power_state_e_fuse) will E-Fuse the appliance bay in the path.
          C(device_bays_power_state_e_fuse) will E-Fuse the device bay in the path.
          C(device_bays_power_state_reset) will Reset the device bay in the path.
          C(interconnect_bays_power_state_e_fuse) will E-Fuse the IC bay in the path.
          C(manager_bays_role_active) will set the active Synergy Frame Link Module.
          C(device_bays_ipv4_removed) will release the IPv4 address in the device bay.
          C(interconnect_bays_ipv4_removed) will release the IPv4 address in the interconnect bay.
          C(support_data_collection_set) will set the support data collection state for the enclosure. The supported
          values for this state are C(PendingCollection), C(Completed), C(Error) and C(NotSupported)
          C(create_certificate_request) will create a Certificate Signing Request (CSR) for an enclosure
          C(get_certificate_request) will return an enclosure's Certificate Signing Request (CSR) that was generated by previous
          POST to same URI.
          C(import_certificate_request) will import a signed server certificate into the enclosure to be used for secure communication
          with the appliance.
      choices: [
        'present', 'absent', 'reconfigured', 'refreshed', 'appliance_bays_powered_on', 'uid_on', 'uid_off',
        'manager_bays_uid_on', 'manager_bays_uid_off', 'manager_bays_power_state_e_fuse',
        'manager_bays_power_state_reset', 'appliance_bays_power_state_e_fuse', 'device_bays_power_state_e_fuse',
        'device_bays_power_state_reset', 'interconnect_bays_power_state_e_fuse', 'manager_bays_role_active',
        'device_bays_ipv4_removed', 'interconnect_bays_ipv4_removed', 'support_data_collection_set', 'create_certificate_request',
        'get_certificate_request', 'import_certificate_request'
        ]
    data:
      description:
        - List with the Enclosure properties.
      required: true
notes:
    - "These states are only available on HPE Synergy: C(appliance_bays_powered_on), C(uid_on), C(uid_off),
      C(manager_bays_uid_on), C(manager_bays_uid_off), C(manager_bays_power_state_e_fuse),
      C(manager_bays_power_state_reset), C(appliance_bays_power_state_e_fuse), C(device_bays_power_state_e_fuse),
      C(device_bays_power_state_reset), C(interconnect_bays_power_state_e_fuse), C(manager_bays_role_active),
      C(device_bays_ipv4_removed) and C(interconnect_bays_ipv4_removed)"

extends_documentation_fragment:
    - oneview
'''

EXAMPLES = '''
- name: Ensure that an Enclosure is present using the default configuration
  oneview_enclosure:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1600
    state: present
    data:
      enclosureGroupUri : '{{ enclosure_group_uri }}'
      hostname : '{{ enclosure_hostname }}'
      username : '{{ enclosure_username }}'
      password : '{{ enclosure_password }}'
      name: 'Test-Enclosure'
      licensingIntent : 'OneView'

- name: Updates the enclosure to have a name of "Test-Enclosure-Renamed".
  oneview_enclosure:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1600
    state: present
    data:
      name: 'Test-Enclosure'
      newName : 'Test-Enclosure-Renamed'

- name: Reconfigure the enclosure "Test-Enclosure"
  oneview_enclosure:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1600
    state: reconfigured
    data:
      name: 'Test-Enclosure'

- name: Ensure that enclosure is absent
  oneview_enclosure:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1600
    state: absent
    data:
      name: 'Test-Enclosure'

- name: Ensure that an enclosure is refreshed
  oneview_enclosure:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1600
    state: refreshed
    data:
      name: 'Test-Enclosure'
      refreshState: Refreshing

- name: Create certificate signing request
  oneview_enclosure:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1600
    state: create_certificate_request
    data:
      name: 'Test-Enclosure'
      type: CertificateDtoV2
      organization: HPE
      organizationalUnit: IT
      locality: 'Fort Collins'
      state: Colorado
      country: US
      commonName: 'e10-oa'
    bay_number: 1

- name: Get certificate signing request
  oneview_enclosure:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1600
    state: get_certificate_request
    data:
      name: 'Test-Enclosure'
      bay_number: 1

- name: Import certificate signing request
  oneview_enclosure:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1600
    state: import_certificate_request
    data:
      name: 'Test-Enclosure'
      type: CertificateDtoV2
      base64Data: certificate

- name: Set the calibrated max power of an unmanaged or unsupported enclosure
  oneview_enclosure:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1600
    state: present
    data:
      name: 'Test-Enclosure'
      calibratedMaxPower: 1700

- name: Set the appliance bay power state on
  oneview_enclosure:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1600
    state: appliance_bays_powered_on
    data:
      name: 'Test-Enclosure'
      bayNumber: 1

- name: Set the appliance UID state on
  oneview_enclosure:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1600
    state: uid_on
    data:
      name: 'Test-Enclosure'

- name: Set the appliance UID state off
  oneview_enclosure:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1600
    state: uid_off
    data:
      name: 'Test-Enclosure'

- name: Set the UID for the Synergy Frame Link Module state on
  oneview_enclosure:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1600
    state: manager_bays_uid_on
    data:
      name: 'Test-Enclosure'
      bayNumber: 1

- name: Set the UID for the Synergy Frame Link Module state off
  oneview_enclosure:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1600
    state: manager_bays_uid_off
    data:
      name: 'Test-Enclosure'
      bayNumber: 1

- name: E-Fuse the Synergy Frame Link Module bay 1
  oneview_enclosure:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1600
    state: manager_bays_power_state_e_fuse
    data:
      name: 'Test-Enclosure'
      bayNumber: 1

- name: Reset the Synergy Frame Link Module bay 1
  oneview_enclosure:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1600
    state: manager_bays_power_state_reset
    data:
      name: 'Test-Enclosure'
      bayNumber: 1

- name: E-Fuse the appliance bay 1
  oneview_enclosure:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1600
    state: appliance_bays_power_state_e_fuse
    data:
      name: 'Test-Enclosure'
      bayNumber: 1

- name: E-Fuse the device bay 10
  oneview_enclosure:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1600
    state: device_bays_power_state_e_fuse
    data:
      name: 'Test-Enclosure'
      bayNumber: 10

- name: Reset the device bay 8
  oneview_enclosure:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1600
    state: device_bays_power_state_reset
    data:
      name: 'Test-Enclosure'
      bayNumber: 8

- name: E-Fuse the IC bay 3
  oneview_enclosure:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1600
    state: interconnect_bays_power_state_e_fuse
    data:
      name: 'Test-Enclosure'
      bayNumber: 3

- name: Set the active Synergy Frame Link Module on bay 2
  oneview_enclosure:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1600
    state: manager_bays_role_active
    data:
      name: 'Test-Enclosure'
      bayNumber: 2

- name: Release IPv4 address in the bay 2
  oneview_enclosure:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1600
    state: device_bays_ipv4_removed
    data:
      name: 'Test-Enclosure'
      bayNumber: 2

- name: Release IPv4 address in the bay 2
  oneview_enclosure:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1600
    state: interconnect_bays_ipv4_removed
    data:
      name: 'Test-Enclosure'
      bayNumber: 2

- name: Set the supportDataCollectionState for the enclosure
  oneview_enclosure:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1600
    state: support_data_collection_set
    data:
      name: 'Test-Enclosure'
      supportDataCollectionState: 'PendingCollection'

- name: Ensure that the Enclosure is present and is inserted in the desired scopes
  oneview_enclosure:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 1600
    state: present
    data:
      name: 'Test-Enclosure'
      scopeUris:
        - '/rest/scopes/00SC123456'
        - '/rest/scopes/01SC123456'
'''

RETURN = '''
enclosure:
    description: Has all the facts about the enclosure.
    returned: On states 'present', 'reconfigured', and 'refreshed'. Can be null.
    type: dict
'''

from ansible.module_utils.oneview import (OneViewModule,
                                          OneViewModuleResourceNotFound,
                                          OneViewModuleValueError)


class EnclosureModule(OneViewModule):
    MSG_DELETED = 'Enclosure removed successfully.'
    MSG_ALREADY_ABSENT = 'Enclosure is already absent.'
    MSG_CREATED = 'Enclosure added successfully.'
    MSG_UPDATED = 'Enclosure updated successfully.'
    MSG_ALREADY_PRESENT = 'Enclosure is already present.'
    MSG_RECONFIGURED = 'Enclosure reconfigured successfully.'
    MSG_REFRESHED = 'Enclosure refreshed successfully.'
    MSG_ENCLOSURE_NOT_FOUND = 'Enclosure not found.'
    MSG_APPLIANCE_BAY_ALREADY_POWERED_ON = 'The device in specified bay is already powered on.'
    MSG_APPLIANCE_BAY_POWERED_ON = 'Appliance bay power state set to on successfully.'
    MSG_UID_ALREADY_POWERED_ON = 'UID state is already On.'
    MSG_UID_POWERED_ON = 'UID state set to On successfully.'
    MSG_UID_ALREADY_POWERED_OFF = 'UID state is already Off.'
    MSG_UID_POWERED_OFF = 'UID state set to Off successfully.'
    MSG_MANAGER_BAY_UID_ON = 'UID for the Synergy Frame Link Module set to On successfully.'
    MSG_MANAGER_BAY_UID_ALREADY_ON = 'The UID for the Synergy Frame Link Module is already On.'
    MSG_BAY_NOT_FOUND = 'Bay not found.'
    MSG_MANAGER_BAY_UID_ALREADY_OFF = 'The UID for the Synergy Frame Link Module is already Off.'
    MSG_MANAGER_BAY_UID_OFF = 'UID for the Synergy Frame Link Module set to Off successfully.'
    MSG_MANAGER_BAY_POWER_STATE_E_FUSED = 'E-Fuse the Synergy Frame Link Module bay in the path.'
    MSG_MANAGER_BAY_POWER_STATE_RESET = 'Reset the Synergy Frame Link Module bay in the path.'
    MSG_APPLIANCE_BAY_POWER_STATE_E_FUSED = 'E-Fuse the appliance bay in the path.'
    MSG_DEVICE_BAY_POWER_STATE_E_FUSED = 'E-Fuse the device bay in the path.'
    MSG_DEVICE_BAY_POWER_STATE_RESET = 'Reset the device bay in the path.'
    MSG_INTERCONNECT_BAY_POWER_STATE_E_FUSE = 'E-Fuse the IC bay in the path.'
    MSG_MANAGER_BAY_ROLE_ACTIVE = 'Set the active Synergy Frame Link Module.'
    MSG_DEVICE_BAY_IPV4_SETTING_REMOVED = 'Release IPv4 address in the device bay.'
    MSG_INTERCONNECT_BAY_IPV4_SETTING_REMOVED = 'Release IPv4 address in the interconnect bay'
    MSG_SUPPORT_DATA_COLLECTION_STATE_SET = 'Support data collection state set.'
    MSG_SUPPORT_DATA_COLLECTION_STATE_ALREADY_SET = \
        'The support data collection state is already set with the desired value.'
    MSG_GET_CERTIFICATE_REQUEST = 'Saved CSR(generated by previous POST) to "enclosure.csr" file'
    MSG_CREATE_CERTIFICATE_REQUEST = 'Created certificate signing request successfully'
    MSG_IMPORT_CERTIFICATE_REQUEST = 'Signed Certificate imported successfully'
    MSG_ENCLOSURE_REQUIRED_FIELDS = \
        'Required hostname to add an enclosure, hostname/name of existing enclosure for other operations'
    argument_spec = dict(
        state=dict(
            required=True,
            choices=[
                'present',
                'absent',
                'reconfigured',
                'refreshed',
                'appliance_bays_powered_on',
                'uid_on',
                'uid_off',
                'manager_bays_uid_on',
                'manager_bays_uid_off',
                'manager_bays_power_state_e_fuse',
                'manager_bays_power_state_reset',
                'appliance_bays_power_state_e_fuse',
                'device_bays_power_state_e_fuse',
                'device_bays_power_state_reset',
                'interconnect_bays_power_state_e_fuse',
                'manager_bays_role_active',
                'device_bays_ipv4_removed',
                'interconnect_bays_ipv4_removed',
                'support_data_collection_set',
                'create_certificate_request',
                'get_certificate_request',
                'import_certificate_request'
            ]
        ),
        data=dict(required=True, type='dict')
    )

    patch_params = dict(
        appliance_bays_powered_on=dict(operation='replace', path='/applianceBays/{bayNumber}/power', value='On'),
        uid_on=dict(operation='replace', path='/uidState', value='On'),
        uid_off=dict(operation='replace', path='/uidState', value='Off'),
        manager_bays_uid_on=dict(operation='replace', path='/managerBays/{bayNumber}/uidState', value='On'),
        manager_bays_uid_off=dict(operation='replace', path='/managerBays/{bayNumber}/uidState', value='Off'),
        manager_bays_power_state_e_fuse=dict(operation='replace', path='/managerBays/{bayNumber}/bayPowerState',
                                             value='E-Fuse'),
        manager_bays_power_state_reset=dict(operation='replace', path='/managerBays/{bayNumber}/bayPowerState',
                                            value='Reset'),
        appliance_bays_power_state_e_fuse=dict(operation='replace', path='/applianceBays/{bayNumber}/bayPowerState',
                                               value='E-Fuse'),
        device_bays_power_state_e_fuse=dict(operation='replace', path='/deviceBays/{bayNumber}/bayPowerState',
                                            value='E-Fuse'),
        device_bays_power_state_reset=dict(operation='replace', path='/deviceBays/{bayNumber}/bayPowerState',
                                           value='Reset'),
        interconnect_bays_power_state_e_fuse=dict(operation='replace',
                                                  path='/interconnectBays/{bayNumber}/bayPowerState', value='E-Fuse'),
        manager_bays_role_active=dict(operation='replace', path='/managerBays/{bayNumber}/role', value='active'),
        device_bays_ipv4_removed=dict(operation='remove', path='/deviceBays/{bayNumber}/ipv4Setting', value=''),
        interconnect_bays_ipv4_removed=dict(operation='remove', path='/interconnectBays/{bayNumber}/ipv4Setting',
                                            value=''),
    )

    patch_messages = dict(
        appliance_bays_powered_on=dict(changed=MSG_APPLIANCE_BAY_POWERED_ON,
                                       not_changed=MSG_APPLIANCE_BAY_ALREADY_POWERED_ON),
        uid_on=dict(changed=MSG_UID_POWERED_ON, not_changed=MSG_UID_ALREADY_POWERED_ON),
        uid_off=dict(changed=MSG_UID_POWERED_OFF, not_changed=MSG_UID_ALREADY_POWERED_OFF),
        manager_bays_uid_on=dict(changed=MSG_MANAGER_BAY_UID_ON, not_changed=MSG_MANAGER_BAY_UID_ALREADY_ON),
        manager_bays_uid_off=dict(changed=MSG_MANAGER_BAY_UID_OFF, not_changed=MSG_MANAGER_BAY_UID_ALREADY_OFF),
        manager_bays_power_state_e_fuse=dict(changed=MSG_MANAGER_BAY_POWER_STATE_E_FUSED),
        manager_bays_power_state_reset=dict(changed=MSG_MANAGER_BAY_POWER_STATE_RESET),
        appliance_bays_power_state_e_fuse=dict(changed=MSG_APPLIANCE_BAY_POWER_STATE_E_FUSED),
        device_bays_power_state_e_fuse=dict(changed=MSG_DEVICE_BAY_POWER_STATE_E_FUSED),
        device_bays_power_state_reset=dict(changed=MSG_DEVICE_BAY_POWER_STATE_RESET),
        interconnect_bays_power_state_e_fuse=dict(changed=MSG_INTERCONNECT_BAY_POWER_STATE_E_FUSE),
        manager_bays_role_active=dict(changed=MSG_MANAGER_BAY_ROLE_ACTIVE),
        device_bays_ipv4_removed=dict(changed=MSG_DEVICE_BAY_IPV4_SETTING_REMOVED),
        interconnect_bays_ipv4_removed=dict(changed=MSG_INTERCONNECT_BAY_IPV4_SETTING_REMOVED),
    )

    def __init__(self):
        super(EnclosureModule, self).__init__(additional_arg_spec=self.argument_spec,
                                              validate_etag_support=True)
        self.set_resource_object(self.oneview_client.enclosures)

    def execute_module(self):
        if self.state == 'present':
            changed, msg, resource = self.__present()
        elif self.state == 'absent':
            return self.resource_absent('remove')
        else:
            if not self.current_resource:
                raise OneViewModuleResourceNotFound(self.MSG_ENCLOSURE_NOT_FOUND)

            if self.state == 'reconfigured':
                changed, msg, resource = self.__reconfigure()
            elif self.state == 'refreshed':
                changed, msg, resource = self.__refresh()
            elif self.state == 'support_data_collection_set':
                changed, msg, resource = self.__support_data_collection_set()
            elif self.state == 'create_certificate_request':
                changed, msg, resource = self.__create_certificate_request()
            elif self.state == 'get_certificate_request':
                changed, msg, resource = self.__get_certificate_request()
            elif self.state == 'import_certificate_request':
                changed, msg, resource = self.__import_certificate_request()
            else:
                changed, msg, resource = self.__patch()

        return dict(changed=changed,
                    msg=msg,
                    ansible_facts=dict(enclosure=resource))

    def __present(self):
        changed = False
        message = self.MSG_ALREADY_PRESENT

        configuration_data = self.data.copy()
        name = configuration_data.pop('newName', configuration_data.pop('name', None))
        rack_name = configuration_data.pop('rackName', None)
        calibrated_max_power = configuration_data.pop('calibratedMaxPower', None)
        scope_uris = configuration_data.pop('scopeUris', None)

        if 'hostname' in self.data:
            resource_by_hostname = self.resource_client.get_by_hostname(self.data['hostname'])
            if not resource_by_hostname:
                self.current_resource = self.resource_client.add(configuration_data)
                message = self.MSG_CREATED
                changed = True
            else:
                self.current_resource = resource_by_hostname

        if not self.current_resource:
            raise OneViewModuleValueError(self.MSG_ENCLOSURE_REQUIRED_FIELDS)

        if self.__name_has_changes(name):
            self.__replace_enclosure_name(name)
            changed = True
            message = self.MSG_UPDATED

        if self.__rack_name_has_changes(rack_name):
            self.__replace_enclosure_rack_name(rack_name)
            changed = True
            message = self.MSG_UPDATED

        if calibrated_max_power:
            self.__set_calibrated_max_power(calibrated_max_power)
            changed = True
            message = self.MSG_UPDATED

        resource = self.current_resource.data

        if scope_uris is not None:
            state = {'ansible_facts': {'enclosure': self.current_resource.data},
                     'changed': changed, 'msg': message}
            result = self.resource_scopes_set(state, 'enclosure', scope_uris)
            resource = result['ansible_facts']['enclosure']
            changed = result['changed']
            message = result['msg']

        return changed, message, resource

    def __reconfigure(self):
        reconfigured_enclosure = self.current_resource.update_configuration()
        return True, self.MSG_RECONFIGURED, reconfigured_enclosure

    def __refresh(self):
        refresh_config = self.data.copy()
        refresh_config.pop('name', None)

        self.current_resource.refresh_state(refresh_config)
        self.current_resource.refresh()  # Get updated data

        return True, self.MSG_REFRESHED, self.current_resource.data

    def __support_data_collection_set(self):
        current_value = self.current_resource.data.get('supportDataCollectionState')
        desired_value = self.data.get('supportDataCollectionState')

        if current_value != desired_value:
            updated_resource = self.current_resource.patch(operation='replace',
                                                           path='/supportDataCollectionState',
                                                           value=desired_value)
            return True, self.MSG_SUPPORT_DATA_COLLECTION_STATE_SET, updated_resource.data

        return False, self.MSG_SUPPORT_DATA_COLLECTION_STATE_ALREADY_SET, self.current_resource.data

    def __patch(self):
        changed = False
        state_name = self.module.params['state']
        state = self.patch_params[state_name].copy()
        property_current_value = self.__get_current_property_value(state_name, state)

        if self.__is_update_needed(state_name, state, property_current_value):
            resource_obj = self.current_resource.patch(**state)
            resource = resource_obj.data
            changed = True
        else:
            resource = self.current_resource.data

        msg = self.patch_messages[state_name]['changed'] if changed else self.patch_messages[state_name]['not_changed']

        return changed, msg, resource

    def __is_update_needed(self, state_name, state, property_current_value):
        need_request_update = False
        if state['value'] in ['E-Fuse', 'Reset', 'active']:
            need_request_update = True
        elif state['operation'] == 'remove':
            need_request_update = True
        elif state_name == 'appliance_bays_powered_on':
            if not property_current_value:
                need_request_update = True
        elif property_current_value != state['value']:
            need_request_update = True

        return need_request_update

    def __get_current_property_value(self, state_name, state):
        property_name = state['path'].split('/')[1]
        sub_property_name = state['path'].split('/')[-1]

        if sub_property_name == property_name:
            sub_property_name = None

        if state_name == 'appliance_bays_powered_on':
            sub_property_name = 'poweredOn'

        filter_ = set(self.data.keys()) - set(["name"])
        if filter_:
            filter_ = filter_.pop()

        property_current_value = None

        if filter_:
            sub_resource = None
            if self.current_resource.data.get(property_name):
                sub_resource = next(
                    (item for item in self.current_resource.data[property_name]
                        if str(item[filter_]) == str(self.data[filter_])), None)

            if not sub_resource:
                # Resource doesn't have that property or subproperty
                raise OneViewModuleResourceNotFound(self.MSG_BAY_NOT_FOUND)

            property_current_value = sub_resource.get(sub_property_name)
            state['path'] = state['path'].format(**self.data)

        else:
            property_current_value = self.current_resource.data[property_name]

        return property_current_value

    def __name_has_changes(self, name):
        return name and self.current_resource.data['name'] != name

    def __rack_name_has_changes(self, rack_name):
        return rack_name and self.current_resource.data.get('rackName', None) != rack_name

    def __replace_enclosure_name(self, name):
        self.current_resource.patch('replace', '/name', name)

    def __replace_enclosure_rack_name(self, rack_name):
        self.current_resource.patch('replace', '/rackName', rack_name)

    def __set_calibrated_max_power(self, calibrated_max_power):
        body = {"calibratedMaxPower": calibrated_max_power}
        self.current_resource.update_environmental_configuration(body)

    def __create_certificate_request(self):
        csr_data = self.data.copy()
        bay_number = csr_data.pop('bay_number', None)
        create_csr = self.current_resource.generate_csr(csr_data, bay_number)
        return True, self.MSG_CREATE_CERTIFICATE_REQUEST, create_csr

    def __get_certificate_request(self):
        bay_number = self.data.pop('bay_number', None)
        get_csr = self.current_resource.get_csr(bay_number)
        return True, self.MSG_GET_CERTIFICATE_REQUEST, get_csr

    def __import_certificate_request(self):
        csr_data = self.data.copy()
        bay_number = csr_data.pop('bay_number', None)
        import_csr = self.current_resource.import_certificate(csr_data, bay_number)
        return True, self.MSG_IMPORT_CERTIFICATE_REQUEST, import_csr


def main():
    EnclosureModule().run()


if __name__ == '__main__':
    main()
