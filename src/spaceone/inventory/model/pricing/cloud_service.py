from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.model.pricing.data import Product
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, EnumDyField
from spaceone.inventory.libs.schema.metadata.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, \
    HTMLDynamicLayout
from spaceone.inventory.libs.schema.cloud_service import CloudServiceResource, CloudServiceResponse, CloudServiceMeta


class PricingResource(CloudServiceResource):
    cloud_service_group = StringType(default='Pricing')


class ProductResource(PricingResource):
    cloud_service_type = StringType(default='Product')
    data = ModelType(Product)


class ProductResponse(CloudServiceResponse):
    resource = PolyModelType(ProductResource)
