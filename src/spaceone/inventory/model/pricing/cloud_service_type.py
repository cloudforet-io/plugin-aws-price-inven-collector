from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, SearchField, EnumDyField
from spaceone.inventory.libs.schema.cloud_service_type import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta


cst_price = CloudServiceTypeResource()
cst_price.name = 'Product'
cst_price.provider = 'aws'
cst_price.group = 'Pricing'
cst_price.labels = ['Management']
cst_price.tags = {}

cst_price._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Service Code', 'data.service_code'),
        TextDyField.data_source('Product Family', 'data.product_family'),
        TextDyField.data_source('Region', 'data.region_name'),
        TextDyField.data_source('SKU', 'data.sku'),
    ],
    search=[]
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_price}),
]
