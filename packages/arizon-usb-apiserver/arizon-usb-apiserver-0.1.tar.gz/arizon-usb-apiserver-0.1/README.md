# ARIZON USB APIServer

An APIServer for ARIZON USB force sensors.

## Installation

Clone & `cd` into this repository then:

```shell
python setup.py install
```

Or download from PyPI:

```shell
python -m pip install arizon-usb-apiserver
## Get Started

To read the sensor locally, use this snippet:

```python
from serial import Serial
from arizon_usb_apiserver import Sensor

if __name__ == '__main__':
    conn = Serial("COM16", 115200)
    sensor = Sensor(conn)
    sensor.reset()
    while True:
        print(sensor.read_once())
```

To generate configuration from command line interaction run:

```shell
python -m arizon_usb_apiserver configure
```

To launch the apiserver, run:

```shell
python -m arizon_usb_apiserver apiserver
```

Init sensor

```shell
curl -X 'PUT' \
  'http://127.0.0.1:8080/v1/arizon/force?flag=true' \
  -H 'accept: application/json'
```

Read sensor

```shell
curl -X 'GET' \
  'http://127.0.0.1:8080/v1/arizon/force' \
  -H 'accept: application/json'
```

Shutdown sensor

```shell
curl -X 'PUT' \
  'http://127.0.0.1:8080/v1/arizon/force?flag=false' \
  -H 'accept: application/json'
```

## Generate Client

First launch the apiserver, then run `openapi-python-client`

```shell
openapi-python-client generate --url http://127.0.0.1:8080/openapi.json
rm -rf ./arizon_usb_driver/client
mv fast-api-client/fast_api_client ./arizon_usb_driver/client
rm -rf ./fast-api-client
```

## Serial Protocol

| Field        | Content |
| ------------ | ------- |
| Head         | 0xFE    |
| Status       | 1 Byte  |
| Data         | 3 Byte  |
| XOR checksum | 1 Byte  |

- Status: 4 bits of address + 4 bits represents number of digits
- Data: 3 bytes of signed integers, no digit, big-endian.
- Checksum: xor() of first 5 bytes