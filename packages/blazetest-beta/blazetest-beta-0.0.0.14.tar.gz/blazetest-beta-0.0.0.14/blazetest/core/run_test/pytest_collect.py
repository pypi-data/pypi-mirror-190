from typing import List

import pytest

from blazetest.core.config import CWD


class NodeIDCollector:
    node_ids: List[str] = []

    def pytest_collection_modifyitems(self, items):
        self.node_ids = [item.nodeid for item in items]


def collect_tests() -> List[str]:
    collector = NodeIDCollector()
    pytest.main([CWD, "--collect-only", "--quiet"], plugins=[collector])
    return collector.node_ids
