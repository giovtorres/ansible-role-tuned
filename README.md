# Ansible Role: Tuned

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
         - ansible-role-tuned

To use one of the other available built-in profiles, set the
`tuned_active_builtin_profile` variable:

    - hosts: servers
      vars:
        tuned_active_builtin_profile: "virtual-guest"
      roles:
         - ansible-role-tuned

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
        - ansible-role-tuned

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

## License

BSD
