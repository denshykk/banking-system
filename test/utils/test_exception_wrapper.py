from unittest import TestCase
from src.utils.exception_wrapper import handle_error_format, handle_server_exception


class TestUtils(TestCase):

    def func_exc(self):
        raise ValueError('something')

    def test_handle_server_exception_with_exc(self):
        result = handle_server_exception(self.func_exc)()
        self.assertEqual(result, ({'errors': ["<class 'ValueError'>",
                                              'something',
                                              result[0].get('errors')[2]],
                                   'traceId': result[0].get('traceId')},
                                  500))

    def test_handle_error_format(self):
        result = handle_error_format('message', 'source')
        expected = {
            'traceId': result.get('traceId'),
            'errors': [
                {
                    'message': 'message',
                    'source': 'source'
                }
            ]
        }
        self.assertEqual(result, expected)
