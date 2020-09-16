import unittest
import subprocess
import re
import uuid

from jsonrpc_client.jsonrpc.JsonRpcMessages import Request, Response, Notification, make_response, BatchRequest


class TestCli(unittest.TestCase):
    id1 = str(uuid.uuid1())

    def test_basic_notification_message_build(self):
        self.assertEqual(Notification.show_registered_handlers(), {
                         'jsonrpc': '2.0', 'method': 'show_registered_handlers'})
        self.assertEqual(Notification.test_list_params(1, 2, 3), {
                         'jsonrpc': '2.0', 'method': 'test_list_params', 'params': [1, 2, 3]})
        self.assertEqual(Notification.test_names_params(name='Traffic', value='Server'), {
                         'jsonrpc': '2.0', 'method': 'test_names_params', 'params': {'name': 'Traffic', 'value': 'Server'}})
        self.assertEqual(Notification.custom(some=[1, 2, 4], stuff={'ok': 'yes'}), {
                         'jsonrpc': '2.0', 'method': 'custom', 'params': {'some': [1, 2, 4], 'stuff': {'ok': 'yes'}}})

    def test_basic_request_message_build(self):
        id1 = str(uuid.uuid1())
        self.assertEqual(Request.m(id=id1), {
                         'jsonrpc': '2.0', 'method': 'm', 'id': id1})
        self.assertEqual(Request.show_registered_handlers(id=id1), {
                         'jsonrpc': '2.0', 'method': 'show_registered_handlers', 'id': id1})
        self.assertEqual(Request.test_list_params(1, 2, 3, id=id1), {
                         'jsonrpc': '2.0', 'method': 'test_list_params', 'params': [1, 2, 3], 'id': id1})

        # self.assertEqual(Request.test_list_params([1, 2, 3], id=id1), {
        #                  'jsonrpc': '2.0', 'method': 'test_list_params', 'params': [1, 2, 3], 'id': id1})
        self.assertEqual(
            Request.test_names_params(
                name='Traffic', value='Server', id=id1), {
                'jsonrpc': '2.0', 'method': 'test_names_params', 'params': {
                    'name': 'Traffic', 'value': 'Server'}, 'id': id1})
        self.assertEqual(Request.custom(some=[1, 2, 4], stuff={'ok': 'yes'}, id=id1), {
                         'jsonrpc': '2.0', 'method': 'custom', 'params': {'some': [1, 2, 4], 'stuff': {'ok': 'yes'}}, 'id': id1})

    def test_basic_response_build(self):
        id1 = str(uuid.uuid1())
        rsp = Response(
            text=f'{{"jsonrpc": "2.0", "result": {{"name": "proxy.config.diags.debug.enabled", "record_type": "1"}}, "id": "{id1}"}}')
        self.assertEqual(rsp.is_error(), False)
        self.assertEqual(rsp.is_Ok(), True)
        self.assertEqual(rsp.jsonrpc, '2.0')
        self.assertEqual(rsp.id, id1)
        self.assertEqual(rsp.result['name'],
                         "proxy.config.diags.debug.enabled")
        self.assertEqual(rsp.result['record_type'], "1")

    def test_basic_response_build_error_single_data(self):
        id1 = str(uuid.uuid1())

        rsp = Response(
            text=f'{{"jsonrpc": "2.0", "error": {{"code": 9, "message": "Error during execution", "data": {{"code": 2000, "message": "Record not found."}}}}, "id": "{id1}"}}')

        self.assertEqual(rsp.is_error(), True)
        self.assertEqual(rsp.is_Ok(), False)
        self.assertEqual(rsp.jsonrpc, '2.0')
        self.assertEqual(rsp.id, id1)
        self.assertEqual(rsp.error['code'], 9)
        self.assertEqual(rsp.error['message'], "Error during execution")

        data = rsp.error['data']
        if isinstance(data, list):
            for e in data:
                self.assertEqual(e['code'], 2000)
                self.assertEqual(e['message'], "Record not found.")
        else:
            self.assertEqual(data['code'], 2000)
            self.assertEqual(data['message'], "Record not found.")

    def test_basic_response_build_error(self):
        id1 = str(uuid.uuid1())

        rsp = Response(
            text=f'{{"jsonrpc": "2.0", "error": {{"code": 9, "message": "Error during execution", "data": [{{"code": 2000, "message": "Record not found."}}]}}, "id": "{id1}"}}')

        self.assertEqual(rsp.is_error(), True)
        self.assertEqual(rsp.is_Ok(), False)
        self.assertEqual(rsp.jsonrpc, '2.0')
        self.assertEqual(rsp.id, id1)
        self.assertEqual(rsp.error['code'], 9)
        self.assertEqual(rsp.error['message'], "Error during execution")
        data = rsp.error['data']
        if isinstance(data, list):
            for e in data:
                self.assertEqual(e['code'], 2000)
                self.assertEqual(e['message'], "Record not found.")
        else:
            self.assertEqual(data['code'], 2000)
            self.assertEqual(data['message'], "Record not found.")

    def test_basic_batch_responses(self):
        id1 = str(uuid.uuid1())
        rsp = make_response(
            '[{"jsonrpc": "2.0", "result": {"name": "item1", "record_type": "1"}, "id": "1"}, {"jsonrpc": "2.0", "result": {"name": "item2", "record_type": "1"}, "id": "2"}]')

        if isinstance(rsp, list):
            # batch
            i = 1
            for r in rsp:
                self.assertEqual(r.is_error(), False)
                self.assertEqual(r.is_Ok(), True)
                self.assertEqual(r.jsonrpc, '2.0')
                self.assertEqual(r.id, str(i))
                self.assertEqual(r.result['name'], f'item{i}')
                i += 1
                self.assertEqual(r.result['record_type'], "1")

    def test_basic_batch_request_build(self):
        req1 = Request.method1(1, 2, 3)
        req2 = Request.method2(4, 5, 6)
        req3 = Request.method3(7, 8, 9)
        not1 = Notification.notify(restart=True)

        batch = BatchRequest()
        batch.add_request(req1)
        batch.add_request(req2)
        batch.add_request(req3)
        batch.add_request(not1)

        batch2 = BatchRequest(req1, req2, req3, not1)

        self.assertEqual(len(batch), 4)
        self.assertEqual(len(batch2), 4)
        self.assertEqual(len(batch), len(batch2))
        self.assertEqual(str(batch), str(batch2))


if __name__ == '__main__':
    unittest.main()
