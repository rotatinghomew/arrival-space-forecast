import copy
import json
import threading
import unittest
from pathlib import Path
from arrival_space.provider import make_server
from arrival_space.partner import operate
from arrival_space.wire import call, RemoteFailure


class DomainHTTPTests(unittest.TestCase):
    def setUp(self):
        self.data=json.loads(Path('data/release.json').read_text())
        self.source=make_server(('127.0.0.1',0),self.data)
        self.thread=threading.Thread(target=self.source.serve_forever,daemon=True)
        self.thread.start()
        self.base=f'http://127.0.0.1:{self.source.server_port}'
        self.payload={'at': '2026-11-14T23:59:59+08:00'}

    def tearDown(self):
        self.source.shutdown()
        self.source.server_close()
        self.thread.join()

    def test_domain_protocol_matches_local_contract(self):
        result=call(self.base,'/v1/asof',{'revision':'release-1',**self.payload})
        expected=operate('/v1/asof',self.payload,self.data)
        self.assertEqual(result,expected)
        self.assertIn('occupancy',result)

    def test_domain_revision_is_required(self):
        with self.assertRaises(RemoteFailure):
            call(self.base,'/v1/asof',{'revision':'old-release',**self.payload})

    def test_query_does_not_rewrite_published_data(self):
        before=copy.deepcopy(self.data)
        operate('/v1/asof',self.payload,self.data)
        self.assertEqual(before,self.data)


if __name__=='__main__':
    unittest.main()
