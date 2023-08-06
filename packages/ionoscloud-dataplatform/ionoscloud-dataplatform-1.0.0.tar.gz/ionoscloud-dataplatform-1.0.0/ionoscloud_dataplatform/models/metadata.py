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


class Metadata(object):
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

        'e_tag': 'str',

        'created_date': 'datetime',

        'created_by': 'str',

        'created_by_user_id': 'str',

        'created_in_contract_number': 'str',

        'last_modified_date': 'datetime',

        'last_modified_by': 'str',

        'last_modified_by_user_id': 'str',

        'current_data_platform_version': 'str',

        'current_data_platform_revision': 'int',

        'available_upgrade_versions': 'list[str]',

        'state': 'str',
    }

    attribute_map = {

        'e_tag': 'ETag',

        'created_date': 'createdDate',

        'created_by': 'createdBy',

        'created_by_user_id': 'createdByUserId',

        'created_in_contract_number': 'createdInContractNumber',

        'last_modified_date': 'lastModifiedDate',

        'last_modified_by': 'lastModifiedBy',

        'last_modified_by_user_id': 'lastModifiedByUserId',

        'current_data_platform_version': 'currentDataPlatformVersion',

        'current_data_platform_revision': 'currentDataPlatformRevision',

        'available_upgrade_versions': 'availableUpgradeVersions',

        'state': 'state',
    }

    def __init__(self, e_tag=None, created_date=None, created_by=None, created_by_user_id=None, created_in_contract_number=None, last_modified_date=None, last_modified_by=None, last_modified_by_user_id=None, current_data_platform_version=None, current_data_platform_revision=None, available_upgrade_versions=None, state=None, local_vars_configuration=None):  # noqa: E501
        """Metadata - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._e_tag = None
        self._created_date = None
        self._created_by = None
        self._created_by_user_id = None
        self._created_in_contract_number = None
        self._last_modified_date = None
        self._last_modified_by = None
        self._last_modified_by_user_id = None
        self._current_data_platform_version = None
        self._current_data_platform_revision = None
        self._available_upgrade_versions = None
        self._state = None
        self.discriminator = None

        if e_tag is not None:
            self.e_tag = e_tag
        if created_date is not None:
            self.created_date = created_date
        if created_by is not None:
            self.created_by = created_by
        if created_by_user_id is not None:
            self.created_by_user_id = created_by_user_id
        if created_in_contract_number is not None:
            self.created_in_contract_number = created_in_contract_number
        if last_modified_date is not None:
            self.last_modified_date = last_modified_date
        if last_modified_by is not None:
            self.last_modified_by = last_modified_by
        if last_modified_by_user_id is not None:
            self.last_modified_by_user_id = last_modified_by_user_id
        if current_data_platform_version is not None:
            self.current_data_platform_version = current_data_platform_version
        if current_data_platform_revision is not None:
            self.current_data_platform_revision = current_data_platform_revision
        if available_upgrade_versions is not None:
            self.available_upgrade_versions = available_upgrade_versions
        if state is not None:
            self.state = state


    @property
    def e_tag(self):
        """Gets the e_tag of this Metadata.  # noqa: E501

        The Entity Tag of the resource as defined in http://www.w3.org/Protocols/rfc2616/rfc2616-sec3.html#sec3.11  # noqa: E501

        :return: The e_tag of this Metadata.  # noqa: E501
        :rtype: str
        """
        return self._e_tag

    @e_tag.setter
    def e_tag(self, e_tag):
        """Sets the e_tag of this Metadata.

        The Entity Tag of the resource as defined in http://www.w3.org/Protocols/rfc2616/rfc2616-sec3.html#sec3.11  # noqa: E501

        :param e_tag: The e_tag of this Metadata.  # noqa: E501
        :type e_tag: str
        """

        self._e_tag = e_tag

    @property
    def created_date(self):
        """Gets the created_date of this Metadata.  # noqa: E501

        The time the resource was created, ISO 8601 timestamp (UTC).  # noqa: E501

        :return: The created_date of this Metadata.  # noqa: E501
        :rtype: datetime
        """
        return self._created_date

    @created_date.setter
    def created_date(self, created_date):
        """Sets the created_date of this Metadata.

        The time the resource was created, ISO 8601 timestamp (UTC).  # noqa: E501

        :param created_date: The created_date of this Metadata.  # noqa: E501
        :type created_date: datetime
        """

        self._created_date = created_date

    @property
    def created_by(self):
        """Gets the created_by of this Metadata.  # noqa: E501

        The user that created the resource  # noqa: E501

        :return: The created_by of this Metadata.  # noqa: E501
        :rtype: str
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """Sets the created_by of this Metadata.

        The user that created the resource  # noqa: E501

        :param created_by: The created_by of this Metadata.  # noqa: E501
        :type created_by: str
        """

        self._created_by = created_by

    @property
    def created_by_user_id(self):
        """Gets the created_by_user_id of this Metadata.  # noqa: E501

        The ID of the user that created the resource  # noqa: E501

        :return: The created_by_user_id of this Metadata.  # noqa: E501
        :rtype: str
        """
        return self._created_by_user_id

    @created_by_user_id.setter
    def created_by_user_id(self, created_by_user_id):
        """Sets the created_by_user_id of this Metadata.

        The ID of the user that created the resource  # noqa: E501

        :param created_by_user_id: The created_by_user_id of this Metadata.  # noqa: E501
        :type created_by_user_id: str
        """

        self._created_by_user_id = created_by_user_id

    @property
    def created_in_contract_number(self):
        """Gets the created_in_contract_number of this Metadata.  # noqa: E501

        The creators contractNumber  # noqa: E501

        :return: The created_in_contract_number of this Metadata.  # noqa: E501
        :rtype: str
        """
        return self._created_in_contract_number

    @created_in_contract_number.setter
    def created_in_contract_number(self, created_in_contract_number):
        """Sets the created_in_contract_number of this Metadata.

        The creators contractNumber  # noqa: E501

        :param created_in_contract_number: The created_in_contract_number of this Metadata.  # noqa: E501
        :type created_in_contract_number: str
        """

        self._created_in_contract_number = created_in_contract_number

    @property
    def last_modified_date(self):
        """Gets the last_modified_date of this Metadata.  # noqa: E501

        The last time the resource was modified, ISO 8601 timestamp (UTC).  # noqa: E501

        :return: The last_modified_date of this Metadata.  # noqa: E501
        :rtype: datetime
        """
        return self._last_modified_date

    @last_modified_date.setter
    def last_modified_date(self, last_modified_date):
        """Sets the last_modified_date of this Metadata.

        The last time the resource was modified, ISO 8601 timestamp (UTC).  # noqa: E501

        :param last_modified_date: The last_modified_date of this Metadata.  # noqa: E501
        :type last_modified_date: datetime
        """

        self._last_modified_date = last_modified_date

    @property
    def last_modified_by(self):
        """Gets the last_modified_by of this Metadata.  # noqa: E501

        The user that last modified the resource  # noqa: E501

        :return: The last_modified_by of this Metadata.  # noqa: E501
        :rtype: str
        """
        return self._last_modified_by

    @last_modified_by.setter
    def last_modified_by(self, last_modified_by):
        """Sets the last_modified_by of this Metadata.

        The user that last modified the resource  # noqa: E501

        :param last_modified_by: The last_modified_by of this Metadata.  # noqa: E501
        :type last_modified_by: str
        """

        self._last_modified_by = last_modified_by

    @property
    def last_modified_by_user_id(self):
        """Gets the last_modified_by_user_id of this Metadata.  # noqa: E501

        The ID of the user that last modified the resource  # noqa: E501

        :return: The last_modified_by_user_id of this Metadata.  # noqa: E501
        :rtype: str
        """
        return self._last_modified_by_user_id

    @last_modified_by_user_id.setter
    def last_modified_by_user_id(self, last_modified_by_user_id):
        """Sets the last_modified_by_user_id of this Metadata.

        The ID of the user that last modified the resource  # noqa: E501

        :param last_modified_by_user_id: The last_modified_by_user_id of this Metadata.  # noqa: E501
        :type last_modified_by_user_id: str
        """

        self._last_modified_by_user_id = last_modified_by_user_id

    @property
    def current_data_platform_version(self):
        """Gets the current_data_platform_version of this Metadata.  # noqa: E501

        The version of the DataPlatform.   # noqa: E501

        :return: The current_data_platform_version of this Metadata.  # noqa: E501
        :rtype: str
        """
        return self._current_data_platform_version

    @current_data_platform_version.setter
    def current_data_platform_version(self, current_data_platform_version):
        """Sets the current_data_platform_version of this Metadata.

        The version of the DataPlatform.   # noqa: E501

        :param current_data_platform_version: The current_data_platform_version of this Metadata.  # noqa: E501
        :type current_data_platform_version: str
        """
        if (self.local_vars_configuration.client_side_validation and
                current_data_platform_version is not None and len(current_data_platform_version) > 32):
            raise ValueError("Invalid value for `current_data_platform_version`, length must be less than or equal to `32`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                current_data_platform_version is not None and not re.search(r'^[-A-Za-z0-9_.]*$', current_data_platform_version)):  # noqa: E501
            raise ValueError(r"Invalid value for `current_data_platform_version`, must be a follow pattern or equal to `/^[-A-Za-z0-9_.]*$/`")  # noqa: E501

        self._current_data_platform_version = current_data_platform_version

    @property
    def current_data_platform_revision(self):
        """Gets the current_data_platform_revision of this Metadata.  # noqa: E501

        The current dataplatform revision of a resource. This internal revision is used to rollout non-breaking internal changes. This attribute is read-only.   # noqa: E501

        :return: The current_data_platform_revision of this Metadata.  # noqa: E501
        :rtype: int
        """
        return self._current_data_platform_revision

    @current_data_platform_revision.setter
    def current_data_platform_revision(self, current_data_platform_revision):
        """Sets the current_data_platform_revision of this Metadata.

        The current dataplatform revision of a resource. This internal revision is used to rollout non-breaking internal changes. This attribute is read-only.   # noqa: E501

        :param current_data_platform_revision: The current_data_platform_revision of this Metadata.  # noqa: E501
        :type current_data_platform_revision: int
        """
        if (self.local_vars_configuration.client_side_validation and
                current_data_platform_revision is not None and current_data_platform_revision < 0):  # noqa: E501
            raise ValueError("Invalid value for `current_data_platform_revision`, must be a value greater than or equal to `0`")  # noqa: E501

        self._current_data_platform_revision = current_data_platform_revision

    @property
    def available_upgrade_versions(self):
        """Gets the available_upgrade_versions of this Metadata.  # noqa: E501

        List of available upgrades for this cluster  # noqa: E501

        :return: The available_upgrade_versions of this Metadata.  # noqa: E501
        :rtype: list[str]
        """
        return self._available_upgrade_versions

    @available_upgrade_versions.setter
    def available_upgrade_versions(self, available_upgrade_versions):
        """Sets the available_upgrade_versions of this Metadata.

        List of available upgrades for this cluster  # noqa: E501

        :param available_upgrade_versions: The available_upgrade_versions of this Metadata.  # noqa: E501
        :type available_upgrade_versions: list[str]
        """

        self._available_upgrade_versions = available_upgrade_versions

    @property
    def state(self):
        """Gets the state of this Metadata.  # noqa: E501

        State of the resource. *AVAILABLE* There are no pending modification requests for this item; *BUSY* There is at least one modification request pending and all following requests will be queued; *DEPLOYING* Resource state DEPLOYING - the resource is being created; *FAILED* Resource state FAILED - creation of the resource failed; *UPDATING* Resource state UPDATING - the resource is being updated; *FAILED_UPDATING* Resource state FAILED_UPDATING - an update to the resource was not successful; *DESTROYING* Resource state DESTROYING - the resource is being deleted; *FAILED_DESTROYING* Resource state FAILED_DESTROYING - deletion of the resource was not successful; *TERMINATED* Resource state TERMINATED - the resource was deleted.   # noqa: E501

        :return: The state of this Metadata.  # noqa: E501
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state):
        """Sets the state of this Metadata.

        State of the resource. *AVAILABLE* There are no pending modification requests for this item; *BUSY* There is at least one modification request pending and all following requests will be queued; *DEPLOYING* Resource state DEPLOYING - the resource is being created; *FAILED* Resource state FAILED - creation of the resource failed; *UPDATING* Resource state UPDATING - the resource is being updated; *FAILED_UPDATING* Resource state FAILED_UPDATING - an update to the resource was not successful; *DESTROYING* Resource state DESTROYING - the resource is being deleted; *FAILED_DESTROYING* Resource state FAILED_DESTROYING - deletion of the resource was not successful; *TERMINATED* Resource state TERMINATED - the resource was deleted.   # noqa: E501

        :param state: The state of this Metadata.  # noqa: E501
        :type state: str
        """
        allowed_values = ["AVAILABLE", "BUSY", "DEPLOYING", "FAILED", "UPDATING", "FAILED_UPDATING", "DESTROYING", "FAILED_DESTROYING", "TERMINATED"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and state not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `state` ({0}), must be one of {1}"  # noqa: E501
                .format(state, allowed_values)
            )

        self._state = state
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
        if not isinstance(other, Metadata):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Metadata):
            return True

        return self.to_dict() != other.to_dict()
