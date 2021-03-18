import time
import logging
import re
import concurrent.futures

from spaceone.core.service import *
from spaceone.inventory.libs.schema.base import ReferenceModel
from spaceone.inventory.manager.pricing_manager import PricingManager
from spaceone.inventory.model.pricing.data import Product
from spaceone.inventory.model.pricing.cloud_service import ProductResource, ProductResponse


_LOGGER = logging.getLogger(__name__)
MAX_WORKER = 20
SUPPORTED_FEATURES = []
SUPPORTED_RESOURCE_TYPE = ['inventory.CloudService', 'inventory.CloudServiceType']
DEFAULT_REGION = 'us-east-1'
FILTER_FORMAT = []


@authentication_handler
class CollectorService(BaseService):
    def __init__(self, metadata):
        super().__init__(metadata)

    @check_required(['options'])
    def init(self, params):
        """ init plugin by options
        """
        capability = {
            'filter_format': FILTER_FORMAT,
            'supported_resource_type': SUPPORTED_RESOURCE_TYPE,
            'supported_features': SUPPORTED_FEATURES
        }
        return {'metadata': capability}

    @transaction
    @check_required(['options', 'secret_data'])
    def verify(self, params):
        """
        Args:
              params:
                - options
                - secret_data
        """
        options = params['options']
        secret_data = params.get('secret_data', {})

        if not secret_data:
            self.get_account_id(secret_data)

        return {}

    @transaction
    @check_required(['options', 'secret_data', 'filter'])
    def list_resources(self, params):
        """
        Args:
            params:
                - options
                - secret_data
                - filter
        """
        start_time = time.time()
        pricing_mgr: PricingManager = self.locator.get_manager('PricingManager', **params)

        for cloud_service_type in pricing_mgr.collect_cloud_service_types():
            yield cloud_service_type.to_primitive()

        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKER) as executor:
            future_executors = []
            for service_code in pricing_mgr.list_service_codes():
                future_executors.append(executor.submit(self.set_product, pricing_mgr, service_code))

            for future in concurrent.futures.as_completed(future_executors):
                try:
                    for resource in future.result():
                        yield resource.to_primitive()
                except Exception as e:
                    _LOGGER.error(f'failed to result {e}')

        print(f'TOTAL TIME : {time.time() - start_time} Seconds')

    def set_product(self, pricing_mgr, service_code):
        # print(f'--- START @@@ {service_code} @@@')
        for product in pricing_mgr.list_products(service_code):
            # print(product.get('product', {}).get('sku'))

            try:
                product_dic = {
                    'service_code': product.get('serviceCode'),
                    'region_name': self.get_region_name_from_location(product.get('product', {}).get('attributes', {}).get('location', '')),
                    'product_family': product.get('product', {}).get('productFamily'),
                    'sku': product.get('product', {}).get('sku'),
                    # 'attributes': product.get('product', {}).get('attributes'),
                    'attributes': self.set_product_attributes(product.get('product', {}).get('attributes')),
                    'publication_date': product.get('publicationDate'),
                    'version': product.get('version'),
                    'terms': self.get_terms(product.get('terms', {}))
                }

                product_data = Product(product_dic, strict=False)
                proudct_resource = ProductResource({
                    'data': product_data,
                    'region_code': product_dic['region_name'],
                    'reference': ReferenceModel(product_data.reference())
                })

                # print(f'##### {product_data.get("service_code")}: {product_data.get("sku")}')

                yield ProductResponse({
                    'resource': proudct_resource
                })

            except Exception as e:
                print(f"[[ ERROR ]] {e}")

        # print(f'--- END @@@ {service_code} @@@')

    def get_terms(self, terms):
        return_terms = []
        for term_type, term in terms.items():
            for k, term_info in term.items():
                term_dic = {
                    'effective_date': term_info.get('effectiveDate', ''),
                    'offer_term_code': term_info.get('offerTermCode', ''),
                    'term_type': term_type,
                    'price_dimensions': self.get_price_dimensions(term_info.get('priceDimensions', {})),
                    'term_attributes': term_info.get('termAttributes', {})
                }
                return_terms.append(term_dic)

        return return_terms

    def get_price_dimensions(self, price_dimensions):
        dimensions = []
        for k, price_dimension in price_dimensions.items():
            price_dimension.update({
                'price_dimension_code': self.get_price_dimension_code(price_dimension.get('rateCode'))
            })

            if price_per_unit := self.convert_price_per_unit(price_dimension.get('pricePerUnit')):
                price_dimension.update({'pricePerUnit': {'USD': price_per_unit}})

            dimensions.append(price_dimension)

        return dimensions

    def set_product_attributes(self, attributes):
        if attributes is None:
            return None

        if 'dedicatedEbsThroughput' in attributes:
            try:
                if throughput := self.convert_throughput_attribute(attributes.get('dedicatedEbsThroughput')):
                    attributes.update({'dedicatedEbsThroughput': throughput})
            except Exception as e:
                pass

        if 'vcpu' in attributes:
            try:
                if vcpu := self.convert_vcpu_attribute(attributes.get('vcpu')):
                    attributes.update({'vcpu': vcpu})
            except Exception as e:
                pass

        if 'gpu' in attributes:
            try:
                if gpu := self.convert_gpu_attribute(attributes.get('gpu')):
                    attributes.update({'gpu': gpu})
            except Exception as e:
                pass

        if 'memory' in attributes:
            try:
                if memory := self.convert_memory_attribute(attributes.get('memory')):
                    attributes.update({'memory': memory})
            except Exception as e:
                pass

        if 'storage' in attributes:
            try:
                if storage_info := self.convert_storage_attribute(attributes.get('storage')):
                    attributes.update({
                        'storageType': storage_info.get('storage_type'),
                        'stroageSize': storage_info.get('storage_size'),
                        'sotrageCount': storage_info.get('storage_count'),
                    })
            except Exception as e:
                pass

        return attributes

    @staticmethod
    def get_region_name_from_location(location):
        REGION_CODE_MAP = {
            'US East (N. Virginia)': 'us-east-1',
            'US East (Ohio)': 'us-east-2',
            'US West (N. California)': 'us-west-1',
            'US West (Oregon)': 'us-west-2',
            'Africa (Cape Town)': 'af-south-1',
            'Asia Pacific (Hong Kong)': 'ap-east-1',
            'Asia Pacific (Mumbai)': 'ap-south-1',
            'Asia Pacific (Osaka-Local)': 'ap-northeast-3',
            'Asia Pacific (Seoul)': 'ap-northeast-2',
            'Asia Pacific (Singapore)': 'ap-southeast-1',
            'Asia Pacific (Sydney)': 'ap-southeast-2',
            'Asia Pacific (Tokyo)': 'ap-northeast-1',
            'Canada (Central)': 'ca-central-1',
            'China (Beijing)': 'cn-north-1',
            'China (Ningxia)': 'cn-northwest-1',
            'EU (Frankfurt)': 'eu-central-1',
            'EU (Ireland)': 'eu-west-1',
            'EU (London)': 'eu-west-2',
            'EU (Milan)': 'eu-south-1',
            'EU (Paris)': 'eu-west-3',
            'EU (Stockholm)': 'eu-north-1',
            'Middle East (Bahrain)': 'me-south-1',
            'South America (Sao Paulo)': 'sa-east-1',
            'AWS GovCloud (US-East)': 'us-gov-east-1',
            'AWS GovCloud (US-West)': 'us-gov-west-1',
            'AWS GovCloud (US)': 'us-gov-west-1',
            'Any': 'global'
        }

        return REGION_CODE_MAP.get(location.strip(), '')

    @staticmethod
    def get_price_dimension_code(rate_code):
        if rate_code:
            return rate_code.split('.')[-1]
        else:
            return ''

    @staticmethod
    def convert_vcpu_attribute(vcpu):
        if vcpu:
            return int(vcpu.strip())
        else:
            return None

    @staticmethod
    def convert_gpu_attribute(gpu):
        if gpu:
            return int(gpu.strip())
        else:
            return None

    @staticmethod
    def convert_memory_attribute(memory):
        if memory:
            return int(re.sub(' GiB', '', memory).strip())
        else:
            return None

    @staticmethod
    def convert_storage_attribute(storage):
        storage_size = 0
        storage_count = 0

        if storage:
            if 'EBS' in storage:
                return {
                    'storage_type': 'EBS',
                    'storage_size': storage_size,
                    'storage_count': storage_count
                }
            elif 'SSD' in storage:
                # pattern 1 : "2 x 150 SSD"
                # pattern 2 : "4 x 300 NVMe SSD"
                # pattern 3 : "1200 GB NVMe SSD"

                storage_split = re.split(' ', storage)
                if storage_split[1] == 'x':
                    storage_size = int(storage_split[2])
                    storage_count = int(storage_split[0])
                else:
                    storage_size = int(storage_split[0])
                    storage_count = 1

                return {
                    'storage_type': 'SSD',
                    'storage_size': storage_size,
                    'storage_count': storage_count
                }
        else:
            return None

    @staticmethod
    def convert_throughput_attribute(throughput):
        # pattern 1 : "Up to 2120 Mbps"
        # pattern 2 : "2000 Mbps"
        if throughput:
            remove_mbps = re.sub(' Mbps', '', throughput)
            throughput_value_only = re.sub('Up to ', '', remove_mbps)
            return int(throughput_value_only)
        else:
            return None

    @staticmethod
    def convert_price_per_unit(price_per_unit):
        if price_per_unit:
            if usd := price_per_unit.get('USD'):
                return float(usd)
        return None
