![license](https://img.shields.io/pypi/l/cloudscale.svg)
![python versions](https://img.shields.io/pypi/pyversions/cloudscale.svg)
![status](https://img.shields.io/pypi/status/cloudscale.svg)
[![pypi version](https://img.shields.io/pypi/v/cloudscale.svg)](https://pypi.org/project/cloudscale/)
![PyPI - Downloads](https://img.shields.io/pypi/dw/cloudscale)
[![codecov](https://codecov.io/gh/resmo/python-cloudscale/branch/master/graph/badge.svg)](https://codecov.io/gh/resmo/python-cloudscale)



# Cloudscale

A [cloudscale.ch](https://www.cloudscale.ch) API client for Python3 and your command line.

## Install / Update

~~~
pip3 install -U cloudscale --user
export PATH=$PATH:$HOME/.local/bin
cloudscale-cli version
~~~

## Command Line Interface

### Autocompletion

zsh:
~~~shell
eval "$(_CLOUDSCALE_CLI_COMPLETE=source_zsh cloudscale-cli)"
~~~

bash:
~~~shell
eval "$(_CLOUDSCALE_CLI_COMPLETE=source cloudscale-cli)"
~~~

### Authentication

#### Evironment variable

Using the ENV `CLOUDSCALE_API_TOKEN` variable:

~~~shell
export CLOUDSCALE_API_TOKEN=<your token>
cloudscale-cli flavor list
~~~

#### Command line argument

Passing the `--api-token` parameter:

~~~shell
cloudscale-cli server --api-token <your_token> create ...
~~~

#### Config file

Creating an ini file `.cloudscale.ini` (leading dot) in your `$HOME` or a `cloudscale.ini` (without leading dot) in the `CWD` with the following schema:

~~~ini
[default]
api_token = <token>
~~~

The default profile taken if available is `default`. The profile can be chosen by passing `--profile` or `CLOUDSCALE_PROFILE` ENV variable.

~~~
export CLOUDSCALE_PROFILE=staging
~~~

~~~ini
[production]
api_token = <token>

[staging]
api_token = <token>
~~~

Passing the command line option will overwrite the ENV var as one would expect:
~~~
cloudscale-cli server --profile production list
~~~

## Help

See all options:

~~~shell
 $ cloudscale-cli
Usage: cloudscale-cli [OPTIONS] COMMAND [ARGS]...

Options:
  -h, --help  Show this message and exit.

Commands:
  flavor
  floating-ip
  image
  network
  objects-user
  region
  server
  server-group
  subnet
  version
  volume
~~~

### Usage Examples

#### Create a server

~~~shell
cloudscale-cli server create --flavor flex-2 --name my-server --image centos-7 --ssh-key "$(cat ~/.ssh/id_rsa.pub)"
~~~

#### List all servers

~~~shell
cloudscale-cli server list
~~~

#### List servers having the tag project with value gemini

~~~shell
cloudscale-cli server list --filter-tag project=gemini
~~~

#### List servers having a tag project

~~~shell
cloudscale-cli server list --filter-tag project
~~~

#### Update servers tags (but keep all existing)

~~~shell
cloudscale-cli server update <uuid> --tag project=apollo --tag stage=prod
~~~

#### Update server tags, remove a specific tag key

~~~shell
cloudscale-cli server update <uuid> --tag project=apollo --tag stage=prod --clear-tag status
~~~

#### Update server tags, remove other tags

~~~shell
cloudscale-cli server update <uuid> --tag project=apollo --tag stage=prod --clear-all-tags
~~~

#### Stop a server

~~~shell
cloudscale-cli server stop <uuid>
~~~

#### Start a server

~~~shell
cloudscale-cli server start <uuid>
~~~

## Usage in Python

### List the slug of all flavors
~~~python
import os
from cloudscale import Cloudscale, CloudscaleApiException

api_token = os.getenv('CLOUDSCALE_API_TOKEN')

cloudscale = Cloudscale(api_token=api_token)
flavors = cloudscale.flavor.get_all()
for flavor in flavors:
    print(flavor['slug'])
~~~

### Print the server names of running servers
~~~python
import os
from cloudscale import Cloudscale, CloudscaleApiException

api_token = os.getenv('CLOUDSCALE_API_TOKEN')

cloudscale = Cloudscale(api_token=api_token)
servers = cloudscale.server.get_all()
for server in servers:
    if server['status'] == "running":
        print(server['name'])
~~~

### Print the server names of all servers having a specifc tag project
~~~python
import os
from cloudscale import Cloudscale, CloudscaleApiException

api_token = os.getenv('CLOUDSCALE_API_TOKEN')

cloudscale = Cloudscale(api_token=api_token)
servers = cloudscale.server.get_all(filter_tag='project')
for server in servers:
    print(server['name'])
~~~

### Print the server names of all servers having a specifc tag project with value apollo
~~~python
import os
from cloudscale import Cloudscale, CloudscaleApiException

api_token = os.getenv('CLOUDSCALE_API_TOKEN')

cloudscale = Cloudscale(api_token=api_token)
servers = cloudscale.server.get_all(filter_tag='project=apollo')
for server in servers:
    print(server['name'])
~~~

### Get resource by UUID
~~~python
import os
from cloudscale import Cloudscale, CloudscaleApiException

api_token = os.getenv('CLOUDSCALE_API_TOKEN')

try:
    cloudscale = Cloudscale(api_token=api_token)
    server_group = cloudscale.server_group.get_by_uuid(uuid="5a1e5b28-d354-47a8-bfb2-01b048c20204")
    print(server_group['name'])
except CloudscaleApiException as e:
    print(e)
~~~

### Error handling
~~~python
import os
from cloudscale import Cloudscale, CloudscaleApiException

api_token = os.getenv('CLOUDSCALE_API_TOKEN')

try:
    cloudscale = Cloudscale(api_token=api_token)
    server = cloudscale.server.get_by_uuid(uuid="does-not-exist")
    print(server['name'])
except CloudscaleApiException as e:
    # Prints "API Response Error (404): Not found."
    print(e)
    # Prints "404"
    print(e.status_code)
    # Prints raw API response
    print(e.response)
~~~

## Development

### Run tests with coverage
~~~shell
tox -e coverage
~~~
