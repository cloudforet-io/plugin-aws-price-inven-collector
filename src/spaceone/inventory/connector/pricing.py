import logging
from spaceone.inventory.libs.connector import AWSConnector
from spaceone.inventory.error import *

__all__ = ['PricingConnector']
_LOGGER = logging.getLogger(__name__)


class PricingConnector(AWSConnector):
    service = 'pricing'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def describe_services(self, **query):
        services = []
        query = self.generate_query(is_paginate=False, **query)
        paginator = self.client.get_paginator('describe_services')

        response_iterator = paginator.paginate(**query)

        for data in response_iterator:
            services.extend(data.get('Services', []))

        return services

    def get_products(self, service_code, **query):
        query = self.generate_query(is_paginate=False, **query)
        paginator = self.client.get_paginator('get_products')
        response_iterator = paginator.paginate(ServiceCode=service_code, **query)

        index = 0
        for data in response_iterator:
            index = index + 1

            if service_code == 'AmazonEC2':
                print(index)

            prices = data.get('PriceList', [])
            for price in prices:
                yield price

    def get_attribute_values(self, service_code, attribute_name, **query):
        attribute_values = []
        query = self.generate_query(is_paginate=False, **query)
        paginator = self.client.get_paginator('get_attribute_values')
        response_iterator = paginator.paginate(ServiceCode=service_code, AttributeName=attribute_name, **query)

        for data in response_iterator:
            attribute_values.extend(data.get('AttributeValues', []))

        return attribute_values
