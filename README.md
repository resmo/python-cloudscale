![license](https://img.shields.io/pypi/l/cloudscale.svg)
![python versions](https://img.shields.io/pypi/pyversions/cloudscale.svg)
![status](https://img.shields.io/pypi/status/cloudscale.svg)
[![pypi version](https://img.shields.io/pypi/v/cloudscale.svg)](https://pypi.org/project/cloudscale/)

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

Using the ENV `CLOUDSCALE_API_TOKEN` variable:

~~~shell
export CLOUDSCALE_API_TOKEN=<your token>
cloudscale-cli flavor list
~~~

or by passing the `--api-token` parameter:

~~~shell
cloudscale-cli server --api-token <your_token> create ...
~~~

## Help

See all options:

~~~shell
$ cloudscale-cli --help
Usage: cloudscale-cli [OPTIONS] COMMAND [ARGS]...

Options:
  -h, --help  Show this message and exit.

Commands:
  version
  server
  server-group
  floating-ip
  flavor
  image
  region
  network
~~~

### Usage Examples

#### Create a Server

~~~shell
cloudscale-cli server create --flavor flex-2 --name my-server --image centos-7 --ssh-keys "$(cat ~/.ssh/id_rsa.pub)"
~~~

#### List all Servers

~~~shell
cloudscale-cli server list
~~~

#### Get Servers having the tag project=gemini

~~~shell
cloudscale-cli server list --filter-tag project=gemini
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
