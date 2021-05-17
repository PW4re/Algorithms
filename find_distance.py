from typing import List, Tuple
from math import inf


class FileWorker:
    def __init__(self, in_path: str, out_path: str):
        self.in_path = in_path
        self.out_path = out_path

    def read_graph(self) -> Tuple[int, int, int, list]:
        graph = [[]]
        with open(self.in_path, 'r') as f:
            n = int(f.readline())
            for _ in range(n):
                graph.append(self._parse_adjacency(f.readline(), n))
            start = int(f.readline())
            finish = int(f.readline())

        return n, start, finish, graph

    # noinspection PyTypeChecker
    @staticmethod
    def _parse_adjacency(line: str, n: int) -> List[int]:
        res = [inf for _ in range(n + 1)]  # нужен лист длины n+1
        # отбросим завершающий нуль:
        parts = [int(x) for x in line.split()[:-1]]
        for i in range(0, len(parts), 2):
            res[parts[i]] = parts[i + 1]

        return res

    def write_result(self, result: Tuple[bool, list]):
        with open(self.out_path, 'w') as f:
            if result[0]:
                f.write('Y\n')
                f.write(' '.join([str(v) for v in reversed(result[1])]) + '\n')
                f.write(str(sum(result[1])))
            else:
                f.write('N')


class PathFinder:
    """Использует алгоритм Форда-Беллмана"""
    def __init__(self, n: int, start: int, finish: int, graph: List[list]):
        self.n: int = n
        self.graph: List[list] = graph
        self.start: int = start
        self.finish: int = finish

    def _distance(self) -> Tuple[list, list]:
        distance = [inf for _ in range(self.n + 1)]
        distance[self.start] = 0
        previous = [inf for _ in range(self.n + 1)]
        previous[self.start] = 0

        for v in range(1, self.n + 1):
            if v == self.start or self.graph[self.start][v] == inf:
                continue
            # правый элемент пары - вес:
            distance[v] = self.graph[self.start][v]
            previous[v] = self.start

        for k in range(1, self.n - 2):
            for v in range(1, self.n + 1):
                if v == self.start:
                    continue
                for w in range(1, self.n + 1):
                    if distance[w] + self.graph[w][v] < distance[v]:
                        distance[v] = distance[w] + self.graph[w][v]
                        previous[v] = w

        return distance, previous

    def find_path(self) -> Tuple[bool, list]:
        """Для текущих start и finish"""
        distance, previous = self._distance()
        result_stack = []
        if distance[self.finish] < inf:
            result_stack.append(self.finish)
            v = self.finish
            while previous[v] != 0:
                v = previous[v]
                result_stack.append(v)
        else:
            return False, []

        return True, result_stack


if __name__ == '__main__':
    f_worker = FileWorker('in.txt', 'out.txt')
    path_finder = PathFinder(*f_worker.read_graph())
    f_worker.write_result(path_finder.find_path())
