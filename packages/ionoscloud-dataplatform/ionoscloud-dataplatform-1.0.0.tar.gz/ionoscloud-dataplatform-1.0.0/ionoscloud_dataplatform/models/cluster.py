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


class Cluster(object):
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

        'name': 'str',

        'data_platform_version': 'str',

        'datacenter_id': 'str',

        'maintenance_window': 'MaintenanceWindow',
    }

    attribute_map = {

        'name': 'name',

        'data_platform_version': 'dataPlatformVersion',

        'datacenter_id': 'datacenterId',

        'maintenance_window': 'maintenanceWindow',
    }

    def __init__(self, name=None, data_platform_version=None, datacenter_id=None, maintenance_window=None, local_vars_configuration=None):  # noqa: E501
        """Cluster - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._name = None
        self._data_platform_version = None
        self._datacenter_id = None
        self._maintenance_window = None
        self.discriminator = None

        if name is not None:
            self.name = name
        if data_platform_version is not None:
            self.data_platform_version = data_platform_version
        if datacenter_id is not None:
            self.datacenter_id = datacenter_id
        if maintenance_window is not None:
            self.maintenance_window = maintenance_window


    @property
    def name(self):
        """Gets the name of this Cluster.  # noqa: E501

        The name of your cluster. Must be 63 characters or less and must begin and end with an alphanumeric character ([a-z0-9A-Z]) with dashes (-), underscores (_), dots (.), and alphanumerics between.   # noqa: E501

        :return: The name of this Cluster.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Cluster.

        The name of your cluster. Must be 63 characters or less and must begin and end with an alphanumeric character ([a-z0-9A-Z]) with dashes (-), underscores (_), dots (.), and alphanumerics between.   # noqa: E501

        :param name: The name of this Cluster.  # noqa: E501
        :type name: str
        """
        if (self.local_vars_configuration.client_side_validation and
                name is not None and len(name) > 63):
            raise ValueError("Invalid value for `name`, length must be less than or equal to `63`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                name is not None and len(name) < 2):
            raise ValueError("Invalid value for `name`, length must be greater than or equal to `2`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                name is not None and not re.search(r'^[A-Za-z0-9][-A-Za-z0-9_.]*[A-Za-z0-9]$', name)):  # noqa: E501
            raise ValueError(r"Invalid value for `name`, must be a follow pattern or equal to `/^[A-Za-z0-9][-A-Za-z0-9_.]*[A-Za-z0-9]$/`")  # noqa: E501

        self._name = name

    @property
    def data_platform_version(self):
        """Gets the data_platform_version of this Cluster.  # noqa: E501

        The version of the DataPlatform.   # noqa: E501

        :return: The data_platform_version of this Cluster.  # noqa: E501
        :rtype: str
        """
        return self._data_platform_version

    @data_platform_version.setter
    def data_platform_version(self, data_platform_version):
        """Sets the data_platform_version of this Cluster.

        The version of the DataPlatform.   # noqa: E501

        :param data_platform_version: The data_platform_version of this Cluster.  # noqa: E501
        :type data_platform_version: str
        """
        if (self.local_vars_configuration.client_side_validation and
                data_platform_version is not None and len(data_platform_version) > 32):
            raise ValueError("Invalid value for `data_platform_version`, length must be less than or equal to `32`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                data_platform_version is not None and not re.search(r'^[-A-Za-z0-9_.]*$', data_platform_version)):  # noqa: E501
            raise ValueError(r"Invalid value for `data_platform_version`, must be a follow pattern or equal to `/^[-A-Za-z0-9_.]*$/`")  # noqa: E501

        self._data_platform_version = data_platform_version

    @property
    def datacenter_id(self):
        """Gets the datacenter_id of this Cluster.  # noqa: E501

        The UUID of the virtual data center (VDC) the cluster is provisioned.   # noqa: E501

        :return: The datacenter_id of this Cluster.  # noqa: E501
        :rtype: str
        """
        return self._datacenter_id

    @datacenter_id.setter
    def datacenter_id(self, datacenter_id):
        """Sets the datacenter_id of this Cluster.

        The UUID of the virtual data center (VDC) the cluster is provisioned.   # noqa: E501

        :param datacenter_id: The datacenter_id of this Cluster.  # noqa: E501
        :type datacenter_id: str
        """
        if (self.local_vars_configuration.client_side_validation and
                datacenter_id is not None and len(datacenter_id) > 36):
            raise ValueError("Invalid value for `datacenter_id`, length must be less than or equal to `36`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                datacenter_id is not None and len(datacenter_id) < 32):
            raise ValueError("Invalid value for `datacenter_id`, length must be greater than or equal to `32`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                datacenter_id is not None and not re.search(r'^[0-9a-f]{8}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{12}$', datacenter_id)):  # noqa: E501
            raise ValueError(r"Invalid value for `datacenter_id`, must be a follow pattern or equal to `/^[0-9a-f]{8}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{12}$/`")  # noqa: E501

        self._datacenter_id = datacenter_id

    @property
    def maintenance_window(self):
        """Gets the maintenance_window of this Cluster.  # noqa: E501


        :return: The maintenance_window of this Cluster.  # noqa: E501
        :rtype: MaintenanceWindow
        """
        return self._maintenance_window

    @maintenance_window.setter
    def maintenance_window(self, maintenance_window):
        """Sets the maintenance_window of this Cluster.


        :param maintenance_window: The maintenance_window of this Cluster.  # noqa: E501
        :type maintenance_window: MaintenanceWindow
        """

        self._maintenance_window = maintenance_window
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
        if not isinstance(other, Cluster):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Cluster):
            return True

        return self.to_dict() != other.to_dict()
