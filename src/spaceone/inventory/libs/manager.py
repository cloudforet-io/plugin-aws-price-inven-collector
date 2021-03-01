from spaceone.core.manager import BaseManager
from spaceone.inventory.libs.connector import AWSConnector


class AWSManager(BaseManager):

    def __init__(self, transaction=None, **kwargs):
        super().__init__(transaction=transaction)

    def verify(self, options, secret_data, **kwargs):
        """ Check collector's status.
        """
        connector: AWSConnector = self.locator.get_connector('AWSConnector', secret_data=secret_data)
        connector.verify()

    def collect_cloud_service_type(self):
        for cloud_service_type in self.cloud_service_types:
            yield cloud_service_type
