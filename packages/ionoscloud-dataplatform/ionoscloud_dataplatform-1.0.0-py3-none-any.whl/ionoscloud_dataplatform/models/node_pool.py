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


class NodePool(object):
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

        'node_count': 'int',

        'cpu_family': 'str',

        'cores_count': 'int',

        'ram_size': 'int',

        'availability_zone': 'AvailabilityZone',

        'storage_type': 'StorageType',

        'storage_size': 'int',

        'maintenance_window': 'MaintenanceWindow',

        'labels': 'object',

        'annotations': 'object',
    }

    attribute_map = {

        'name': 'name',

        'data_platform_version': 'dataPlatformVersion',

        'datacenter_id': 'datacenterId',

        'node_count': 'nodeCount',

        'cpu_family': 'cpuFamily',

        'cores_count': 'coresCount',

        'ram_size': 'ramSize',

        'availability_zone': 'availabilityZone',

        'storage_type': 'storageType',

        'storage_size': 'storageSize',

        'maintenance_window': 'maintenanceWindow',

        'labels': 'labels',

        'annotations': 'annotations',
    }

    def __init__(self, name=None, data_platform_version=None, datacenter_id=None, node_count=None, cpu_family='AUTO', cores_count=4, ram_size=4096, availability_zone=None, storage_type=None, storage_size=20, maintenance_window=None, labels=None, annotations=None, local_vars_configuration=None):  # noqa: E501
        """NodePool - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._name = None
        self._data_platform_version = None
        self._datacenter_id = None
        self._node_count = None
        self._cpu_family = None
        self._cores_count = None
        self._ram_size = None
        self._availability_zone = None
        self._storage_type = None
        self._storage_size = None
        self._maintenance_window = None
        self._labels = None
        self._annotations = None
        self.discriminator = None

        if name is not None:
            self.name = name
        if data_platform_version is not None:
            self.data_platform_version = data_platform_version
        if datacenter_id is not None:
            self.datacenter_id = datacenter_id
        if node_count is not None:
            self.node_count = node_count
        if cpu_family is not None:
            self.cpu_family = cpu_family
        if cores_count is not None:
            self.cores_count = cores_count
        if ram_size is not None:
            self.ram_size = ram_size
        if availability_zone is not None:
            self.availability_zone = availability_zone
        if storage_type is not None:
            self.storage_type = storage_type
        if storage_size is not None:
            self.storage_size = storage_size
        if maintenance_window is not None:
            self.maintenance_window = maintenance_window
        if labels is not None:
            self.labels = labels
        if annotations is not None:
            self.annotations = annotations


    @property
    def name(self):
        """Gets the name of this NodePool.  # noqa: E501

        The name of your node pool. Must be 63 characters or less and must begin and end with an alphanumeric character ([a-z0-9A-Z]) with dashes (-), underscores (_), dots (.), and alphanumerics between.   # noqa: E501

        :return: The name of this NodePool.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this NodePool.

        The name of your node pool. Must be 63 characters or less and must begin and end with an alphanumeric character ([a-z0-9A-Z]) with dashes (-), underscores (_), dots (.), and alphanumerics between.   # noqa: E501

        :param name: The name of this NodePool.  # noqa: E501
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
        """Gets the data_platform_version of this NodePool.  # noqa: E501

        The version of the DataPlatform.   # noqa: E501

        :return: The data_platform_version of this NodePool.  # noqa: E501
        :rtype: str
        """
        return self._data_platform_version

    @data_platform_version.setter
    def data_platform_version(self, data_platform_version):
        """Sets the data_platform_version of this NodePool.

        The version of the DataPlatform.   # noqa: E501

        :param data_platform_version: The data_platform_version of this NodePool.  # noqa: E501
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
        """Gets the datacenter_id of this NodePool.  # noqa: E501

        The UUID of the virtual data center (VDC) the cluster is provisioned.   # noqa: E501

        :return: The datacenter_id of this NodePool.  # noqa: E501
        :rtype: str
        """
        return self._datacenter_id

    @datacenter_id.setter
    def datacenter_id(self, datacenter_id):
        """Sets the datacenter_id of this NodePool.

        The UUID of the virtual data center (VDC) the cluster is provisioned.   # noqa: E501

        :param datacenter_id: The datacenter_id of this NodePool.  # noqa: E501
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
    def node_count(self):
        """Gets the node_count of this NodePool.  # noqa: E501

        The number of nodes that make up the node pool.   # noqa: E501

        :return: The node_count of this NodePool.  # noqa: E501
        :rtype: int
        """
        return self._node_count

    @node_count.setter
    def node_count(self, node_count):
        """Sets the node_count of this NodePool.

        The number of nodes that make up the node pool.   # noqa: E501

        :param node_count: The node_count of this NodePool.  # noqa: E501
        :type node_count: int
        """
        if (self.local_vars_configuration.client_side_validation and
                node_count is not None and node_count < 1):  # noqa: E501
            raise ValueError("Invalid value for `node_count`, must be a value greater than or equal to `1`")  # noqa: E501

        self._node_count = node_count

    @property
    def cpu_family(self):
        """Gets the cpu_family of this NodePool.  # noqa: E501

        A valid CPU family name or `AUTO` if the platform shall choose the best fitting option. Available CPU architectures can be retrieved from the datacenter resource.   # noqa: E501

        :return: The cpu_family of this NodePool.  # noqa: E501
        :rtype: str
        """
        return self._cpu_family

    @cpu_family.setter
    def cpu_family(self, cpu_family):
        """Sets the cpu_family of this NodePool.

        A valid CPU family name or `AUTO` if the platform shall choose the best fitting option. Available CPU architectures can be retrieved from the datacenter resource.   # noqa: E501

        :param cpu_family: The cpu_family of this NodePool.  # noqa: E501
        :type cpu_family: str
        """
        if (self.local_vars_configuration.client_side_validation and
                cpu_family is not None and len(cpu_family) > 32):
            raise ValueError("Invalid value for `cpu_family`, length must be less than or equal to `32`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                cpu_family is not None and not re.search(r'^[-A-Za-z0-9_.]*$', cpu_family)):  # noqa: E501
            raise ValueError(r"Invalid value for `cpu_family`, must be a follow pattern or equal to `/^[-A-Za-z0-9_.]*$/`")  # noqa: E501

        self._cpu_family = cpu_family

    @property
    def cores_count(self):
        """Gets the cores_count of this NodePool.  # noqa: E501

        The number of CPU cores per node.   # noqa: E501

        :return: The cores_count of this NodePool.  # noqa: E501
        :rtype: int
        """
        return self._cores_count

    @cores_count.setter
    def cores_count(self, cores_count):
        """Sets the cores_count of this NodePool.

        The number of CPU cores per node.   # noqa: E501

        :param cores_count: The cores_count of this NodePool.  # noqa: E501
        :type cores_count: int
        """
        if (self.local_vars_configuration.client_side_validation and
                cores_count is not None and cores_count < 1):  # noqa: E501
            raise ValueError("Invalid value for `cores_count`, must be a value greater than or equal to `1`")  # noqa: E501

        self._cores_count = cores_count

    @property
    def ram_size(self):
        """Gets the ram_size of this NodePool.  # noqa: E501

        The RAM size for one node in MB. Must be set in multiples of 1024 MB, with a minimum size is of 2048 MB.  # noqa: E501

        :return: The ram_size of this NodePool.  # noqa: E501
        :rtype: int
        """
        return self._ram_size

    @ram_size.setter
    def ram_size(self, ram_size):
        """Sets the ram_size of this NodePool.

        The RAM size for one node in MB. Must be set in multiples of 1024 MB, with a minimum size is of 2048 MB.  # noqa: E501

        :param ram_size: The ram_size of this NodePool.  # noqa: E501
        :type ram_size: int
        """
        if (self.local_vars_configuration.client_side_validation and
                ram_size is not None and ram_size < 2048):  # noqa: E501
            raise ValueError("Invalid value for `ram_size`, must be a value greater than or equal to `2048`")  # noqa: E501

        self._ram_size = ram_size

    @property
    def availability_zone(self):
        """Gets the availability_zone of this NodePool.  # noqa: E501


        :return: The availability_zone of this NodePool.  # noqa: E501
        :rtype: AvailabilityZone
        """
        return self._availability_zone

    @availability_zone.setter
    def availability_zone(self, availability_zone):
        """Sets the availability_zone of this NodePool.


        :param availability_zone: The availability_zone of this NodePool.  # noqa: E501
        :type availability_zone: AvailabilityZone
        """

        self._availability_zone = availability_zone

    @property
    def storage_type(self):
        """Gets the storage_type of this NodePool.  # noqa: E501


        :return: The storage_type of this NodePool.  # noqa: E501
        :rtype: StorageType
        """
        return self._storage_type

    @storage_type.setter
    def storage_type(self, storage_type):
        """Sets the storage_type of this NodePool.


        :param storage_type: The storage_type of this NodePool.  # noqa: E501
        :type storage_type: StorageType
        """

        self._storage_type = storage_type

    @property
    def storage_size(self):
        """Gets the storage_size of this NodePool.  # noqa: E501

        The size of the volume in GB. The size must be greater than 10GB.  # noqa: E501

        :return: The storage_size of this NodePool.  # noqa: E501
        :rtype: int
        """
        return self._storage_size

    @storage_size.setter
    def storage_size(self, storage_size):
        """Sets the storage_size of this NodePool.

        The size of the volume in GB. The size must be greater than 10GB.  # noqa: E501

        :param storage_size: The storage_size of this NodePool.  # noqa: E501
        :type storage_size: int
        """
        if (self.local_vars_configuration.client_side_validation and
                storage_size is not None and storage_size < 10):  # noqa: E501
            raise ValueError("Invalid value for `storage_size`, must be a value greater than or equal to `10`")  # noqa: E501

        self._storage_size = storage_size

    @property
    def maintenance_window(self):
        """Gets the maintenance_window of this NodePool.  # noqa: E501


        :return: The maintenance_window of this NodePool.  # noqa: E501
        :rtype: MaintenanceWindow
        """
        return self._maintenance_window

    @maintenance_window.setter
    def maintenance_window(self, maintenance_window):
        """Sets the maintenance_window of this NodePool.


        :param maintenance_window: The maintenance_window of this NodePool.  # noqa: E501
        :type maintenance_window: MaintenanceWindow
        """

        self._maintenance_window = maintenance_window

    @property
    def labels(self):
        """Gets the labels of this NodePool.  # noqa: E501

        Key-value pairs attached to the node pool resource as [Kubernetes labels](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/)   # noqa: E501

        :return: The labels of this NodePool.  # noqa: E501
        :rtype: object
        """
        return self._labels

    @labels.setter
    def labels(self, labels):
        """Sets the labels of this NodePool.

        Key-value pairs attached to the node pool resource as [Kubernetes labels](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/)   # noqa: E501

        :param labels: The labels of this NodePool.  # noqa: E501
        :type labels: object
        """

        self._labels = labels

    @property
    def annotations(self):
        """Gets the annotations of this NodePool.  # noqa: E501

        Key-value pairs attached to node pool resource as [Kubernetes annotations](https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/)   # noqa: E501

        :return: The annotations of this NodePool.  # noqa: E501
        :rtype: object
        """
        return self._annotations

    @annotations.setter
    def annotations(self, annotations):
        """Sets the annotations of this NodePool.

        Key-value pairs attached to node pool resource as [Kubernetes annotations](https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/)   # noqa: E501

        :param annotations: The annotations of this NodePool.  # noqa: E501
        :type annotations: object
        """

        self._annotations = annotations
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
        if not isinstance(other, NodePool):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, NodePool):
            return True

        return self.to_dict() != other.to_dict()
