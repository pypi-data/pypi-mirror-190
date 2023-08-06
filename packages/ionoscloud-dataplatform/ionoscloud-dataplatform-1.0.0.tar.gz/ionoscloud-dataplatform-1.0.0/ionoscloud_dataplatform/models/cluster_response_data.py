# coding: utf-8

"""
    IONOS Cloud - Managed Stackable Data Platform API

    Managed Stackable Data Platform by IONOS Cloud provides a preconfigured Kubernetes cluster with pre-installed and managed Stackable operators. After the provision of these Stackable operators, the customer can interact with them directly and build his desired application on top of the Stackable Platform.  Managed Stackable Data Platform by IONOS Cloud can be configured through the IONOS Cloud API in addition or as an alternative to the \"Data Center Designer\" (DCD).  ## Getting Started  To get your DataPlatformCluster up and running, the following steps needs to be performed.  ### IONOS Cloud Account  The first step is the creation of a IONOS Cloud account if not already existing.  To register a **new account** visit [cloud.ionos.com](https://cloud.ionos.com/compute/signup).  ### Virtual Datacenter (VDC)  The Managed Data Stack needs a virtual datacenter (VDC) hosting the cluster. This could either be a VDC that already exists, especially if you want to connect the managed DataPlatform to other services already running within your VDC. Otherwise, if you want to place the Managed Data Stack in a new VDC or you have not yet created a VDC, you need to do so.  A new VDC can be created via the IONOS Cloud API, the IONOS-CLI or the DCD Web interface. For more information, see the [official documentation](https://docs.ionos.com/cloud/getting-started/tutorials/data-center-basics)  ### Get a authentication token  To interact with this API a user specific authentication token is needed. This token can be generated using the IONOS-CLI the following way:  ``` ionosctl token generate ```  For more information [see](https://docs.ionos.com/cli-ionosctl/subcommands/authentication/token-generate)  ### Create a new DataPlatformCluster  Before using Managed Stackable Data Platform, a new DataPlatformCluster must be created.  To create a cluster, use the [Create DataPlatformCluster](paths./clusters.post) API endpoint.  The provisioning of the cluster might take some time. To check the current provisioning status, you can query the cluster by calling the [Get Endpoint](#/DataPlatformCluster/getCluster) with the cluster ID that was presented to you in the response of the create cluster call.  ### Add a DataPlatformNodePool  To deploy and run a Stackable service, the cluster must have enough computational resources. The node pool that is provisioned along with the cluster is reserved for the Stackable operators. You may create further node pools with resources tailored to your use-case.  To create a new node pool use the [Create DataPlatformNodepool](paths./clusters/{clusterId}/nodepools.post) endpoint.  ### Receive Kubeconfig  Once the DataPlatformCluster is created, the kubeconfig can be accessed by the API. The kubeconfig allows the interaction with the provided cluster as with any regular Kubernetes cluster.  The kubeconfig can be downloaded with the [Get Kubeconfig](paths./clusters/{clusterId}/kubeconfig.get) endpoint using the cluster ID of the created DataPlatformCluster.  ### Create Stackable Service  To create the desired application, the Stackable service needs to be provided, using the received kubeconfig and [deploy a Stackable service](https://docs.stackable.tech/home/getting_started.html#_deploying_stackable_services)  ## Authorization  All endpoints are secured, so only an authenticated user can access them. As Authentication mechanism the default IONOS Cloud authentication mechanism is used. A detailed description can be found [here](https://api.ionos.com/docs/authentication/).  ### Basic-Auth  The basic auth scheme uses the IONOS Cloud user credentials in form of a Basic Authentication Header accordingly to [RFC7617](https://datatracker.ietf.org/doc/html/rfc7617)  ### API-Key as Bearer Token  The Bearer auth token used at the API-Gateway is a user related token created with the IONOS-CLI. (See the [documentation](https://docs.ionos.com/cli-ionosctl/subcommands/authentication/token-generate) for details) For every request to be authenticated, the token is passed as 'Authorization Bearer' header along with the request.  ### Permissions and access roles  Currently, an admin can see and manipulate all resources in a contract. A normal authenticated user can only see and manipulate resources he created.   ## Components  The Managed Stackable Data Platform by IONOS Cloud consists of two components. The concept of a DataPlatformClusters and the backing DataPlatformNodePools the cluster is build on.  ### DataPlatformCluster  A DataPlatformCluster is the virtual instance of the customer services and operations running the managed Services like Stackable operators. A DataPlatformCluster is a Kubernetes Cluster in the VDC of the customer. Therefore, it's possible to integrate the cluster with other resources as vLANs e.G. to shape the datacenter in the customer's need and integrate the cluster within the topology the customer wants to build.  In addition to the Kubernetes cluster a small node pool is provided which is exclusively used to run the Stackable operators.  ### DataPlatformNodePool  A DataPlatformNodePool represents the physical machines a DataPlatformCluster is build on top. All nodes within a node pool are identical in setup. The nodes of a pool are provisioned into virtual data centers at a location of your choice and you can freely specify the properties of all the nodes at once before creation.  Nodes in node pools provisioned by the Managed Stackable Data Platform Cloud API are readonly in the customer's VDC and can only be modified or deleted via the API.  ### References   # noqa: E501

    The version of the OpenAPI document: 0.0.7
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from ionoscloud_dataplatform.configuration import Configuration


class ClusterResponseData(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {

        'id': 'str',

        'type': 'str',

        'href': 'str',

        'metadata': 'Metadata',

        'properties': 'Cluster',
    }

    attribute_map = {

        'id': 'id',

        'type': 'type',

        'href': 'href',

        'metadata': 'metadata',

        'properties': 'properties',
    }

    def __init__(self, id=None, type=None, href=None, metadata=None, properties=None, local_vars_configuration=None):  # noqa: E501
        """ClusterResponseData - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._type = None
        self._href = None
        self._metadata = None
        self._properties = None
        self.discriminator = None

        self.id = id
        if type is not None:
            self.type = type
        if href is not None:
            self.href = href
        self.metadata = metadata
        self.properties = properties


    @property
    def id(self):
        """Gets the id of this ClusterResponseData.  # noqa: E501

        The unique ID of the resource. Must conform to the UUID format.   # noqa: E501

        :return: The id of this ClusterResponseData.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ClusterResponseData.

        The unique ID of the resource. Must conform to the UUID format.   # noqa: E501

        :param id: The id of this ClusterResponseData.  # noqa: E501
        :type id: str
        """
        if self.local_vars_configuration.client_side_validation and id is None:  # noqa: E501
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                id is not None and len(id) > 36):
            raise ValueError("Invalid value for `id`, length must be less than or equal to `36`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                id is not None and len(id) < 32):
            raise ValueError("Invalid value for `id`, length must be greater than or equal to `32`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                id is not None and not re.search(r'^[0-9a-f]{8}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{12}$', id)):  # noqa: E501
            raise ValueError(r"Invalid value for `id`, must be a follow pattern or equal to `/^[0-9a-f]{8}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{12}$/`")  # noqa: E501

        self._id = id

    @property
    def type(self):
        """Gets the type of this ClusterResponseData.  # noqa: E501

        The type of the resource.  # noqa: E501

        :return: The type of this ClusterResponseData.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this ClusterResponseData.

        The type of the resource.  # noqa: E501

        :param type: The type of this ClusterResponseData.  # noqa: E501
        :type type: str
        """

        self._type = type

    @property
    def href(self):
        """Gets the href of this ClusterResponseData.  # noqa: E501

        URL to the object representation (absolute path).  # noqa: E501

        :return: The href of this ClusterResponseData.  # noqa: E501
        :rtype: str
        """
        return self._href

    @href.setter
    def href(self, href):
        """Sets the href of this ClusterResponseData.

        URL to the object representation (absolute path).  # noqa: E501

        :param href: The href of this ClusterResponseData.  # noqa: E501
        :type href: str
        """

        self._href = href

    @property
    def metadata(self):
        """Gets the metadata of this ClusterResponseData.  # noqa: E501


        :return: The metadata of this ClusterResponseData.  # noqa: E501
        :rtype: Metadata
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """Sets the metadata of this ClusterResponseData.


        :param metadata: The metadata of this ClusterResponseData.  # noqa: E501
        :type metadata: Metadata
        """
        if self.local_vars_configuration.client_side_validation and metadata is None:  # noqa: E501
            raise ValueError("Invalid value for `metadata`, must not be `None`")  # noqa: E501

        self._metadata = metadata

    @property
    def properties(self):
        """Gets the properties of this ClusterResponseData.  # noqa: E501


        :return: The properties of this ClusterResponseData.  # noqa: E501
        :rtype: Cluster
        """
        return self._properties

    @properties.setter
    def properties(self, properties):
        """Sets the properties of this ClusterResponseData.


        :param properties: The properties of this ClusterResponseData.  # noqa: E501
        :type properties: Cluster
        """
        if self.local_vars_configuration.client_side_validation and properties is None:  # noqa: E501
            raise ValueError("Invalid value for `properties`, must not be `None`")  # noqa: E501

        self._properties = properties
    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ClusterResponseData):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ClusterResponseData):
            return True

        return self.to_dict() != other.to_dict()
