# hyperglass-frr

hyperglass-frr is a restful API for the FRRouting stack, for use by [hyperglass](https://github.com/checktheroads/hyperglass). hyperglass-frr ingests a HTTP POST with JSON data and constructs 1 of 5 shell commands to run based on the passed parameters. For example:

```json
{
  "query_type": "ping",
  "afi": "ipv4",
  "source": "192.0.2.1",
  "target": "1.1.1.1"
}
```

Would construct (by default) `ping -4 -c 5 -I 192.0.2.1 1.1.1.1`, execute the command, and return the output as a string. For BGP commands, FRRouting's `vtysh` is used to get the output. For example:

```json
{
  "query_type": "bgp_route",
  "afi": "ipv6",
  "target": "2606:4700:4700::/48"
}
```
Would construct (by default) `vtysh -u -c "show bgp ipv6 unicast 2606:4700:4700::/48"`, execute the command, and return the output as a string.

## Installation

Currently, hyperglass-frr has only been tested on Ubuntu Server 18.04. A sample systemd service file is included to run hyperglass-frr as a service.

### Clone the repository

```console
$ cd /opt/
$ git clone https://github.com/checktheroads/hyperglass-frr
```

### Install requirements

```console
$ cd /opt/hyperglass-frr/
$ pip3 install -r requirements.txt
```

### Create service account

```console
# useradd hyperglass-frr
# usermod -a -G frrvty hyperglass-frr
```

### Install systemd service
```console
# cp /opt/hyperglass-frr/hyperglass-frr.service.example /etc/systemd/system/hyperglass-frr.service
# systemctl daemon-reload
# systemctl enable hyperglass-frr
```

### Generate API Key
```console
$ cd /opt/hyperglass-frr
$ python3 manage.py generatekey
Your API Key is: B3K1ckWUpwNyFU1F
Your Key Hash is: $pbkdf2-sha256$29000$9T5njNFaS6lVag1B6H2vFQ$mLEbQD5kOAgjfZZ1zEVlrke6wE8vBEHzK.zI.7MOAVo
```

Copy the API Key, in this example `B3K1ckWUpwNyFU1F` and add it to `configuration.toml`:

```toml
[api]
# listen_addr = "*"
# port = 8080
key = "B3K1ckWUpwNyFU1F"
```

If needed, you can uncomment the `listen_addr` or `port` varibales if you need to define a specific listen address or TCP port for hyperglass-frr to run on. For exmaple:

```toml
[api]
listen_addr = "10.0.1.1"
port = 8001
key = "B3K1ckWUpwNyFU1F"
```

In hyperglass, configure `devices.toml` to use the Key Hash (in this example `$pbkdf2-sha256$29000$9T5njNFaS6lVag1B6H2vFQ$mLEbQD5kOAgjfZZ1zEVlrke6wE8vBEHzK.zI.7MOAVo`) as your FRRouting device's password:

```toml
[router.'router1']
address = "10.0.0.1"
asn = "65000"
src_addr_ipv4 = "192.0.2.1"
src_addr_ipv6 = "2001:db8::1"
credential = "frr_api_router1"
location = "pop1"
name = "router1.pop1"
display_name = "POP 1"
port = "8080"
type = "frr"
proxy = ""

[credential.'frr_api_router1']
username = "frr"
password = "$pbkdf2-sha256$29000$9T5njNFaS6lVag1B6H2vFQ$mLEbQD5kOAgjfZZ1zEVlrke6wE8vBEHzK.zI.7MOAVo"
```

## Start hyperglass-frr

```console
# systemctl restart hyperglass-frr
# systemctl status hyperglass-frr
```

## Test

hyperglass-frr should now be active, and you can run a simple test to verify that it is working apart from your main hyperglass implementation:

```python
import json
import requests
query = '{"query_type": "bgp_route", "afi": "ipv4", "target": "1.1.1.0/24"}'
query_json = json.dumps(query)
headers = {'Content-Type': 'application/json', 'X-API-Key': '$pbkdf2-sha256$29000$m9M6R.j9HwMgJGRs7f0/Jw$5HERwfOIn3P0U/M9t5t04SmgRmTzk3435Lr0duqz07w'}
url = "http://192.168.15.130:8080/frr"
output = requests.post(url, headers=headers, data=query_json)
print(output.text)
```
