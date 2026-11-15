import json
import unittest
from pathlib import Path
from arrival_space.partner import operate, parse_time


class DomainTests(unittest.TestCase):
    def setUp(self):
        self.data=json.loads(Path('data/release.json').read_text())

    def test_existing_domain_contract(self):
        result=operate('/v1/asof',{'at':'2026-11-14T23:59:59+08:00'},self.data)
        self.assertTrue(all(row['known_at']<='2026-11-14T23:59:59+08:00' for row in result['occupancy']))
        self.assertEqual(len(result['occupancy']),160)


if __name__=='__main__':
    unittest.main()
