'''
# `databricks_mws_customer_managed_keys`

Refer to the Terraform Registory for docs: [`databricks_mws_customer_managed_keys`](https://www.terraform.io/docs/providers/databricks/r/mws_customer_managed_keys).
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


class MwsCustomerManagedKeys(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.mwsCustomerManagedKeys.MwsCustomerManagedKeys",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/databricks/r/mws_customer_managed_keys databricks_mws_customer_managed_keys}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        account_id: builtins.str,
        aws_key_info: typing.Union["MwsCustomerManagedKeysAwsKeyInfo", typing.Dict[builtins.str, typing.Any]],
        use_cases: typing.Sequence[builtins.str],
        creation_time: typing.Optional[jsii.Number] = None,
        customer_managed_key_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/databricks/r/mws_customer_managed_keys databricks_mws_customer_managed_keys} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param account_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/databricks/r/mws_customer_managed_keys#account_id MwsCustomerManagedKeys#account_id}.
        :param aws_key_info: aws_key_info block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/databricks/r/mws_customer_managed_keys#aws_key_info MwsCustomerManagedKeys#aws_key_info}
        :param use_cases: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/databricks/r/mws_customer_managed_keys#use_cases MwsCustomerManagedKeys#use_cases}.
        :param creation_time: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/databricks/r/mws_customer_managed_keys#creation_time MwsCustomerManagedKeys#creation_time}.
        :param customer_managed_key_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/databricks/r/mws_customer_managed_keys#customer_managed_key_id MwsCustomerManagedKeys#customer_managed_key_id}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/databricks/r/mws_customer_managed_keys#id MwsCustomerManagedKeys#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85b412a05a46ac2c5734bf50cebac532c3a88af19b415180382188b9a2b5b969)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = MwsCustomerManagedKeysConfig(
            account_id=account_id,
            aws_key_info=aws_key_info,
            use_cases=use_cases,
            creation_time=creation_time,
            customer_managed_key_id=customer_managed_key_id,
            id=id,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putAwsKeyInfo")
    def put_aws_key_info(
        self,
        *,
        key_alias: builtins.str,
        key_arn: builtins.str,
        key_region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key_alias: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/databricks/r/mws_customer_managed_keys#key_alias MwsCustomerManagedKeys#key_alias}.
        :param key_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/databricks/r/mws_customer_managed_keys#key_arn MwsCustomerManagedKeys#key_arn}.
        :param key_region: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/databricks/r/mws_customer_managed_keys#key_region MwsCustomerManagedKeys#key_region}.
        '''
        value = MwsCustomerManagedKeysAwsKeyInfo(
            key_alias=key_alias, key_arn=key_arn, key_region=key_region
        )

        return typing.cast(None, jsii.invoke(self, "putAwsKeyInfo", [value]))

    @jsii.member(jsii_name="resetCreationTime")
    def reset_creation_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreationTime", []))

    @jsii.member(jsii_name="resetCustomerManagedKeyId")
    def reset_customer_managed_key_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomerManagedKeyId", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="awsKeyInfo")
    def aws_key_info(self) -> "MwsCustomerManagedKeysAwsKeyInfoOutputReference":
        return typing.cast("MwsCustomerManagedKeysAwsKeyInfoOutputReference", jsii.get(self, "awsKeyInfo"))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="awsKeyInfoInput")
    def aws_key_info_input(self) -> typing.Optional["MwsCustomerManagedKeysAwsKeyInfo"]:
        return typing.cast(typing.Optional["MwsCustomerManagedKeysAwsKeyInfo"], jsii.get(self, "awsKeyInfoInput"))

    @builtins.property
    @jsii.member(jsii_name="creationTimeInput")
    def creation_time_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "creationTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="customerManagedKeyIdInput")
    def customer_managed_key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customerManagedKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="useCasesInput")
    def use_cases_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "useCasesInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26cad5cad793a5e806ca8000bd211065ba0e325cab96bb20a822479c85c6df14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value)

    @builtins.property
    @jsii.member(jsii_name="creationTime")
    def creation_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "creationTime"))

    @creation_time.setter
    def creation_time(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f7ac2d6ba8fdebd285bc7a0b5f1e88b27a1b673716a23d1bd96293d9887a01a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "creationTime", value)

    @builtins.property
    @jsii.member(jsii_name="customerManagedKeyId")
    def customer_managed_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customerManagedKeyId"))

    @customer_managed_key_id.setter
    def customer_managed_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f3bb167b938262a72cf2ac8b3a56321ae6e72a0db79a24de4a6659c7dbed53c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customerManagedKeyId", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__036c52f8548fbf7b9f7df7d27bdb824ef076da8ff94a2c6a0464d3e770c8771e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="useCases")
    def use_cases(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "useCases"))

    @use_cases.setter
    def use_cases(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bde940406f51c8952868373c8c4660b1cc0b22cb5da1a629f06ac9cc203a9c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useCases", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.mwsCustomerManagedKeys.MwsCustomerManagedKeysAwsKeyInfo",
    jsii_struct_bases=[],
    name_mapping={
        "key_alias": "keyAlias",
        "key_arn": "keyArn",
        "key_region": "keyRegion",
    },
)
class MwsCustomerManagedKeysAwsKeyInfo:
    def __init__(
        self,
        *,
        key_alias: builtins.str,
        key_arn: builtins.str,
        key_region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key_alias: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/databricks/r/mws_customer_managed_keys#key_alias MwsCustomerManagedKeys#key_alias}.
        :param key_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/databricks/r/mws_customer_managed_keys#key_arn MwsCustomerManagedKeys#key_arn}.
        :param key_region: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/databricks/r/mws_customer_managed_keys#key_region MwsCustomerManagedKeys#key_region}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__847c8f2b19da49bf6684e1cdd80758aa61f5aa115c73c132bcb35c9bc127657b)
            check_type(argname="argument key_alias", value=key_alias, expected_type=type_hints["key_alias"])
            check_type(argname="argument key_arn", value=key_arn, expected_type=type_hints["key_arn"])
            check_type(argname="argument key_region", value=key_region, expected_type=type_hints["key_region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key_alias": key_alias,
            "key_arn": key_arn,
        }
        if key_region is not None:
            self._values["key_region"] = key_region

    @builtins.property
    def key_alias(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/databricks/r/mws_customer_managed_keys#key_alias MwsCustomerManagedKeys#key_alias}.'''
        result = self._values.get("key_alias")
        assert result is not None, "Required property 'key_alias' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def key_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/databricks/r/mws_customer_managed_keys#key_arn MwsCustomerManagedKeys#key_arn}.'''
        result = self._values.get("key_arn")
        assert result is not None, "Required property 'key_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def key_region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/databricks/r/mws_customer_managed_keys#key_region MwsCustomerManagedKeys#key_region}.'''
        result = self._values.get("key_region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MwsCustomerManagedKeysAwsKeyInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MwsCustomerManagedKeysAwsKeyInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.mwsCustomerManagedKeys.MwsCustomerManagedKeysAwsKeyInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1570f6a57ae5ff69f7864af976c8f7f4d80f0854fffc30533a13e45f518a5795)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKeyRegion")
    def reset_key_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyRegion", []))

    @builtins.property
    @jsii.member(jsii_name="keyAliasInput")
    def key_alias_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyAliasInput"))

    @builtins.property
    @jsii.member(jsii_name="keyArnInput")
    def key_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyArnInput"))

    @builtins.property
    @jsii.member(jsii_name="keyRegionInput")
    def key_region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyRegionInput"))

    @builtins.property
    @jsii.member(jsii_name="keyAlias")
    def key_alias(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyAlias"))

    @key_alias.setter
    def key_alias(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f00ecbdbc3caecfb749f5164068d20304d466107eaa5de1a53794b3c295c00f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyAlias", value)

    @builtins.property
    @jsii.member(jsii_name="keyArn")
    def key_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyArn"))

    @key_arn.setter
    def key_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9967d29b817145e95e5df6b72ac822cb12619ac1b1da977025ed08df7d31296)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyArn", value)

    @builtins.property
    @jsii.member(jsii_name="keyRegion")
    def key_region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyRegion"))

    @key_region.setter
    def key_region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf224486b151f40a4831a9188f38a72001a082c2de830b2e1700d1f06fc0534f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyRegion", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MwsCustomerManagedKeysAwsKeyInfo]:
        return typing.cast(typing.Optional[MwsCustomerManagedKeysAwsKeyInfo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MwsCustomerManagedKeysAwsKeyInfo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__263efa1c641edfe0d7f2aaca5c80e411029b27fde8ac217594e2196ea483958a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.mwsCustomerManagedKeys.MwsCustomerManagedKeysConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "account_id": "accountId",
        "aws_key_info": "awsKeyInfo",
        "use_cases": "useCases",
        "creation_time": "creationTime",
        "customer_managed_key_id": "customerManagedKeyId",
        "id": "id",
    },
)
class MwsCustomerManagedKeysConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        account_id: builtins.str,
        aws_key_info: typing.Union[MwsCustomerManagedKeysAwsKeyInfo, typing.Dict[builtins.str, typing.Any]],
        use_cases: typing.Sequence[builtins.str],
        creation_time: typing.Optional[jsii.Number] = None,
        customer_managed_key_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param account_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/databricks/r/mws_customer_managed_keys#account_id MwsCustomerManagedKeys#account_id}.
        :param aws_key_info: aws_key_info block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/databricks/r/mws_customer_managed_keys#aws_key_info MwsCustomerManagedKeys#aws_key_info}
        :param use_cases: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/databricks/r/mws_customer_managed_keys#use_cases MwsCustomerManagedKeys#use_cases}.
        :param creation_time: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/databricks/r/mws_customer_managed_keys#creation_time MwsCustomerManagedKeys#creation_time}.
        :param customer_managed_key_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/databricks/r/mws_customer_managed_keys#customer_managed_key_id MwsCustomerManagedKeys#customer_managed_key_id}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/databricks/r/mws_customer_managed_keys#id MwsCustomerManagedKeys#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(aws_key_info, dict):
            aws_key_info = MwsCustomerManagedKeysAwsKeyInfo(**aws_key_info)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e6c2cb3118dd1d5164a572f9c2feaacae4452eafd9060fc424b0250d34b180b)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument aws_key_info", value=aws_key_info, expected_type=type_hints["aws_key_info"])
            check_type(argname="argument use_cases", value=use_cases, expected_type=type_hints["use_cases"])
            check_type(argname="argument creation_time", value=creation_time, expected_type=type_hints["creation_time"])
            check_type(argname="argument customer_managed_key_id", value=customer_managed_key_id, expected_type=type_hints["customer_managed_key_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_id": account_id,
            "aws_key_info": aws_key_info,
            "use_cases": use_cases,
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
        if creation_time is not None:
            self._values["creation_time"] = creation_time
        if customer_managed_key_id is not None:
            self._values["customer_managed_key_id"] = customer_managed_key_id
        if id is not None:
            self._values["id"] = id

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
    def account_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/databricks/r/mws_customer_managed_keys#account_id MwsCustomerManagedKeys#account_id}.'''
        result = self._values.get("account_id")
        assert result is not None, "Required property 'account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def aws_key_info(self) -> MwsCustomerManagedKeysAwsKeyInfo:
        '''aws_key_info block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/databricks/r/mws_customer_managed_keys#aws_key_info MwsCustomerManagedKeys#aws_key_info}
        '''
        result = self._values.get("aws_key_info")
        assert result is not None, "Required property 'aws_key_info' is missing"
        return typing.cast(MwsCustomerManagedKeysAwsKeyInfo, result)

    @builtins.property
    def use_cases(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/databricks/r/mws_customer_managed_keys#use_cases MwsCustomerManagedKeys#use_cases}.'''
        result = self._values.get("use_cases")
        assert result is not None, "Required property 'use_cases' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def creation_time(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/databricks/r/mws_customer_managed_keys#creation_time MwsCustomerManagedKeys#creation_time}.'''
        result = self._values.get("creation_time")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def customer_managed_key_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/databricks/r/mws_customer_managed_keys#customer_managed_key_id MwsCustomerManagedKeys#customer_managed_key_id}.'''
        result = self._values.get("customer_managed_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/databricks/r/mws_customer_managed_keys#id MwsCustomerManagedKeys#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MwsCustomerManagedKeysConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "MwsCustomerManagedKeys",
    "MwsCustomerManagedKeysAwsKeyInfo",
    "MwsCustomerManagedKeysAwsKeyInfoOutputReference",
    "MwsCustomerManagedKeysConfig",
]

publication.publish()

def _typecheckingstub__85b412a05a46ac2c5734bf50cebac532c3a88af19b415180382188b9a2b5b969(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    account_id: builtins.str,
    aws_key_info: typing.Union[MwsCustomerManagedKeysAwsKeyInfo, typing.Dict[builtins.str, typing.Any]],
    use_cases: typing.Sequence[builtins.str],
    creation_time: typing.Optional[jsii.Number] = None,
    customer_managed_key_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__26cad5cad793a5e806ca8000bd211065ba0e325cab96bb20a822479c85c6df14(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f7ac2d6ba8fdebd285bc7a0b5f1e88b27a1b673716a23d1bd96293d9887a01a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f3bb167b938262a72cf2ac8b3a56321ae6e72a0db79a24de4a6659c7dbed53c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__036c52f8548fbf7b9f7df7d27bdb824ef076da8ff94a2c6a0464d3e770c8771e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bde940406f51c8952868373c8c4660b1cc0b22cb5da1a629f06ac9cc203a9c2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__847c8f2b19da49bf6684e1cdd80758aa61f5aa115c73c132bcb35c9bc127657b(
    *,
    key_alias: builtins.str,
    key_arn: builtins.str,
    key_region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1570f6a57ae5ff69f7864af976c8f7f4d80f0854fffc30533a13e45f518a5795(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f00ecbdbc3caecfb749f5164068d20304d466107eaa5de1a53794b3c295c00f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9967d29b817145e95e5df6b72ac822cb12619ac1b1da977025ed08df7d31296(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf224486b151f40a4831a9188f38a72001a082c2de830b2e1700d1f06fc0534f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__263efa1c641edfe0d7f2aaca5c80e411029b27fde8ac217594e2196ea483958a(
    value: typing.Optional[MwsCustomerManagedKeysAwsKeyInfo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e6c2cb3118dd1d5164a572f9c2feaacae4452eafd9060fc424b0250d34b180b(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    account_id: builtins.str,
    aws_key_info: typing.Union[MwsCustomerManagedKeysAwsKeyInfo, typing.Dict[builtins.str, typing.Any]],
    use_cases: typing.Sequence[builtins.str],
    creation_time: typing.Optional[jsii.Number] = None,
    customer_managed_key_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
