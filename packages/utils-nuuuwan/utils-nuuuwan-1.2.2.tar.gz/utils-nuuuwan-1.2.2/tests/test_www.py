import os
import unittest

from utils import WWW, CSVFile, File, JSONFile, TSVFile

DIR_TESTS = 'tests'


URL_BASE = os.path.join(
    'https://raw.githubusercontent.com',
    'nuuuwan/utils',
    'main/tests',
)


def get_test_file(ext: str) -> str:
    return os.path.join(DIR_TESTS, f'data.{ext}')


def get_test_url(ext: str) -> str:
    return os.path.join(URL_BASE, f'data.{ext}')


class TestCase(unittest.TestCase):
    def test_read_binary(self):
        self.assertEqual(
            File(get_test_file('png')).readBinary(),
            WWW(get_test_url('png')).readBinary(),
        )

        with self.assertRaises(Exception):
            WWW(get_test_url('png') + '.1234').readBinary()

    def test_read_selenium(self):
        content = WWW(get_test_url('html')).readSelenium()
        self.assertIn(
            'This is a test',
            content,
        )

    def test_read(self):
        self.assertEqual(
            File(get_test_file('txt')).read(),
            WWW(get_test_url('txt')).read(),
        )

    def test_read_json(self):
        self.assertEqual(
            JSONFile(get_test_file('json')).read(),
            WWW(get_test_url('json')).readJSON(),
        )

    def test_read_xsv(self):
        self.assertEqual(
            TSVFile(get_test_file('tsv')).read(),
            WWW(get_test_url('tsv')).readXSV('\t'),
        )

    def test_read_tsv(self):
        self.assertEqual(
            TSVFile(get_test_file('tsv')).read(),
            WWW(get_test_url('tsv')).readTSV(),
        )

    def test_read_csv(self):
        self.assertEqual(
            CSVFile(get_test_file('csv')).read(),
            WWW(get_test_url('csv')).readCSV(),
        )

    def test_download_binary(self):
        url = get_test_url('png')
        tmp_file_name = '/tmp/data.png'
        WWW(url).downloadBinary(tmp_file_name)
        self.assertEqual(
            File(get_test_file('png')).readBinary(),
            File(tmp_file_name).readBinary(),
        )

    def test_exists(self):
        url = get_test_url('png')
        self.assertTrue(WWW(url).exists)
        self.assertFalse(WWW(url + '.1234').exists)
