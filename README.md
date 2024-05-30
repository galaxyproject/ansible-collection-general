**NOTE: This branch is deprecated. Prior to the conversion of these roles to an [Ansible Collection](https://docs.ansible.com/ansible/latest/collections_guide/index.html), they were included into playbooks as a git submodule. Work continues on the [main branch](https://github.com/galaxyproject/ansible-collection-general/tree/main).**

# ansible-common-roles

A collection of simple Ansible roles for common (mostly system) tasks.

## Usage

```shell
% git submodule add https://github.com/galaxyproject/ansible-common-roles common_roles
```

Then add `roles_path = common_roles` to the `[defaults]` section of your
`ansible.cfg`.
