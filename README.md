# A Command Line Interface and Python Module for cloudscale.ch

## Install

~~~
pip3 install cloudscale
~~~

## Command Line Interface

### Authentication

Using the ENV `CLOUDSCALE_API_TOKEN` variable:

~~~
export CLOUDSCALE_API_TOKEN=<your token>
cloudscale-cli flavor list
~~~

or by passing the `--api-token` parameter:

~~~
cloudscale-cli server --api-token <your_token> create ...
~~~

### Usage Examples

#### Create a Server

~~~
cloudscale-cli server create --flavor flex-2 --name my-server --image centos-7 --ssh-keys "$(cat ~/.ssh/id_rsa.pub)"
~~~

#### List all Servers

~~~
cloudscale-cli server list
~~~

#### Get Servers having the tag project=gemini

~~~
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
from cloudscale import Cloudscale, CloudscaleApiException

try:
    cloudscale = Cloudscale(api_token=api_token)
    server_group = cloudscale.server_group.get_by_uuid(uuid="5a1e5b28-d354-47a8-bfb2-01b048c20204")
    print(server_group['name'])
except CloudscaleApiException as e:
    print(e)
~~~

### Error handling
~~~python
from cloudscale import Cloudscale, CloudscaleApiException
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
