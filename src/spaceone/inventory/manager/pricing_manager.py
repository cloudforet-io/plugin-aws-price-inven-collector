import json
from spaceone.inventory.libs.manager import AWSManager
from spaceone.inventory.connector.pricing import PricingConnector
from spaceone.inventory.model.pricing.cloud_service_type import CLOUD_SERVICE_TYPES


class PricingManager(AWSManager):
    conn = None

    def __init__(self, transaction=None, **kwargs):
        super().__init__(transaction=transaction)
        self.conn: PricingConnector = self.locator.get_connector('PricingConnector', **kwargs)
        self.conn.set_client()

    def list_service_codes(self):
        services = self.conn.describe_services()
        return [service.get('ServiceCode') for service in services if service.get('ServiceCode')]

    def list_products(self, service_code):
        for product in self.conn.get_products(service_code):
            yield json.loads(product)

    @staticmethod
    def collect_cloud_service_types():
        for cloud_service_type in CLOUD_SERVICE_TYPES:
            yield cloud_service_type
