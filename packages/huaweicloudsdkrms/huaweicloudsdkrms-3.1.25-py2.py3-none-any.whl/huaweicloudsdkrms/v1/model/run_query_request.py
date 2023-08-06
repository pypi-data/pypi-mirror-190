# coding: utf-8

import re
import six



from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization


class RunQueryRequest:

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []
    sensitive_list.append('x_auth_token')

    openapi_types = {
        'x_auth_token': 'str',
        'body': 'QueryRunRequestBody'
    }

    attribute_map = {
        'x_auth_token': 'X-Auth-Token',
        'body': 'body'
    }

    def __init__(self, x_auth_token=None, body=None):
        """RunQueryRequest

        The model defined in huaweicloud sdk

        :param x_auth_token: 用户Token。 获取Token，请参考《统一身份认证服务API参考》的“获取用户Token”章节。请求响应成功后在响应消息头中包含的“X-Subject-Token”的值即为Token值。
        :type x_auth_token: str
        :param body: Body of the RunQueryRequest
        :type body: :class:`huaweicloudsdkrms.v1.QueryRunRequestBody`
        """
        
        

        self._x_auth_token = None
        self._body = None
        self.discriminator = None

        self.x_auth_token = x_auth_token
        if body is not None:
            self.body = body

    @property
    def x_auth_token(self):
        """Gets the x_auth_token of this RunQueryRequest.

        用户Token。 获取Token，请参考《统一身份认证服务API参考》的“获取用户Token”章节。请求响应成功后在响应消息头中包含的“X-Subject-Token”的值即为Token值。

        :return: The x_auth_token of this RunQueryRequest.
        :rtype: str
        """
        return self._x_auth_token

    @x_auth_token.setter
    def x_auth_token(self, x_auth_token):
        """Sets the x_auth_token of this RunQueryRequest.

        用户Token。 获取Token，请参考《统一身份认证服务API参考》的“获取用户Token”章节。请求响应成功后在响应消息头中包含的“X-Subject-Token”的值即为Token值。

        :param x_auth_token: The x_auth_token of this RunQueryRequest.
        :type x_auth_token: str
        """
        self._x_auth_token = x_auth_token

    @property
    def body(self):
        """Gets the body of this RunQueryRequest.

        :return: The body of this RunQueryRequest.
        :rtype: :class:`huaweicloudsdkrms.v1.QueryRunRequestBody`
        """
        return self._body

    @body.setter
    def body(self, body):
        """Sets the body of this RunQueryRequest.

        :param body: The body of this RunQueryRequest.
        :type body: :class:`huaweicloudsdkrms.v1.QueryRunRequestBody`
        """
        self._body = body

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
                if attr in self.sensitive_list:
                    result[attr] = "****"
                else:
                    result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        import simplejson as json
        if six.PY2:
            import sys
            reload(sys)
            sys.setdefaultencoding("utf-8")
        return json.dumps(sanitize_for_serialization(self), ensure_ascii=False)

    def __repr__(self):
        """For `print`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, RunQueryRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
