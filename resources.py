# resources.py
from dataclasses import dataclass
from typing import Dict
import logging
# import json

logger = logging.getLogger(__name__)
logging.basicConfig(filename='resources.log',
                    encoding='utf-8',
                    format='%(asctime)s %(message)s',
                    level=logging.DEBUG)

logger.info('Resources module imported')
logger.debug('Resources module imported')


@dataclass
class Resources:
    compute_points: int = 100
    network_bandwidth: int = 50
    storage_capacity: int = 10
    memory_capacity: int = 128
    latency_measure: int = 5
    security_level: int = 3
    data_integrity: int = 95

    def has_sufficient(self, available: Dict[str, int]) -> bool:
        logger.debug('Resources module imported')
        return (self.compute_points >= available.get('compute', 0) and
                self.network_bandwidth >= available.get('network', 0) and
                self.storage_capacity >= available.get('storage', 0))

    def consume(self, cost: Dict[str, int]) -> bool:
        logger.debug('Resources module imported')
        if self.has_sufficient(cost):
            self.compute_points -= cost.get('compute')
            self.network_bandwidth -= cost.get('network')
            self.storage_capacity -= cost.get('storage')
            return f"Resources consumed: {cost}"
        return False


myrss = Resources(10, 10, 10, 10, 10, 10)
print(myrss.has_sufficient({'compute': 10, 'network': 10, 'storage': 10}))
print(myrss.consume({'compute': 10, 'network': 10, 'storage': 10}))
