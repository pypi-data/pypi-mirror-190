[![CI Data Platform Python](https://github.com/ionos-cloud/sdk-resources/actions/workflows/ci-dataplatform-python.yml/badge.svg)](https://github.com/ionos-cloud/sdk-resources/actions/workflows/ci-dataplatform-python.yml)
[![Gitter](https://img.shields.io/gitter/room/ionos-cloud/sdk-general)](https://gitter.im/ionos-cloud/sdk-general)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=sdk-python-dataplatform&metric=alert_status)](https://sonarcloud.io/summary?id=sdk-python-dataplatform)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=sdk-python-dataplatform&metric=bugs)](https://sonarcloud.io/summary/new_code?id=sdk-python-dataplatform)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=sdk-python-dataplatform&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=sdk-python-dataplatform)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=sdk-python-dataplatform&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=sdk-python-dataplatform)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=sdk-python-dataplatform&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=sdk-python-dataplatform)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=sdk-python-dataplatform&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=sdk-python-dataplatform)
[![Release](https://img.shields.io/github/v/release/ionos-cloud/sdk-python-dataplatform.svg)](https://github.com/ionos-cloud/sdk-python-dataplatform/releases/latest)
[![Release Date](https://img.shields.io/github/release-date/ionos-cloud/sdk-python-dataplatform.svg)](https://github.com/ionos-cloud/sdk-python-dataplatform/releases/latest)
[![PyPI version](https://img.shields.io/pypi/v/ionoscloud-dataplatform)](https://pypi.org/project/ionoscloud-dataplatform/)

![Alt text](.github/IONOS.CLOUD.BLU.svg?raw=true "Title")


# Python API client for ionoscloud_dataplatform

Managed Stackable Data Platform by IONOS Cloud provides a preconfigured Kubernetes cluster
with pre-installed and managed Stackable operators. After the provision of these Stackable operators,
the customer can interact with them directly
and build his desired application on top of the Stackable Platform.

Managed Stackable Data Platform by IONOS Cloud can be configured through the IONOS Cloud API
in addition or as an alternative to the \"Data Center Designer\" (DCD).

## Getting Started

To get your DataPlatformCluster up and running, the following steps needs to be performed.

### IONOS Cloud Account

The first step is the creation of a IONOS Cloud account if not already existing.

To register a **new account** visit [cloud.ionos.com](https://cloud.ionos.com/compute/signup).

### Virtual Datacenter (VDC)

The Managed Data Stack needs a virtual datacenter (VDC) hosting the cluster.
This could either be a VDC that already exists, especially if you want to connect the managed DataPlatform
to other services already running within your VDC. Otherwise, if you want to place the Managed Data Stack in
a new VDC or you have not yet created a VDC, you need to do so.

A new VDC can be created via the IONOS Cloud API, the IONOS-CLI or the DCD Web interface.
For more information, see the [official documentation](https://docs.ionos.com/cloud/getting-started/tutorials/data-center-basics)

### Get a authentication token

To interact with this API a user specific authentication token is needed.
This token can be generated using the IONOS-CLI the following way:

```
ionosctl token generate
```

For more information [see](https://docs.ionos.com/cli-ionosctl/subcommands/authentication/token-generate)

### Create a new DataPlatformCluster

Before using Managed Stackable Data Platform, a new DataPlatformCluster must be created.

To create a cluster, use the [Create DataPlatformCluster](paths./clusters.post) API endpoint.

The provisioning of the cluster might take some time. To check the current provisioning status,
you can query the cluster by calling the [Get Endpoint](#/DataPlatformCluster/getCluster) with the cluster ID
that was presented to you in the response of the create cluster call.

### Add a DataPlatformNodePool

To deploy and run a Stackable service, the cluster must have enough computational resources. The node pool
that is provisioned along with the cluster is reserved for the Stackable operators.
You may create further node pools with resources tailored to your use-case.

To create a new node pool use the [Create DataPlatformNodepool](paths./clusters/{clusterId}/nodepools.post)
endpoint.

### Receive Kubeconfig

Once the DataPlatformCluster is created, the kubeconfig can be accessed by the API.
The kubeconfig allows the interaction with the provided cluster as with any regular Kubernetes cluster.

The kubeconfig can be downloaded with the [Get Kubeconfig](paths./clusters/{clusterId}/kubeconfig.get) endpoint
using the cluster ID of the created DataPlatformCluster.

### Create Stackable Service

To create the desired application, the Stackable service needs to be provided,
using the received kubeconfig and
[deploy a Stackable service](https://docs.stackable.tech/home/getting_started.html#_deploying_stackable_services)

## Authorization

All endpoints are secured, so only an authenticated user can access them.
As Authentication mechanism the default IONOS Cloud authentication mechanism
is used. A detailed description can be found [here](https://api.ionos.com/docs/authentication/).

### Basic-Auth

The basic auth scheme uses the IONOS Cloud user credentials in form of a Basic Authentication Header
accordingly to [RFC7617](https://datatracker.ietf.org/doc/html/rfc7617)

### API-Key as Bearer Token

The Bearer auth token used at the API-Gateway is a user related token created with the IONOS-CLI.
(See the [documentation](https://docs.ionos.com/cli-ionosctl/subcommands/authentication/token-generate) for details)
For every request to be authenticated, the token is passed as 'Authorization Bearer' header along with the request.

### Permissions and access roles

Currently, an admin can see and manipulate all resources in a contract.
A normal authenticated user can only see and manipulate resources he created.


## Components

The Managed Stackable Data Platform by IONOS Cloud consists of two components.
The concept of a DataPlatformClusters and the backing DataPlatformNodePools the cluster is build on.

### DataPlatformCluster

A DataPlatformCluster is the virtual instance of the customer services and operations running the managed Services like Stackable operators.
A DataPlatformCluster is a Kubernetes Cluster in the VDC of the customer.
Therefore, it's possible to integrate the cluster with other resources as vLANs e.G.
to shape the datacenter in the customer's need and integrate the cluster within the topology the customer wants to build.

In addition to the Kubernetes cluster a small node pool is provided which is exclusively used to run the Stackable operators.

### DataPlatformNodePool

A DataPlatformNodePool represents the physical machines a DataPlatformCluster is build on top.
All nodes within a node pool are identical in setup.
The nodes of a pool are provisioned into virtual data centers at a location of your choice
and you can freely specify the properties of all the nodes at once before creation.

Nodes in node pools provisioned by the Managed Stackable Data Platform Cloud API are readonly in the customer's VDC
and can only be modified or deleted via the API.

### References


## Overview
The IONOS Cloud SDK for Python provides you with access to the IONOS Cloud Managed Stackable Data Platform API. The client library supports both simple and complex requests. It is designed for developers who are building applications in Python. All API operations are performed over SSL and authenticated using your IONOS Cloud portal credentials. The API can be accessed within an instance running in IONOS Cloud or directly over the Internet from any application that can send an HTTPS request and receive an HTTPS response.


### Installation & Usage

**Requirements:**
- Python >= 3.5

### pip install

Since this package is hosted on [Pypi](https://pypi.org/) you can install it by using:

```bash
pip install ionoscloud-dataplatform
```

If the python package is hosted on a repository, you can install directly using:

```bash
pip install git+https://github.com/ionos-cloud/sdk-python-dataplatform.git
```

Note: you may need to run `pip` with root permission: `sudo pip install git+https://github.com/ionos-cloud/sdk-python-dataplatform.git`

Then import the package:

```python
import ionoscloud_dataplatform
```

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```bash
python setup.py install --user
```

or `sudo python setup.py install` to install the package for all users

Then import the package:

```python
import ionoscloud_dataplatform
```

> **_NOTE:_**  The Python SDK does not support Python 2. It only supports Python >= 3.5.

### Authentication

The username and password **or** the authentication token can be manually specified when initializing the SDK client:

```python
configuration = ionoscloud_dataplatform.Configuration(
                username='YOUR_USERNAME',
                password='YOUR_PASSWORD',
                token='YOUR_TOKEN'
                )
client = ionoscloud_dataplatform.ApiClient(configuration)
```

Environment variables can also be used. This is an example of how one would do that:

```python
import os

configuration = ionoscloud_dataplatform.Configuration(
                username=os.environ.get('IONOS_USERNAME'),
                password=os.environ.get('IONOS_PASSWORD'),
                token=os.environ.get('IONOS_TOKEN')
                )
client = ionoscloud_dataplatform.ApiClient(configuration)
```

**Warning**: Make sure to follow the Information Security Best Practices when using credentials within your code or storing them in a file.


### HTTP proxies

You can use http proxies by setting the following environment variables:
- `IONOS_HTTP_PROXY` - proxy URL
- `IONOS_HTTP_PROXY_HEADERS` - proxy headers

### Changing the base URL

Base URL for the HTTP operation can be changed in the following way:

```python
import os

configuration = ionoscloud_dataplatform.Configuration(
                username=os.environ.get('IONOS_USERNAME'),
                password=os.environ.get('IONOS_PASSWORD'),
                host=os.environ.get('IONOS_API_URL'),
                server_index=None,
                )
client = ionoscloud_dataplatform.ApiClient(configuration)
```

## Certificate pinning:

You can enable certificate pinning if you want to bypass the normal certificate checking procedure,
by doing the following:

Set env variable IONOS_PINNED_CERT=<insert_sha256_public_fingerprint_here>

You can get the sha256 fingerprint most easily from the browser by inspecting the certificate.


## Documentation for API Endpoints

All URIs are relative to *https://api.ionos.com/dataplatform*
<details >
    <summary title="Click to toggle">API Endpoints table</summary>


| Class | Method | HTTP request | Description |
| ------------- | ------------- | ------------- | ------------- |
| DataPlatformClusterApi | [**create_cluster**](docs/api/DataPlatformClusterApi.md#create_cluster) | **POST** /clusters | Create a DataPlatformCluster |
| DataPlatformClusterApi | [**delete_cluster**](docs/api/DataPlatformClusterApi.md#delete_cluster) | **DELETE** /clusters/{clusterId} | Delete DataPlatformCluster |
| DataPlatformClusterApi | [**get_cluster**](docs/api/DataPlatformClusterApi.md#get_cluster) | **GET** /clusters/{clusterId} | Retrieve a DataPlatformCluster |
| DataPlatformClusterApi | [**get_cluster_kubeconfig**](docs/api/DataPlatformClusterApi.md#get_cluster_kubeconfig) | **GET** /clusters/{clusterId}/kubeconfig | Read the kubeconfig |
| DataPlatformClusterApi | [**get_clusters**](docs/api/DataPlatformClusterApi.md#get_clusters) | **GET** /clusters | List DataPlatformCluster |
| DataPlatformClusterApi | [**patch_cluster**](docs/api/DataPlatformClusterApi.md#patch_cluster) | **PATCH** /clusters/{clusterId} | Partially modify a DataPlatformCluster |
| DataPlatformMetaDataApi | [**versions_get**](docs/api/DataPlatformMetaDataApi.md#versions_get) | **GET** /versions | Managed Data Stack API version |
| DataPlatformNodePoolApi | [**create_cluster_nodepool**](docs/api/DataPlatformNodePoolApi.md#create_cluster_nodepool) | **POST** /clusters/{clusterId}/nodepools | Create a DataPlatformNodePool for a distinct DataPlatformCluster |
| DataPlatformNodePoolApi | [**delete_cluster_nodepool**](docs/api/DataPlatformNodePoolApi.md#delete_cluster_nodepool) | **DELETE** /clusters/{clusterId}/nodepools/{nodepoolId} | Remove node pool from DataPlatformCluster. |
| DataPlatformNodePoolApi | [**get_cluster_nodepool**](docs/api/DataPlatformNodePoolApi.md#get_cluster_nodepool) | **GET** /clusters/{clusterId}/nodepools/{nodepoolId} | Retrieve a DataPlatformNodePool |
| DataPlatformNodePoolApi | [**get_cluster_nodepools**](docs/api/DataPlatformNodePoolApi.md#get_cluster_nodepools) | **GET** /clusters/{clusterId}/nodepools | List the DataPlatformNodePools of a  DataPlatformCluster |
| DataPlatformNodePoolApi | [**patch_cluster_nodepool**](docs/api/DataPlatformNodePoolApi.md#patch_cluster_nodepool) | **PATCH** /clusters/{clusterId}/nodepools/{nodepoolId} | Partially modify a DataPlatformNodePool |

</details>

## Documentation For Models

All URIs are relative to *https://api.ionos.com/dataplatform*
<details >
<summary title="Click to toggle">API models list</summary>

 - [AvailabilityZone](docs/models/AvailabilityZone)
 - [Cluster](docs/models/Cluster)
 - [ClusterListResponseData](docs/models/ClusterListResponseData)
 - [ClusterResponseData](docs/models/ClusterResponseData)
 - [CreateClusterProperties](docs/models/CreateClusterProperties)
 - [CreateClusterRequest](docs/models/CreateClusterRequest)
 - [CreateNodePoolProperties](docs/models/CreateNodePoolProperties)
 - [CreateNodePoolRequest](docs/models/CreateNodePoolRequest)
 - [ErrorMessage](docs/models/ErrorMessage)
 - [ErrorResponse](docs/models/ErrorResponse)
 - [MaintenanceWindow](docs/models/MaintenanceWindow)
 - [Metadata](docs/models/Metadata)
 - [NodePool](docs/models/NodePool)
 - [NodePoolListResponseData](docs/models/NodePoolListResponseData)
 - [NodePoolResponseData](docs/models/NodePoolResponseData)
 - [PatchClusterProperties](docs/models/PatchClusterProperties)
 - [PatchClusterRequest](docs/models/PatchClusterRequest)
 - [PatchNodePoolProperties](docs/models/PatchNodePoolProperties)
 - [PatchNodePoolRequest](docs/models/PatchNodePoolRequest)
 - [StorageType](docs/models/StorageType)


[[Back to API list]](#documentation-for-api-endpoints) [[Back to Model list]](#documentation-for-models)

</details>