from typing import List

from file_processor import FileProcessor


class CycleFinder:
    """Внутри этого класса руководствуемся правилами по просмотру
     и вытаскиванию в первую очередь вершины с наименьшим номером"""

    def __init__(self):
        self.graph: List[list] = [[0]]
        self.checked: set = set()
        self.stack: List[int] = []
        self.father: list
        self._parse_graph()
        self._cycle: set = set()
        self.result: str = 'A'

    @staticmethod
    def _get_adjacency_list(s_list: List[str]):
        return list(sorted(filter(lambda x: x != 0, map(int, s_list))))

    def _parse_graph(self):
        lines = FileProcessor.read_lines('in.txt')
        n = int(lines[0])
        self.father = [0] * (n + 1)
        for i in range(1, n + 1):
            self.graph.append(self._get_adjacency_list(lines[i].split(' ')))

    def dfs(self, vertex: int):
        self.stack.append(vertex)
        while self.stack:
            current_vertex = self.stack[-1]
            self.checked.add(current_vertex)
            for v in self.graph[current_vertex]:
                if v not in self.checked:
                    self.father[v] = current_vertex
                    self.stack.append(v)
                    break
                elif current_vertex >= v != self.father[current_vertex]:
                    self._find_cycle(v, current_vertex)
                    self.result = 'N'
                    print("В графе есть цикл!")
                    return
            else:
                self.stack.pop()

    def _find_cycle(self, s_vertex: int, f_vertex: int):
        current_vertex = f_vertex
        self._cycle.add(current_vertex)
        while current_vertex != s_vertex:
            current_vertex = self.father[current_vertex]
            self._cycle.add(current_vertex)

    def write_result(self):
        if self.result == 'N':
            cycle_vertices: list = list(map(str, sorted(self._cycle)))
            self.result += f' {" ".join(cycle_vertices)}'
        FileProcessor.write_result('out.txt', self.result)


if __name__ == '__main__':
    finder = CycleFinder()
    finder.dfs(1)
    finder.write_result()
    # finder.build_plot()
