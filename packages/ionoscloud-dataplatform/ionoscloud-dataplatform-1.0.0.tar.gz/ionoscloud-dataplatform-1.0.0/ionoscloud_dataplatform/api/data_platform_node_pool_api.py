from __future__ import absolute_import

import re  # noqa: F401
import six

from ionoscloud_dataplatform.api_client import ApiClient
from ionoscloud_dataplatform.exceptions import (  # noqa: F401
    ApiTypeError,
    ApiValueError
)


class DataPlatformNodePoolApi(object):

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def create_cluster_nodepool(self, cluster_id, create_node_pool_request, **kwargs):  # noqa: E501
        """Create a DataPlatformNodePool for a distinct DataPlatformCluster  # noqa: E501

        Creates a new node pool and assignes the node pool resources exclusively to the defined managed cluster.  The cluster ID can be found in the response when a cluster is created or when you GET a list of all DataPlatformClusters.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.create_cluster_nodepool(cluster_id, create_node_pool_request, async_req=True)
        >>> result = thread.get()

        :param cluster_id: The unique ID of the cluster. Must conform to the UUID format.  (required)
        :type cluster_id: str
        :param create_node_pool_request: Request payload with the properties that defines a DataPlatformNodePool.  (required)
        :type create_node_pool_request: CreateNodePoolRequest
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: NodePoolResponseData
        """
        kwargs['_return_http_data_only'] = True
        return self.create_cluster_nodepool_with_http_info(cluster_id, create_node_pool_request, **kwargs)  # noqa: E501

    def create_cluster_nodepool_with_http_info(self, cluster_id, create_node_pool_request, **kwargs):  # noqa: E501
        """Create a DataPlatformNodePool for a distinct DataPlatformCluster  # noqa: E501

        Creates a new node pool and assignes the node pool resources exclusively to the defined managed cluster.  The cluster ID can be found in the response when a cluster is created or when you GET a list of all DataPlatformClusters.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.create_cluster_nodepool_with_http_info(cluster_id, create_node_pool_request, async_req=True)
        >>> result = thread.get()

        :param cluster_id: The unique ID of the cluster. Must conform to the UUID format.  (required)
        :type cluster_id: str
        :param create_node_pool_request: Request payload with the properties that defines a DataPlatformNodePool.  (required)
        :type create_node_pool_request: CreateNodePoolRequest
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _return_http_data_only: response data without head status code
                                       and headers
        :type _return_http_data_only: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(NodePoolResponseData, status_code(int), headers(HTTPHeaderDict))
        """

        local_var_params = locals()

        all_params = [
            'cluster_id',
            'create_node_pool_request'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                'response_type',
                'query_params'
            ]
        )

        for local_var_params_key, local_var_params_val in six.iteritems(local_var_params['kwargs']):
            if local_var_params_key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create_cluster_nodepool" % local_var_params_key
                )
            local_var_params[local_var_params_key] = local_var_params_val
        del local_var_params['kwargs']
        # verify the required parameter 'cluster_id' is set
        if self.api_client.client_side_validation and ('cluster_id' not in local_var_params or  # noqa: E501
                                                        local_var_params['cluster_id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `cluster_id` when calling `create_cluster_nodepool`")  # noqa: E501
        # verify the required parameter 'create_node_pool_request' is set
        if self.api_client.client_side_validation and ('create_node_pool_request' not in local_var_params or  # noqa: E501
                                                        local_var_params['create_node_pool_request'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `create_node_pool_request` when calling `create_cluster_nodepool`")  # noqa: E501

        if self.api_client.client_side_validation and ('cluster_id' in local_var_params and  # noqa: E501
                                                        len(local_var_params['cluster_id']) > 36):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `cluster_id` when calling `create_cluster_nodepool`, length must be less than or equal to `36`")  # noqa: E501
        if self.api_client.client_side_validation and ('cluster_id' in local_var_params and  # noqa: E501
                                                        len(local_var_params['cluster_id']) < 32):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `cluster_id` when calling `create_cluster_nodepool`, length must be greater than or equal to `32`")  # noqa: E501
        if self.api_client.client_side_validation and 'cluster_id' in local_var_params and not re.search(r'^[0-9a-f]{8}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{12}$', local_var_params['cluster_id']):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `cluster_id` when calling `create_cluster_nodepool`, must conform to the pattern `/^[0-9a-f]{8}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{12}$/`")  # noqa: E501
        collection_formats = {}

        path_params = {}
        if 'cluster_id' in local_var_params:
            path_params['clusterId'] = local_var_params['cluster_id']  # noqa: E501

        query_params = list(local_var_params.get('query_params', {}).items())

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'create_node_pool_request' in local_var_params:
            body_params = local_var_params['create_node_pool_request']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['basicAuth', 'tokenAuth']  # noqa: E501

        response_type = 'NodePoolResponseData'
        if 'response_type' in kwargs:
            response_type = kwargs['response_type']

        return self.api_client.call_api(
            '/clusters/{clusterId}/nodepools', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=response_type,  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats,
            _request_auth=local_var_params.get('_request_auth'))

    def delete_cluster_nodepool(self, cluster_id, nodepool_id, **kwargs):  # noqa: E501
        """Remove node pool from DataPlatformCluster.  # noqa: E501

        Removes the specified node pool from the specified DataPlatformCluster and deletes the node pool afterwards.  The cluster ID can be found in the response when a cluster is created or when you GET a list of all DataPlatformClusters.  The node pool ID can be found in the response when a node pool is created or when you GET a list of all node pools assigned to a specific DataPlatformCluster.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.delete_cluster_nodepool(cluster_id, nodepool_id, async_req=True)
        >>> result = thread.get()

        :param cluster_id: The unique ID of the cluster. Must conform to the UUID format.  (required)
        :type cluster_id: str
        :param nodepool_id: The unique ID of the node pool. Must conform to the UUID format.  (required)
        :type nodepool_id: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: NodePoolResponseData
        """
        kwargs['_return_http_data_only'] = True
        return self.delete_cluster_nodepool_with_http_info(cluster_id, nodepool_id, **kwargs)  # noqa: E501

    def delete_cluster_nodepool_with_http_info(self, cluster_id, nodepool_id, **kwargs):  # noqa: E501
        """Remove node pool from DataPlatformCluster.  # noqa: E501

        Removes the specified node pool from the specified DataPlatformCluster and deletes the node pool afterwards.  The cluster ID can be found in the response when a cluster is created or when you GET a list of all DataPlatformClusters.  The node pool ID can be found in the response when a node pool is created or when you GET a list of all node pools assigned to a specific DataPlatformCluster.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.delete_cluster_nodepool_with_http_info(cluster_id, nodepool_id, async_req=True)
        >>> result = thread.get()

        :param cluster_id: The unique ID of the cluster. Must conform to the UUID format.  (required)
        :type cluster_id: str
        :param nodepool_id: The unique ID of the node pool. Must conform to the UUID format.  (required)
        :type nodepool_id: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _return_http_data_only: response data without head status code
                                       and headers
        :type _return_http_data_only: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(NodePoolResponseData, status_code(int), headers(HTTPHeaderDict))
        """

        local_var_params = locals()

        all_params = [
            'cluster_id',
            'nodepool_id'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                'response_type',
                'query_params'
            ]
        )

        for local_var_params_key, local_var_params_val in six.iteritems(local_var_params['kwargs']):
            if local_var_params_key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_cluster_nodepool" % local_var_params_key
                )
            local_var_params[local_var_params_key] = local_var_params_val
        del local_var_params['kwargs']
        # verify the required parameter 'cluster_id' is set
        if self.api_client.client_side_validation and ('cluster_id' not in local_var_params or  # noqa: E501
                                                        local_var_params['cluster_id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `cluster_id` when calling `delete_cluster_nodepool`")  # noqa: E501
        # verify the required parameter 'nodepool_id' is set
        if self.api_client.client_side_validation and ('nodepool_id' not in local_var_params or  # noqa: E501
                                                        local_var_params['nodepool_id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `nodepool_id` when calling `delete_cluster_nodepool`")  # noqa: E501

        if self.api_client.client_side_validation and ('cluster_id' in local_var_params and  # noqa: E501
                                                        len(local_var_params['cluster_id']) > 36):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `cluster_id` when calling `delete_cluster_nodepool`, length must be less than or equal to `36`")  # noqa: E501
        if self.api_client.client_side_validation and ('cluster_id' in local_var_params and  # noqa: E501
                                                        len(local_var_params['cluster_id']) < 32):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `cluster_id` when calling `delete_cluster_nodepool`, length must be greater than or equal to `32`")  # noqa: E501
        if self.api_client.client_side_validation and 'cluster_id' in local_var_params and not re.search(r'^[0-9a-f]{8}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{12}$', local_var_params['cluster_id']):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `cluster_id` when calling `delete_cluster_nodepool`, must conform to the pattern `/^[0-9a-f]{8}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{12}$/`")  # noqa: E501
        if self.api_client.client_side_validation and ('nodepool_id' in local_var_params and  # noqa: E501
                                                        len(local_var_params['nodepool_id']) > 36):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `nodepool_id` when calling `delete_cluster_nodepool`, length must be less than or equal to `36`")  # noqa: E501
        if self.api_client.client_side_validation and ('nodepool_id' in local_var_params and  # noqa: E501
                                                        len(local_var_params['nodepool_id']) < 32):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `nodepool_id` when calling `delete_cluster_nodepool`, length must be greater than or equal to `32`")  # noqa: E501
        if self.api_client.client_side_validation and 'nodepool_id' in local_var_params and not re.search(r'^[0-9a-f]{8}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{12}$', local_var_params['nodepool_id']):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `nodepool_id` when calling `delete_cluster_nodepool`, must conform to the pattern `/^[0-9a-f]{8}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{12}$/`")  # noqa: E501
        collection_formats = {}

        path_params = {}
        if 'cluster_id' in local_var_params:
            path_params['clusterId'] = local_var_params['cluster_id']  # noqa: E501
        if 'nodepool_id' in local_var_params:
            path_params['nodepoolId'] = local_var_params['nodepool_id']  # noqa: E501

        query_params = list(local_var_params.get('query_params', {}).items())

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['basicAuth', 'tokenAuth']  # noqa: E501

        response_type = 'NodePoolResponseData'
        if 'response_type' in kwargs:
            response_type = kwargs['response_type']

        return self.api_client.call_api(
            '/clusters/{clusterId}/nodepools/{nodepoolId}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=response_type,  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats,
            _request_auth=local_var_params.get('_request_auth'))

    def get_cluster_nodepool(self, cluster_id, nodepool_id, **kwargs):  # noqa: E501
        """Retrieve a DataPlatformNodePool  # noqa: E501

        Retrieve a node pool belonging to a Kubernetes cluster running Stackable by using its ID.  The cluster ID can be found in the response when a cluster is created or when you GET a list of all DataPlatformClusters.  The node pool ID can be found in the response when a node pool is created or when you GET a list of all node pools assigned to a specific DataPlatformCluster.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_cluster_nodepool(cluster_id, nodepool_id, async_req=True)
        >>> result = thread.get()

        :param cluster_id: The unique ID of the cluster. Must conform to the UUID format.  (required)
        :type cluster_id: str
        :param nodepool_id: The unique ID of the node pool. Must conform to the UUID format.  (required)
        :type nodepool_id: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: NodePoolResponseData
        """
        kwargs['_return_http_data_only'] = True
        return self.get_cluster_nodepool_with_http_info(cluster_id, nodepool_id, **kwargs)  # noqa: E501

    def get_cluster_nodepool_with_http_info(self, cluster_id, nodepool_id, **kwargs):  # noqa: E501
        """Retrieve a DataPlatformNodePool  # noqa: E501

        Retrieve a node pool belonging to a Kubernetes cluster running Stackable by using its ID.  The cluster ID can be found in the response when a cluster is created or when you GET a list of all DataPlatformClusters.  The node pool ID can be found in the response when a node pool is created or when you GET a list of all node pools assigned to a specific DataPlatformCluster.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_cluster_nodepool_with_http_info(cluster_id, nodepool_id, async_req=True)
        >>> result = thread.get()

        :param cluster_id: The unique ID of the cluster. Must conform to the UUID format.  (required)
        :type cluster_id: str
        :param nodepool_id: The unique ID of the node pool. Must conform to the UUID format.  (required)
        :type nodepool_id: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _return_http_data_only: response data without head status code
                                       and headers
        :type _return_http_data_only: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(NodePoolResponseData, status_code(int), headers(HTTPHeaderDict))
        """

        local_var_params = locals()

        all_params = [
            'cluster_id',
            'nodepool_id'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                'response_type',
                'query_params'
            ]
        )

        for local_var_params_key, local_var_params_val in six.iteritems(local_var_params['kwargs']):
            if local_var_params_key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_cluster_nodepool" % local_var_params_key
                )
            local_var_params[local_var_params_key] = local_var_params_val
        del local_var_params['kwargs']
        # verify the required parameter 'cluster_id' is set
        if self.api_client.client_side_validation and ('cluster_id' not in local_var_params or  # noqa: E501
                                                        local_var_params['cluster_id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `cluster_id` when calling `get_cluster_nodepool`")  # noqa: E501
        # verify the required parameter 'nodepool_id' is set
        if self.api_client.client_side_validation and ('nodepool_id' not in local_var_params or  # noqa: E501
                                                        local_var_params['nodepool_id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `nodepool_id` when calling `get_cluster_nodepool`")  # noqa: E501

        if self.api_client.client_side_validation and ('cluster_id' in local_var_params and  # noqa: E501
                                                        len(local_var_params['cluster_id']) > 36):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `cluster_id` when calling `get_cluster_nodepool`, length must be less than or equal to `36`")  # noqa: E501
        if self.api_client.client_side_validation and ('cluster_id' in local_var_params and  # noqa: E501
                                                        len(local_var_params['cluster_id']) < 32):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `cluster_id` when calling `get_cluster_nodepool`, length must be greater than or equal to `32`")  # noqa: E501
        if self.api_client.client_side_validation and 'cluster_id' in local_var_params and not re.search(r'^[0-9a-f]{8}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{12}$', local_var_params['cluster_id']):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `cluster_id` when calling `get_cluster_nodepool`, must conform to the pattern `/^[0-9a-f]{8}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{12}$/`")  # noqa: E501
        if self.api_client.client_side_validation and ('nodepool_id' in local_var_params and  # noqa: E501
                                                        len(local_var_params['nodepool_id']) > 36):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `nodepool_id` when calling `get_cluster_nodepool`, length must be less than or equal to `36`")  # noqa: E501
        if self.api_client.client_side_validation and ('nodepool_id' in local_var_params and  # noqa: E501
                                                        len(local_var_params['nodepool_id']) < 32):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `nodepool_id` when calling `get_cluster_nodepool`, length must be greater than or equal to `32`")  # noqa: E501
        if self.api_client.client_side_validation and 'nodepool_id' in local_var_params and not re.search(r'^[0-9a-f]{8}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{12}$', local_var_params['nodepool_id']):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `nodepool_id` when calling `get_cluster_nodepool`, must conform to the pattern `/^[0-9a-f]{8}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{12}$/`")  # noqa: E501
        collection_formats = {}

        path_params = {}
        if 'cluster_id' in local_var_params:
            path_params['clusterId'] = local_var_params['cluster_id']  # noqa: E501
        if 'nodepool_id' in local_var_params:
            path_params['nodepoolId'] = local_var_params['nodepool_id']  # noqa: E501

        query_params = list(local_var_params.get('query_params', {}).items())

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['basicAuth', 'tokenAuth']  # noqa: E501

        response_type = 'NodePoolResponseData'
        if 'response_type' in kwargs:
            response_type = kwargs['response_type']

        return self.api_client.call_api(
            '/clusters/{clusterId}/nodepools/{nodepoolId}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=response_type,  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats,
            _request_auth=local_var_params.get('_request_auth'))

    def get_cluster_nodepools(self, cluster_id, **kwargs):  # noqa: E501
        """List the DataPlatformNodePools of a  DataPlatformCluster  # noqa: E501

        List all node pools assigned to the specified DataplatformCluster by its ID.  The cluster ID can be found in the response when a cluster is created or when you GET a list of all DataPlatformClusters.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_cluster_nodepools(cluster_id, async_req=True)
        >>> result = thread.get()

        :param cluster_id: The unique ID of the cluster. Must conform to the UUID format.  (required)
        :type cluster_id: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: NodePoolListResponseData
        """
        kwargs['_return_http_data_only'] = True
        return self.get_cluster_nodepools_with_http_info(cluster_id, **kwargs)  # noqa: E501

    def get_cluster_nodepools_with_http_info(self, cluster_id, **kwargs):  # noqa: E501
        """List the DataPlatformNodePools of a  DataPlatformCluster  # noqa: E501

        List all node pools assigned to the specified DataplatformCluster by its ID.  The cluster ID can be found in the response when a cluster is created or when you GET a list of all DataPlatformClusters.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.get_cluster_nodepools_with_http_info(cluster_id, async_req=True)
        >>> result = thread.get()

        :param cluster_id: The unique ID of the cluster. Must conform to the UUID format.  (required)
        :type cluster_id: str
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _return_http_data_only: response data without head status code
                                       and headers
        :type _return_http_data_only: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(NodePoolListResponseData, status_code(int), headers(HTTPHeaderDict))
        """

        local_var_params = locals()

        all_params = [
            'cluster_id'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                'response_type',
                'query_params'
            ]
        )

        for local_var_params_key, local_var_params_val in six.iteritems(local_var_params['kwargs']):
            if local_var_params_key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_cluster_nodepools" % local_var_params_key
                )
            local_var_params[local_var_params_key] = local_var_params_val
        del local_var_params['kwargs']
        # verify the required parameter 'cluster_id' is set
        if self.api_client.client_side_validation and ('cluster_id' not in local_var_params or  # noqa: E501
                                                        local_var_params['cluster_id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `cluster_id` when calling `get_cluster_nodepools`")  # noqa: E501

        if self.api_client.client_side_validation and ('cluster_id' in local_var_params and  # noqa: E501
                                                        len(local_var_params['cluster_id']) > 36):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `cluster_id` when calling `get_cluster_nodepools`, length must be less than or equal to `36`")  # noqa: E501
        if self.api_client.client_side_validation and ('cluster_id' in local_var_params and  # noqa: E501
                                                        len(local_var_params['cluster_id']) < 32):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `cluster_id` when calling `get_cluster_nodepools`, length must be greater than or equal to `32`")  # noqa: E501
        if self.api_client.client_side_validation and 'cluster_id' in local_var_params and not re.search(r'^[0-9a-f]{8}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{12}$', local_var_params['cluster_id']):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `cluster_id` when calling `get_cluster_nodepools`, must conform to the pattern `/^[0-9a-f]{8}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{12}$/`")  # noqa: E501
        collection_formats = {}

        path_params = {}
        if 'cluster_id' in local_var_params:
            path_params['clusterId'] = local_var_params['cluster_id']  # noqa: E501

        query_params = list(local_var_params.get('query_params', {}).items())

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['basicAuth', 'tokenAuth']  # noqa: E501

        response_type = 'NodePoolListResponseData'
        if 'response_type' in kwargs:
            response_type = kwargs['response_type']

        return self.api_client.call_api(
            '/clusters/{clusterId}/nodepools', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=response_type,  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats,
            _request_auth=local_var_params.get('_request_auth'))

    def patch_cluster_nodepool(self, cluster_id, nodepool_id, patch_node_pool_request, **kwargs):  # noqa: E501
        """Partially modify a DataPlatformNodePool  # noqa: E501

        Modifies the specified node pool of a DataPlatformCluster. Update selected attributes of a node pool belonging to a Kubernetes cluster running Stackable.  The fields in the request body are applied to the cluster. Note that the application to the node pool  itself is performed asynchronously. You can check the sync state by querying the node pool with the GET method.  The cluster ID can be found in the response when a cluster is created or when you GET a list of all DataPlatformClusters.  The node pool ID can be found in the response when a node pool is created or when you GET a list of all node pools assigned to a specific DataPlatformCluster.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.patch_cluster_nodepool(cluster_id, nodepool_id, patch_node_pool_request, async_req=True)
        >>> result = thread.get()

        :param cluster_id: The unique ID of the cluster. Must conform to the UUID format.  (required)
        :type cluster_id: str
        :param nodepool_id: The unique ID of the node pool. Must conform to the UUID format.  (required)
        :type nodepool_id: str
        :param patch_node_pool_request: Request payload with the properties that shall be applied to an existing DataPlatformNodePool.  (required)
        :type patch_node_pool_request: PatchNodePoolRequest
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: NodePoolResponseData
        """
        kwargs['_return_http_data_only'] = True
        return self.patch_cluster_nodepool_with_http_info(cluster_id, nodepool_id, patch_node_pool_request, **kwargs)  # noqa: E501

    def patch_cluster_nodepool_with_http_info(self, cluster_id, nodepool_id, patch_node_pool_request, **kwargs):  # noqa: E501
        """Partially modify a DataPlatformNodePool  # noqa: E501

        Modifies the specified node pool of a DataPlatformCluster. Update selected attributes of a node pool belonging to a Kubernetes cluster running Stackable.  The fields in the request body are applied to the cluster. Note that the application to the node pool  itself is performed asynchronously. You can check the sync state by querying the node pool with the GET method.  The cluster ID can be found in the response when a cluster is created or when you GET a list of all DataPlatformClusters.  The node pool ID can be found in the response when a node pool is created or when you GET a list of all node pools assigned to a specific DataPlatformCluster.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True

        >>> thread = api.patch_cluster_nodepool_with_http_info(cluster_id, nodepool_id, patch_node_pool_request, async_req=True)
        >>> result = thread.get()

        :param cluster_id: The unique ID of the cluster. Must conform to the UUID format.  (required)
        :type cluster_id: str
        :param nodepool_id: The unique ID of the node pool. Must conform to the UUID format.  (required)
        :type nodepool_id: str
        :param patch_node_pool_request: Request payload with the properties that shall be applied to an existing DataPlatformNodePool.  (required)
        :type patch_node_pool_request: PatchNodePoolRequest
        :param async_req: Whether to execute the request asynchronously.
        :type async_req: bool, optional
        :param _return_http_data_only: response data without head status code
                                       and headers
        :type _return_http_data_only: bool, optional
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :type _preload_content: bool, optional
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :param _request_auth: set to override the auth_settings for an a single
                              request; this effectively ignores the authentication
                              in the spec for a single request.
        :type _request_auth: dict, optional
        :return: Returns the result object.
                 If the method is called asynchronously,
                 returns the request thread.
        :rtype: tuple(NodePoolResponseData, status_code(int), headers(HTTPHeaderDict))
        """

        local_var_params = locals()

        all_params = [
            'cluster_id',
            'nodepool_id',
            'patch_node_pool_request'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout',
                '_request_auth',
                'response_type',
                'query_params'
            ]
        )

        for local_var_params_key, local_var_params_val in six.iteritems(local_var_params['kwargs']):
            if local_var_params_key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method patch_cluster_nodepool" % local_var_params_key
                )
            local_var_params[local_var_params_key] = local_var_params_val
        del local_var_params['kwargs']
        # verify the required parameter 'cluster_id' is set
        if self.api_client.client_side_validation and ('cluster_id' not in local_var_params or  # noqa: E501
                                                        local_var_params['cluster_id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `cluster_id` when calling `patch_cluster_nodepool`")  # noqa: E501
        # verify the required parameter 'nodepool_id' is set
        if self.api_client.client_side_validation and ('nodepool_id' not in local_var_params or  # noqa: E501
                                                        local_var_params['nodepool_id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `nodepool_id` when calling `patch_cluster_nodepool`")  # noqa: E501
        # verify the required parameter 'patch_node_pool_request' is set
        if self.api_client.client_side_validation and ('patch_node_pool_request' not in local_var_params or  # noqa: E501
                                                        local_var_params['patch_node_pool_request'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `patch_node_pool_request` when calling `patch_cluster_nodepool`")  # noqa: E501

        if self.api_client.client_side_validation and ('cluster_id' in local_var_params and  # noqa: E501
                                                        len(local_var_params['cluster_id']) > 36):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `cluster_id` when calling `patch_cluster_nodepool`, length must be less than or equal to `36`")  # noqa: E501
        if self.api_client.client_side_validation and ('cluster_id' in local_var_params and  # noqa: E501
                                                        len(local_var_params['cluster_id']) < 32):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `cluster_id` when calling `patch_cluster_nodepool`, length must be greater than or equal to `32`")  # noqa: E501
        if self.api_client.client_side_validation and 'cluster_id' in local_var_params and not re.search(r'^[0-9a-f]{8}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{12}$', local_var_params['cluster_id']):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `cluster_id` when calling `patch_cluster_nodepool`, must conform to the pattern `/^[0-9a-f]{8}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{12}$/`")  # noqa: E501
        if self.api_client.client_side_validation and ('nodepool_id' in local_var_params and  # noqa: E501
                                                        len(local_var_params['nodepool_id']) > 36):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `nodepool_id` when calling `patch_cluster_nodepool`, length must be less than or equal to `36`")  # noqa: E501
        if self.api_client.client_side_validation and ('nodepool_id' in local_var_params and  # noqa: E501
                                                        len(local_var_params['nodepool_id']) < 32):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `nodepool_id` when calling `patch_cluster_nodepool`, length must be greater than or equal to `32`")  # noqa: E501
        if self.api_client.client_side_validation and 'nodepool_id' in local_var_params and not re.search(r'^[0-9a-f]{8}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{12}$', local_var_params['nodepool_id']):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `nodepool_id` when calling `patch_cluster_nodepool`, must conform to the pattern `/^[0-9a-f]{8}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{12}$/`")  # noqa: E501
        collection_formats = {}

        path_params = {}
        if 'cluster_id' in local_var_params:
            path_params['clusterId'] = local_var_params['cluster_id']  # noqa: E501
        if 'nodepool_id' in local_var_params:
            path_params['nodepoolId'] = local_var_params['nodepool_id']  # noqa: E501

        query_params = list(local_var_params.get('query_params', {}).items())

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'patch_node_pool_request' in local_var_params:
            body_params = local_var_params['patch_node_pool_request']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['basicAuth', 'tokenAuth']  # noqa: E501

        response_type = 'NodePoolResponseData'
        if 'response_type' in kwargs:
            response_type = kwargs['response_type']

        return self.api_client.call_api(
            '/clusters/{clusterId}/nodepools/{nodepoolId}', 'PATCH',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=response_type,  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats,
            _request_auth=local_var_params.get('_request_auth'))
