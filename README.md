# UnsafeOpenSSL

## Description 

In progress

## Usage

Build binary packages for all supported distributions

```
cd docker
make -j4 
cd ../packages
ls -al
```

## Customisation

Packages are built using docker containers and fpm gem.

Dockerfiles are generated using ansible and Jinja template.

To adapt to your needs please edit:
1. `docker/ansible/vars/default.yml`
2. `docker/ansible/templates/Dockerfile.j2`
3. `docker/Makefile`

Actual build is performed using `build.sh` script.

Patched sources that are actually used are located in `openssl-1.0.2i` directory.

### Ansible

To install ansible:

```
pip install ansible
```

To update dockerfiles:

```
ansible-playbook docker/ansible/dockerfiles.yml
```

