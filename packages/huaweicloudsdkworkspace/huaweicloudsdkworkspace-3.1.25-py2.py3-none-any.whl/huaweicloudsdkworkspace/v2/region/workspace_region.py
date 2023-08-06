# coding: utf-8

import types
import six

from huaweicloudsdkcore.region.region import Region
from huaweicloudsdkcore.region.provider import RegionProviderChain

class WorkspaceRegion:
    _PROVIDER = RegionProviderChain.get_default_region_provider_chain("WORKSPACE")


    CN_EAST_3 = Region(id="cn-east-3", endpoint="https://workspace.cn-east-3.myhuaweicloud.com")

    CN_NORTH_4 = Region(id="cn-north-4", endpoint="https://workspace.cn-north-4.myhuaweicloud.com")

    CN_SOUTH_1 = Region(id="cn-south-1", endpoint="https://workspace.cn-south-1.myhuaweicloud.com")

    CN_SOUTHWEST_2 = Region(id="cn-southwest-2", endpoint="https://workspace.cn-southwest-2.myhuaweicloud.com")

    LA_SOUTH_2 = Region(id="la-south-2", endpoint="https://workspace.la-south-2.myhuaweicloud.com")

    static_fields = {
        "cn-east-3": CN_EAST_3,
        "cn-north-4": CN_NORTH_4,
        "cn-south-1": CN_SOUTH_1,
        "cn-southwest-2": CN_SOUTHWEST_2,
        "la-south-2": LA_SOUTH_2,
    }

    @classmethod
    def value_of(cls, region_id, static_fields=None):
        if not region_id:
            raise KeyError("Unexpected empty parameter: region_id.")

        fields = static_fields if static_fields else cls.static_fields

        region = cls._PROVIDER.get_region(region_id)
        if region:
            return region

        if region_id in fields:
            return fields.get(region_id)

        raise KeyError("Unexpected region_id: " + region_id)


