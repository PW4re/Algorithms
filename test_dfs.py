import unittest
from typing import List
from unittest.mock import patch

from acyclic import CycleFinder


class TestCycleFinder(unittest.TestCase):
    @patch('file_processor.FileProcessor.read_lines')
    def setUp(self, proc):
        proc.return_value = ["0"]
        self.finder = CycleFinder()

    @patch('file_processor.FileProcessor.read_lines')
    def _test_dfs(self, n, graph: List[list], expected: str, proc):
        proc.return_value = [f'{n}\n'] + list(
            map(lambda x: ' '.join(map(str, x)) + '\n', graph))
        self.finder._parse_graph()
        self.finder.dfs(1)
        self.finder.write_result()
        self.assertEqual(self.finder.result, expected)

    def test_dfs_example(self):
        self._test_dfs(4, [[2, 3], [1, 3], [1, 2, 4], [3]], 'N 1 2 3')

    def test_dfs_chain1(self):
        self._test_dfs(4, [[2], [1, 3], [2, 4], [3]], 'A')

    def test_dfs_chain2(self):
        self._test_dfs(4, [[3], [3], [1, 2, 4], [3]], 'A')

    def test_dfs_circle(self):
        self._test_dfs(3, [[2], [1, 3], [2, 1]], 'N 1 2 3')

    def test_dfs_loopback(self):
        self._test_dfs(1, [[1]], 'N 1')

    def test_dfs_loopback_long_graph(self):
        self._test_dfs(4, [[2], [1, 3], [3, 2, 4], [3]], 'N 3')

    def test_dfs_acyclic_graph(self):
        self._test_dfs(8, [[2], [1, 3, 5, 7], [2, 4, 6, 8], [3], [2], [3], [2], [3]], 'A')
