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
    search=[
        SearchField.set(name='Service Code', key='data.service_code'),
        SearchField.set(name='Region', key='data.region_name'),
        SearchField.set(name='Product Family', key='data.product_family'),
        SearchField.set(name='SKU', key='data.sku'),
        SearchField.set(name='Physical Processor', key='data.attributes.physicalProcessor'),
        SearchField.set(name='Processor Features', key='data.attributes.processorFeatures'),
        SearchField.set(name='Instance Type', key='data.attributes.instanceType'),
        SearchField.set(name='Instance Family', key='data.attributes.instanceFamily'),
        SearchField.set(name='Operating System', key='data.attributes.operatingSystem'),
        SearchField.set(name='vcpu', key='data.attributes.vcpu', data_type='integer'),
        SearchField.set(name='memory', key='data.attributes.memory', data_type='integer'),
        SearchField.set(name='gpu', key='data.attributes.gpu', data_type='integer'),
        SearchField.set(name='EC2 Storage Type', key='data.attributes.storageType'),
        SearchField.set(name='EC2 Storage Size', key='data.attributes.storageSize', data_type='integer'),
        SearchField.set(name='EC2 Storage Count', key='data.attributes.storageCount', data_type='integer'),
        SearchField.set(name='Dedicated EBS Throughput', key='data.attributes.dedicatedEbsThroughput',
                        data_type='integer'),
        SearchField.set(name='Price per Unit (USD)', key='data.terms.price_dimensions.price_per_unit.USD',
                        data_type='float'),
    ]
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_price}),
]
