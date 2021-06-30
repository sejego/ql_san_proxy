# Launch Manual

This launch manual will guide you through launching correctly the proxy server. There are 2 ways to launch the proxy, either by downloading the source code or by running a Docker image.

ql_san_proxy server is a simple proxy server used to translate OPIL SAN entities that are present in Orion Context Broker to NGSI entities readable by FIWARE QuantumLeap. FIWARE QuantumLeap has a specific format that it "understands". To make use of QuantumLeap and software like Grafana, a translator is needed to convert these entities. The created entities will have a **_ql** postfix in **entity id** and **entity type**.

**NB! ql_san_proxy works only with digital sensor entities!**

More about:
* [OPIL](http://www.l4ms.eu/OPIL)
* [FIWARE](https://www.fiware.org/)

## Prerequisites
Make sure you have the following things downloaded:

1. Docker 
2. [Orion Context Broker](https://fiware-orion.readthedocs.io/en/master/)

Next, make sure that Orion Context Broker is up and running.

# Running from source

Clone the git repo available [here](https://github.com/sejego/ql_san_proxy)

Open the repo in the terminal and write 
```
python3 qlProxy.py
```

# Running a Docker image

## Building an image

1. Make sure you have created a folder with the necessary files, such as:
* config.json
* Dockerfile

### config file
config file must be a *config.json* file in the same repository as the *Dockerfile*

config.json has the following structure:


```json
{
    "context-broker":
    {
        "ocb_ip": "192.168.1.102",
        "ocb_port": 1026
    },

    "ql_proxy":
    {
        "proxy_ip": "0.0.0.0",
        "proxy_port": 4440
    }
}
```
**DO NOT MODIFY proxy_ip** 

Modify the Orion CB IP and port to the ones that it uses on your machine.

In case you need to user another port - modify the port in *config.json* before building the image.

### Dockerfile used in this image

```Dockerfile
FROM sejego/ql_san_proxy:latest
COPY config.json /app
WORKDIR /app
EXPOSE 4440
CMD python qlProxy.py
```
In case you will use another port, substitute the port *4440* with the desired one.
## Build an image

Use the following command to build your image:

```
docker build -t qlproxy .
```
Make sure you are executing this command while being in the same folder where these files are located. You can change the name *qlproxy* with any other name, this name is later used to run the container.
## Running the proxy server

use this command to run the image

```
sudo docker run --rm -it --name ql_san_proxy -p 192.168.1.102:4440:4440 qlproxy
```
instead of *192.168.1.102*- local ip of the machine (**can be anything but localhost or 0.0.0.0**). By default proxy runs on port *4440*, but if your machines are occupying these ports, substitute the *4440* port with the desired port (both in this command and in *config.json*)

Make sure that the IP's are correct. Currently proxy *must run on 0.0.0.0*.

## Closing the proxy
Simply use Ctrl+C to exit the proxy. Proxy will do the needed cleanup in Orion CB.

If something gone wrong upon cancellation - refer to techniques on container and image removal provided by Docker.

## Building the image from source code
In case you have made modifications to source code, then building an image would look something like this:

### Dockerfile
```
FROM python:3.5.2
COPY /ql_san_proxy/. /app
COPY requirements.txt /app
COPY config.json /app
WORKDIR /app
EXPOSE 4440
RUN pip install -r requirements.txt
CMD python qlProxy.py

```

### requirements.txt content
```
requests==2.23.0
httpserver==1.1.0
```

## Subscribe proxy server to receive notifications about SensorAgent changes

use the following payload to POST to Orion CB subscriptions

```json
{
  "description": "Notify QL Proxy Server about changes in SensorAgent",
  "subject": {
    "entities": [
      {
        "idPattern": ".*",
        "type": "SensorAgent"
      }
    ],
    "condition": {
      "attrs": []
    }
  },
  "notification": {
    "http": {
      "url": "http://ipaddress:4440"
    },
    "attrs": [],
	"metadata": ["dateCreated", "dateModified"]
  }
}
```

In place of *http://ipaddress:4440* put the url of proxy server