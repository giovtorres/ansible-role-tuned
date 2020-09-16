# Ansible Role: Tuned

[![Build Status](https://travis-ci.org/giovtorres/ansible-role-tuned.svg?branch=master)](https://travis-ci.org/giovtorres/ansible-role-tuned)
[![Ansible Role](https://img.shields.io/ansible/role/19447.svg)](https://galaxy.ansible.com/giovtorres/tuned/)

Installs and configures the tuned daemon for setting system tuning profiles.
Supported on EL7.

## Requirements

None.

## Role Variables

The available built-in profiles on EL7 are:

- balanced
- desktop
- latency-performance
- network-latency
- network-throughput
- powersave
- throughput-performance
- virtual-guest
- virtual-host

Change the active tuned profile using one of the built-in profiles above:

    tuned_active_builtin_profile: "throughput-performance"

Change the active tuned profile by creating a custom tuned profile.  *See
example below on how to build a custom tuned profile*:

    tuned_active_custom_profile: ""

## Dependencies

None.

## Example Playbooks

To use the role's default profile, `throughput-performance`, just apply the
role:

    - hosts: servers
      roles:
         - giovtorres.tuned

To use one of the other available built-in profiles, set the
`tuned_active_builtin_profile` variable:

    - hosts: servers
      vars:
        tuned_active_builtin_profile: "virtual-guest"
      roles:
         - giovtorres.tuned

To build a custom profile, create a dictionary using the
`tuned_active_custom_profile` variable with the **name** and **sections**
items, where **sections** contains the name of the section in the config file
and a list of option/value pairs that go into that given section.

    - hosts: all
      vars:
        tuned_active_custom_profile:
          name: my_custom_profile
          sections:
            - name: main
              params:
                - option: summary
                  value: Test
                - option: include
                  value: throughput-performance
            - name: sysctl
              params:
                - option: vm.dirty_ratio
                  value: 30
                - option: vm.swappiness
                  value: 30
            - name: vm
              params:
                - option: transparent_hugepages
                  value: never
      roles:
        - giovtorres.tuned

The above playbook results in the following configuration output:

```ini
[main]
summary=Test
include=throughput-performance

[sysctl]
vm.dirty_ratio=30
vm.swappiness=30

[vm]
transparent_hugepages=never
```

### Exam Playbook with a script

To build a custom profile, create a dictionary using the
`tuned_active_custom_profile` variable with the **name** and **sections**
items, where **sections** contains the name of the section in the config file
and a list of option/value pairs that go into that given section. A script can
be added to this profile by using a section named `script`. This section contains
two params, the first param is used to define the name of script (a file with this name)
will be created under the directory of this profile. The second param is the content of
the script and will be skipped in the profile configuration

    - hosts: all
      vars:
        tuned_active_custom_profile:
          name: my_custom_profile_and_script
          sections:
            - name: main
              params:
                - option: summary
                  value: Test
                - option: include
                  value: throughput-performance
            - name: sysctl
              params:
                - option: vm.dirty_ratio
                  value: 30
                - option: vm.swappiness
                  value: 30
            - name: vm
              params:
                - option: transparent_hugepages
                  value: never
            - name: script
              params:
                - option: script
                  value: script.sh
                - option: content
                  value: |-
                    #!/bin/sh

                    . /usr/lib/tuned/functions

                    start() {
                        echo never > /sys/kernel/mm/transparent_hugepage/defrag
                        return 0
                    }

                    stop() {
                        return 0
                    }

                    process $@
                  enabled: false

      roles:
        - giovtorres.tuned

The above playbook results in the following configuration output:

```ini
[main]
summary=Test
include=throughput-performance

[sysctl]
vm.dirty_ratio=30
vm.swappiness=30

[vm]
transparent_hugepages=never

[script]
script=script.sh
```

## License

BSD
