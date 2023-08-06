'''
# `data_newrelic_notification_destination`

Refer to the Terraform Registory for docs: [`data_newrelic_notification_destination`](https://www.terraform.io/docs/providers/newrelic/d/notification_destination).
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from .._jsii import *

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class DataNewrelicNotificationDestination(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.dataNewrelicNotificationDestination.DataNewrelicNotificationDestination",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/newrelic/d/notification_destination newrelic_notification_destination}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        id: builtins.str,
        account_id: typing.Optional[jsii.Number] = None,
        active: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        auth_basic: typing.Optional[typing.Union["DataNewrelicNotificationDestinationAuthBasic", typing.Dict[builtins.str, typing.Any]]] = None,
        auth_token: typing.Optional[typing.Union["DataNewrelicNotificationDestinationAuthToken", typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        property: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataNewrelicNotificationDestinationProperty", typing.Dict[builtins.str, typing.Any]]]]] = None,
        type: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/newrelic/d/notification_destination newrelic_notification_destination} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param id: The ID of the destination. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/d/notification_destination#id DataNewrelicNotificationDestination#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param account_id: The account ID under which to put the destination. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/d/notification_destination#account_id DataNewrelicNotificationDestination#account_id}
        :param active: Indicates whether the destination is active. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/d/notification_destination#active DataNewrelicNotificationDestination#active}
        :param auth_basic: auth_basic block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/d/notification_destination#auth_basic DataNewrelicNotificationDestination#auth_basic}
        :param auth_token: auth_token block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/d/notification_destination#auth_token DataNewrelicNotificationDestination#auth_token}
        :param name: The name of the destination. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/d/notification_destination#name DataNewrelicNotificationDestination#name}
        :param property: property block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/d/notification_destination#property DataNewrelicNotificationDestination#property}
        :param type: The type of the destination. One of: (WEBHOOK, EMAIL, SERVICE_NOW, PAGERDUTY_ACCOUNT_INTEGRATION, PAGERDUTY_SERVICE_INTEGRATION, JIRA, SLACK, SLACK_COLLABORATION, SLACK_LEGACY, MOBILE_PUSH, EVENT_BRIDGE). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/d/notification_destination#type DataNewrelicNotificationDestination#type}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5eedddc6b06660f8195509d19b188a0d0a3db209d0e2aaf061798d22f92cc9a0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataNewrelicNotificationDestinationConfig(
            id=id,
            account_id=account_id,
            active=active,
            auth_basic=auth_basic,
            auth_token=auth_token,
            name=name,
            property=property,
            type=type,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putAuthBasic")
    def put_auth_basic(self, *, user: typing.Optional[builtins.str] = None) -> None:
        '''
        :param user: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/d/notification_destination#user DataNewrelicNotificationDestination#user}.
        '''
        value = DataNewrelicNotificationDestinationAuthBasic(user=user)

        return typing.cast(None, jsii.invoke(self, "putAuthBasic", [value]))

    @jsii.member(jsii_name="putAuthToken")
    def put_auth_token(self, *, prefix: typing.Optional[builtins.str] = None) -> None:
        '''
        :param prefix: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/d/notification_destination#prefix DataNewrelicNotificationDestination#prefix}.
        '''
        value = DataNewrelicNotificationDestinationAuthToken(prefix=prefix)

        return typing.cast(None, jsii.invoke(self, "putAuthToken", [value]))

    @jsii.member(jsii_name="putProperty")
    def put_property(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataNewrelicNotificationDestinationProperty", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d55a21235e7c044323690af7d6f134c4dcac99715b23d7de764b5e4926c4002)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putProperty", [value]))

    @jsii.member(jsii_name="resetAccountId")
    def reset_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountId", []))

    @jsii.member(jsii_name="resetActive")
    def reset_active(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActive", []))

    @jsii.member(jsii_name="resetAuthBasic")
    def reset_auth_basic(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthBasic", []))

    @jsii.member(jsii_name="resetAuthToken")
    def reset_auth_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthToken", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetProperty")
    def reset_property(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProperty", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="authBasic")
    def auth_basic(
        self,
    ) -> "DataNewrelicNotificationDestinationAuthBasicOutputReference":
        return typing.cast("DataNewrelicNotificationDestinationAuthBasicOutputReference", jsii.get(self, "authBasic"))

    @builtins.property
    @jsii.member(jsii_name="authToken")
    def auth_token(
        self,
    ) -> "DataNewrelicNotificationDestinationAuthTokenOutputReference":
        return typing.cast("DataNewrelicNotificationDestinationAuthTokenOutputReference", jsii.get(self, "authToken"))

    @builtins.property
    @jsii.member(jsii_name="lastSent")
    def last_sent(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastSent"))

    @builtins.property
    @jsii.member(jsii_name="property")
    def property(self) -> "DataNewrelicNotificationDestinationPropertyList":
        return typing.cast("DataNewrelicNotificationDestinationPropertyList", jsii.get(self, "property"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="activeInput")
    def active_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "activeInput"))

    @builtins.property
    @jsii.member(jsii_name="authBasicInput")
    def auth_basic_input(
        self,
    ) -> typing.Optional["DataNewrelicNotificationDestinationAuthBasic"]:
        return typing.cast(typing.Optional["DataNewrelicNotificationDestinationAuthBasic"], jsii.get(self, "authBasicInput"))

    @builtins.property
    @jsii.member(jsii_name="authTokenInput")
    def auth_token_input(
        self,
    ) -> typing.Optional["DataNewrelicNotificationDestinationAuthToken"]:
        return typing.cast(typing.Optional["DataNewrelicNotificationDestinationAuthToken"], jsii.get(self, "authTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="propertyInput")
    def property_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataNewrelicNotificationDestinationProperty"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataNewrelicNotificationDestinationProperty"]]], jsii.get(self, "propertyInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85458621b2808db51167210c0d421a817360dc953fe14d445527d8a84acbb943)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value)

    @builtins.property
    @jsii.member(jsii_name="active")
    def active(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "active"))

    @active.setter
    def active(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ca54dced8b558898f2a43e36824ca1b152803a9e9af091851b9fa6c551ff20f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "active", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86d0e477d1ebcc5c02ddc22762414486a8245b1783d2f220fbb6ade7de5af740)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb821d02b75993c564f89b397b8cbb0826a0838ec08d090227cd36ae87499b00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c31662d137f1323c526f980b7d50f07eaf6e95b1108e137e7f9007f39c3ebf4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.dataNewrelicNotificationDestination.DataNewrelicNotificationDestinationAuthBasic",
    jsii_struct_bases=[],
    name_mapping={"user": "user"},
)
class DataNewrelicNotificationDestinationAuthBasic:
    def __init__(self, *, user: typing.Optional[builtins.str] = None) -> None:
        '''
        :param user: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/d/notification_destination#user DataNewrelicNotificationDestination#user}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b5e76517b37dbc44995a6f6d729469f65bb9b734f970ce106ff3b096ae5a70a)
            check_type(argname="argument user", value=user, expected_type=type_hints["user"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if user is not None:
            self._values["user"] = user

    @builtins.property
    def user(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/d/notification_destination#user DataNewrelicNotificationDestination#user}.'''
        result = self._values.get("user")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataNewrelicNotificationDestinationAuthBasic(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataNewrelicNotificationDestinationAuthBasicOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.dataNewrelicNotificationDestination.DataNewrelicNotificationDestinationAuthBasicOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d0a4631eac4373b13a67db8c37965f3138402eefd12d52754b0ab23a1a41734)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetUser")
    def reset_user(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUser", []))

    @builtins.property
    @jsii.member(jsii_name="userInput")
    def user_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userInput"))

    @builtins.property
    @jsii.member(jsii_name="user")
    def user(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "user"))

    @user.setter
    def user(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41d3b5b01293ddadb502427e73afe28d2daa872c392cfcca024c65e7f3f7a85e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "user", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataNewrelicNotificationDestinationAuthBasic]:
        return typing.cast(typing.Optional[DataNewrelicNotificationDestinationAuthBasic], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataNewrelicNotificationDestinationAuthBasic],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65afa8e4492ae80adf53ca3f603b3efc1a689577e9aaff98b62f68db589e86ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.dataNewrelicNotificationDestination.DataNewrelicNotificationDestinationAuthToken",
    jsii_struct_bases=[],
    name_mapping={"prefix": "prefix"},
)
class DataNewrelicNotificationDestinationAuthToken:
    def __init__(self, *, prefix: typing.Optional[builtins.str] = None) -> None:
        '''
        :param prefix: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/d/notification_destination#prefix DataNewrelicNotificationDestination#prefix}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cadb29552bc22da84a72a9f3c7194837bb3455eeb1d836ee5b404d86ae347590)
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if prefix is not None:
            self._values["prefix"] = prefix

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/d/notification_destination#prefix DataNewrelicNotificationDestination#prefix}.'''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataNewrelicNotificationDestinationAuthToken(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataNewrelicNotificationDestinationAuthTokenOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.dataNewrelicNotificationDestination.DataNewrelicNotificationDestinationAuthTokenOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cffc3d50ac296ce5e78310bed6b132c5622ac400797f6733973eaefa8b15fafc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPrefix")
    def reset_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefix", []))

    @builtins.property
    @jsii.member(jsii_name="prefixInput")
    def prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefixInput"))

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefix"))

    @prefix.setter
    def prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22f9af1a3bfc954ccf3fe93502bf2b059eadf3fab93f5ec54e03bcd332315555)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataNewrelicNotificationDestinationAuthToken]:
        return typing.cast(typing.Optional[DataNewrelicNotificationDestinationAuthToken], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataNewrelicNotificationDestinationAuthToken],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81727c94ae4e56b24e468eab3e761fb5a50998b24cdbcbbf575a1d1ddab17c18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.dataNewrelicNotificationDestination.DataNewrelicNotificationDestinationConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "id": "id",
        "account_id": "accountId",
        "active": "active",
        "auth_basic": "authBasic",
        "auth_token": "authToken",
        "name": "name",
        "property": "property",
        "type": "type",
    },
)
class DataNewrelicNotificationDestinationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: builtins.str,
        account_id: typing.Optional[jsii.Number] = None,
        active: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        auth_basic: typing.Optional[typing.Union[DataNewrelicNotificationDestinationAuthBasic, typing.Dict[builtins.str, typing.Any]]] = None,
        auth_token: typing.Optional[typing.Union[DataNewrelicNotificationDestinationAuthToken, typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        property: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataNewrelicNotificationDestinationProperty", typing.Dict[builtins.str, typing.Any]]]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param id: The ID of the destination. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/d/notification_destination#id DataNewrelicNotificationDestination#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param account_id: The account ID under which to put the destination. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/d/notification_destination#account_id DataNewrelicNotificationDestination#account_id}
        :param active: Indicates whether the destination is active. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/d/notification_destination#active DataNewrelicNotificationDestination#active}
        :param auth_basic: auth_basic block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/d/notification_destination#auth_basic DataNewrelicNotificationDestination#auth_basic}
        :param auth_token: auth_token block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/d/notification_destination#auth_token DataNewrelicNotificationDestination#auth_token}
        :param name: The name of the destination. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/d/notification_destination#name DataNewrelicNotificationDestination#name}
        :param property: property block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/d/notification_destination#property DataNewrelicNotificationDestination#property}
        :param type: The type of the destination. One of: (WEBHOOK, EMAIL, SERVICE_NOW, PAGERDUTY_ACCOUNT_INTEGRATION, PAGERDUTY_SERVICE_INTEGRATION, JIRA, SLACK, SLACK_COLLABORATION, SLACK_LEGACY, MOBILE_PUSH, EVENT_BRIDGE). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/d/notification_destination#type DataNewrelicNotificationDestination#type}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(auth_basic, dict):
            auth_basic = DataNewrelicNotificationDestinationAuthBasic(**auth_basic)
        if isinstance(auth_token, dict):
            auth_token = DataNewrelicNotificationDestinationAuthToken(**auth_token)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b86b6fa42761a3abf1229e402deb30f0981cb70840f02339434bade16fbfc94)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument active", value=active, expected_type=type_hints["active"])
            check_type(argname="argument auth_basic", value=auth_basic, expected_type=type_hints["auth_basic"])
            check_type(argname="argument auth_token", value=auth_token, expected_type=type_hints["auth_token"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument property", value=property, expected_type=type_hints["property"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if account_id is not None:
            self._values["account_id"] = account_id
        if active is not None:
            self._values["active"] = active
        if auth_basic is not None:
            self._values["auth_basic"] = auth_basic
        if auth_token is not None:
            self._values["auth_token"] = auth_token
        if name is not None:
            self._values["name"] = name
        if property is not None:
            self._values["property"] = property
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def id(self) -> builtins.str:
        '''The ID of the destination.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/d/notification_destination#id DataNewrelicNotificationDestination#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account_id(self) -> typing.Optional[jsii.Number]:
        '''The account ID under which to put the destination.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/d/notification_destination#account_id DataNewrelicNotificationDestination#account_id}
        '''
        result = self._values.get("account_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def active(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates whether the destination is active.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/d/notification_destination#active DataNewrelicNotificationDestination#active}
        '''
        result = self._values.get("active")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def auth_basic(
        self,
    ) -> typing.Optional[DataNewrelicNotificationDestinationAuthBasic]:
        '''auth_basic block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/d/notification_destination#auth_basic DataNewrelicNotificationDestination#auth_basic}
        '''
        result = self._values.get("auth_basic")
        return typing.cast(typing.Optional[DataNewrelicNotificationDestinationAuthBasic], result)

    @builtins.property
    def auth_token(
        self,
    ) -> typing.Optional[DataNewrelicNotificationDestinationAuthToken]:
        '''auth_token block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/d/notification_destination#auth_token DataNewrelicNotificationDestination#auth_token}
        '''
        result = self._values.get("auth_token")
        return typing.cast(typing.Optional[DataNewrelicNotificationDestinationAuthToken], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the destination.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/d/notification_destination#name DataNewrelicNotificationDestination#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def property(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataNewrelicNotificationDestinationProperty"]]]:
        '''property block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/d/notification_destination#property DataNewrelicNotificationDestination#property}
        '''
        result = self._values.get("property")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataNewrelicNotificationDestinationProperty"]]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of the destination. One of: (WEBHOOK, EMAIL, SERVICE_NOW, PAGERDUTY_ACCOUNT_INTEGRATION, PAGERDUTY_SERVICE_INTEGRATION, JIRA, SLACK, SLACK_COLLABORATION, SLACK_LEGACY, MOBILE_PUSH, EVENT_BRIDGE).

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/d/notification_destination#type DataNewrelicNotificationDestination#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataNewrelicNotificationDestinationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.dataNewrelicNotificationDestination.DataNewrelicNotificationDestinationProperty",
    jsii_struct_bases=[],
    name_mapping={
        "key": "key",
        "value": "value",
        "display_value": "displayValue",
        "label": "label",
    },
)
class DataNewrelicNotificationDestinationProperty:
    def __init__(
        self,
        *,
        key: builtins.str,
        value: builtins.str,
        display_value: typing.Optional[builtins.str] = None,
        label: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key: Notification property key. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/d/notification_destination#key DataNewrelicNotificationDestination#key}
        :param value: Notification property value. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/d/notification_destination#value DataNewrelicNotificationDestination#value}
        :param display_value: Notification property display key. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/d/notification_destination#display_value DataNewrelicNotificationDestination#display_value}
        :param label: Notification property label. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/d/notification_destination#label DataNewrelicNotificationDestination#label}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9148c56fd614823010c51fcdd968b9f4785f64dcba93ecfac6e165ee867c5c2d)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument display_value", value=display_value, expected_type=type_hints["display_value"])
            check_type(argname="argument label", value=label, expected_type=type_hints["label"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "value": value,
        }
        if display_value is not None:
            self._values["display_value"] = display_value
        if label is not None:
            self._values["label"] = label

    @builtins.property
    def key(self) -> builtins.str:
        '''Notification property key.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/d/notification_destination#key DataNewrelicNotificationDestination#key}
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Notification property value.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/d/notification_destination#value DataNewrelicNotificationDestination#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_value(self) -> typing.Optional[builtins.str]:
        '''Notification property display key.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/d/notification_destination#display_value DataNewrelicNotificationDestination#display_value}
        '''
        result = self._values.get("display_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def label(self) -> typing.Optional[builtins.str]:
        '''Notification property label.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/d/notification_destination#label DataNewrelicNotificationDestination#label}
        '''
        result = self._values.get("label")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataNewrelicNotificationDestinationProperty(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataNewrelicNotificationDestinationPropertyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.dataNewrelicNotificationDestination.DataNewrelicNotificationDestinationPropertyList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdf988133cd4db03e89515a546e6d79a8496c60f40236f837e94546ed4a4ec2b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataNewrelicNotificationDestinationPropertyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ae523fae5f6f3120746a830fc6fb579ff257f2920b343f926e12f395e20ab5a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataNewrelicNotificationDestinationPropertyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ac9214c860356a0886ca6428be14f3593f86030cacef0e65bf2440a1dfb13d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41d613f66aa7842c41a43d4843d63e7b554e90c3d2f47b9a6c854dbdfcbf6d1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36079604249c337f5de77b4e5cdb80b5e72583b347c5eaa85bfead05ae88b181)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataNewrelicNotificationDestinationProperty]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataNewrelicNotificationDestinationProperty]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataNewrelicNotificationDestinationProperty]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbc08d6318ba85e1b246f0ac5d11d5d8b3ac71b7efce20a28b410f9445b7d15c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataNewrelicNotificationDestinationPropertyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.dataNewrelicNotificationDestination.DataNewrelicNotificationDestinationPropertyOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c5a5bfb74f4bc7c040ca2af4735afcf01f80474298ac8edc860714d8415ba13)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDisplayValue")
    def reset_display_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayValue", []))

    @jsii.member(jsii_name="resetLabel")
    def reset_label(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabel", []))

    @builtins.property
    @jsii.member(jsii_name="displayValueInput")
    def display_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayValueInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="labelInput")
    def label_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "labelInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="displayValue")
    def display_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayValue"))

    @display_value.setter
    def display_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e90521f14b2a91f760567213944a8956a082b5307034fd089da64228fc5114a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayValue", value)

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4be532192014a60be84f57777bd17464c1c3cef92f2663a5aeae389627ff93fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value)

    @builtins.property
    @jsii.member(jsii_name="label")
    def label(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "label"))

    @label.setter
    def label(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e25fe650cf68dccb1dc43a1baad4b6d66373c3e3fd87e84729f295a0d14e5544)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "label", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9408a787f2b48b0a56b7c58ddae1cc4a7e2d341de23523ba1a4d99c5c7f0333)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[DataNewrelicNotificationDestinationProperty, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[DataNewrelicNotificationDestinationProperty, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[DataNewrelicNotificationDestinationProperty, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf7a1bcf1c8e694d6b24bde0fffb4d8429b87b8329b3e9bbf83ed0f3c2fc24da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "DataNewrelicNotificationDestination",
    "DataNewrelicNotificationDestinationAuthBasic",
    "DataNewrelicNotificationDestinationAuthBasicOutputReference",
    "DataNewrelicNotificationDestinationAuthToken",
    "DataNewrelicNotificationDestinationAuthTokenOutputReference",
    "DataNewrelicNotificationDestinationConfig",
    "DataNewrelicNotificationDestinationProperty",
    "DataNewrelicNotificationDestinationPropertyList",
    "DataNewrelicNotificationDestinationPropertyOutputReference",
]

publication.publish()

def _typecheckingstub__5eedddc6b06660f8195509d19b188a0d0a3db209d0e2aaf061798d22f92cc9a0(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    id: builtins.str,
    account_id: typing.Optional[jsii.Number] = None,
    active: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    auth_basic: typing.Optional[typing.Union[DataNewrelicNotificationDestinationAuthBasic, typing.Dict[builtins.str, typing.Any]]] = None,
    auth_token: typing.Optional[typing.Union[DataNewrelicNotificationDestinationAuthToken, typing.Dict[builtins.str, typing.Any]]] = None,
    name: typing.Optional[builtins.str] = None,
    property: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataNewrelicNotificationDestinationProperty, typing.Dict[builtins.str, typing.Any]]]]] = None,
    type: typing.Optional[builtins.str] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d55a21235e7c044323690af7d6f134c4dcac99715b23d7de764b5e4926c4002(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataNewrelicNotificationDestinationProperty, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85458621b2808db51167210c0d421a817360dc953fe14d445527d8a84acbb943(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ca54dced8b558898f2a43e36824ca1b152803a9e9af091851b9fa6c551ff20f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86d0e477d1ebcc5c02ddc22762414486a8245b1783d2f220fbb6ade7de5af740(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb821d02b75993c564f89b397b8cbb0826a0838ec08d090227cd36ae87499b00(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c31662d137f1323c526f980b7d50f07eaf6e95b1108e137e7f9007f39c3ebf4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b5e76517b37dbc44995a6f6d729469f65bb9b734f970ce106ff3b096ae5a70a(
    *,
    user: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d0a4631eac4373b13a67db8c37965f3138402eefd12d52754b0ab23a1a41734(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41d3b5b01293ddadb502427e73afe28d2daa872c392cfcca024c65e7f3f7a85e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65afa8e4492ae80adf53ca3f603b3efc1a689577e9aaff98b62f68db589e86ee(
    value: typing.Optional[DataNewrelicNotificationDestinationAuthBasic],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cadb29552bc22da84a72a9f3c7194837bb3455eeb1d836ee5b404d86ae347590(
    *,
    prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cffc3d50ac296ce5e78310bed6b132c5622ac400797f6733973eaefa8b15fafc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22f9af1a3bfc954ccf3fe93502bf2b059eadf3fab93f5ec54e03bcd332315555(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81727c94ae4e56b24e468eab3e761fb5a50998b24cdbcbbf575a1d1ddab17c18(
    value: typing.Optional[DataNewrelicNotificationDestinationAuthToken],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b86b6fa42761a3abf1229e402deb30f0981cb70840f02339434bade16fbfc94(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: builtins.str,
    account_id: typing.Optional[jsii.Number] = None,
    active: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    auth_basic: typing.Optional[typing.Union[DataNewrelicNotificationDestinationAuthBasic, typing.Dict[builtins.str, typing.Any]]] = None,
    auth_token: typing.Optional[typing.Union[DataNewrelicNotificationDestinationAuthToken, typing.Dict[builtins.str, typing.Any]]] = None,
    name: typing.Optional[builtins.str] = None,
    property: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataNewrelicNotificationDestinationProperty, typing.Dict[builtins.str, typing.Any]]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9148c56fd614823010c51fcdd968b9f4785f64dcba93ecfac6e165ee867c5c2d(
    *,
    key: builtins.str,
    value: builtins.str,
    display_value: typing.Optional[builtins.str] = None,
    label: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdf988133cd4db03e89515a546e6d79a8496c60f40236f837e94546ed4a4ec2b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ae523fae5f6f3120746a830fc6fb579ff257f2920b343f926e12f395e20ab5a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ac9214c860356a0886ca6428be14f3593f86030cacef0e65bf2440a1dfb13d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41d613f66aa7842c41a43d4843d63e7b554e90c3d2f47b9a6c854dbdfcbf6d1d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36079604249c337f5de77b4e5cdb80b5e72583b347c5eaa85bfead05ae88b181(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbc08d6318ba85e1b246f0ac5d11d5d8b3ac71b7efce20a28b410f9445b7d15c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataNewrelicNotificationDestinationProperty]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c5a5bfb74f4bc7c040ca2af4735afcf01f80474298ac8edc860714d8415ba13(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e90521f14b2a91f760567213944a8956a082b5307034fd089da64228fc5114a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4be532192014a60be84f57777bd17464c1c3cef92f2663a5aeae389627ff93fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e25fe650cf68dccb1dc43a1baad4b6d66373c3e3fd87e84729f295a0d14e5544(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9408a787f2b48b0a56b7c58ddae1cc4a7e2d341de23523ba1a4d99c5c7f0333(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf7a1bcf1c8e694d6b24bde0fffb4d8429b87b8329b3e9bbf83ed0f3c2fc24da(
    value: typing.Optional[typing.Union[DataNewrelicNotificationDestinationProperty, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
