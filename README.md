# Traffic Generator Service with iperf3

## Introduction
A traffic generator can generate traffic over a network, with the purpose of:
* simulating load on a network
* measuring the network's capabilities (bandwidth, packet loss, etc.)

We created a Service that is orchestratable by a MANO platform, specifically the [ETSI Open Source MANO](https://osm.etsi.org/) and it uses Virtual Machines. A container-based version is in development, but it isn't ready yet. 
The descriptors found here can be used with OSM up to version 8, but simple translation into formats used by later OSM versions will lead to correct deployment.

The image used is a simple Ubuntu 18.04 cloud image, but this was used for demo purposes. Other images can be used as well with proper modification of the cloud-init for different distros.

The proposed Traffic Generator Service is based on the [iperf3](https://iperf.fr/) software. 

## Implementation
The traffic generator architecture requires a client, which acts as the traffic sender, and a server, which acts as the traffic receiver.

The Service is implemented as two separate Network Services, one for the client and one for the server, in order to offer more flexibility to the Service owner, in case multiple clients are required to be placed at multiple parts of the network to measure different network links.

The client can then initiate the generation of traffic at any point after the client's successful deployment, using OSM's mechanism for day-2 (after deployment) actions. This is done with the use of [Juju charms](https://osm.etsi.org/docs/user-guide/latest/05-osm-usage.html?highlight=charms#understanding-day-1-and-day-2-operations).

## Orchestration
The services can be orchestrated using the descriptors in the respective directory in the repository. The initial configuration commands for each component can be seen in the cloud-init file of each VNF descriptor. 

### Server
During the server's service deployment, the iperf3 software is installed and an instance of iperf3 starts listening for traffic on the port 5201 by default. 

### Client
During the client's service deployment, the iperf3 software is installed and no further action is taken. At any point after the service's successful deployment, it is possible to trigger the generation of traffic towards the server using OSM's juju charms. This is done either via OSM's CLI or UI as shown in OSM's charm usage [documetnation](https://osm.etsi.org/docs/user-guide/latest/05-osm-usage.html?highlight=charms#understanding-day-1-and-day-2-operations).

## Parameters
The traffic generation can be triggered with the parameters seen below:
* **gateway:** IP address of the default gateway to be set before traffic generation [Optional]
* **server_ip:** IP address of the iperf3 server [Mandatory]
* **mode:** possible vaslues are udp or UDP, if something else is given or if "mode" not present the traffic defaults to TCP [Optional]
* **bandwidth:** bandwidth to use, example "200", if not present the default target bandwidth for UDP connections is 1Mbps, and the default target bandwidth for TCP connections is unlimited [Optional]
* **duration:** time in seconds to run the traffic generation, example "60", if not present, defaults to 10s [Optional]
* **direction:** possible values are ul or UL/dl or DL, determines whether traffic is uplink or downlink relative to the client, default is downlink (from server to client) [Optional]
