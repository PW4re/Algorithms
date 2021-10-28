from functools import reduce

IN_FILE = 'in.txt'
OUT_FILE = 'out.txt'
MAGIC_FINAL_CONSTANT = 32767


def vertices_with_weights(sublist): return dict([(x, y) for x, y in zip(sublist[::2], sublist[1::2])])


def parse_input():
    """Читает из файла граф, заданный массивом смежности, и возвращает списки смежности"""
    graph = [(-1, -1)]
    with open(IN_FILE, 'r') as f:
        n = int(f.readline())
        all_adj_arr = [0] + [int(x) for x in reduce(list.__add__, (line.split() for line in list(f)))]

    number_of_vertices = all_adj_arr[1]
    # бежим по индексной части:
    for i in range(1, number_of_vertices - 1):
        graph.append(vertices_with_weights(all_adj_arr[all_adj_arr[i]:all_adj_arr[i + 1]]))

    if all_adj_arr[all_adj_arr[number_of_vertices - 1]] != MAGIC_FINAL_CONSTANT:
        print('Что-то не так с форматом входного файла или с разбором оного')
        exit(31)

    return graph


def min_accretion(dist, unused):
    m = float('+inf')
    res = -1
    for v in unused:
        if dist[v] < m:
            m = dist[v]
            res = v

    return res


def find_spanning_tree(graph):
    spanning_tree = []
    n = len(graph) - 1
    near = [1 for _ in range(n + 1)]  # start_vertex = 1
    dist = [graph[1][v] if v in graph[1] else float('+inf') for v in range(n + 1)]
    unused = set(range(2, n + 1))

    while len(spanning_tree) != n - 1:
        v = min_accretion(dist, unused)
        u = near[v]
        spanning_tree.append((v, u))
        unused.remove(v)

        for x in unused:
            if v in graph[x] and dist[x] > graph[x][v]:
                near[x] = v
                dist[x] = graph[x][v]

    return spanning_tree


def write_result():
    graph = parse_input()
    spanning_tree = find_spanning_tree(graph)
    spanning_tree_weight = reduce(int.__add__, [graph[u][v] for u, v in spanning_tree])
    with open(OUT_FILE, 'w') as f:
        for i in range(1, len(graph)):
            print(' '.join(sorted(str(v) if u == i else str(u) for u, v in spanning_tree if u == i or v == i)) + ' 0', file=f)
        print(spanning_tree_weight, file=f)


if __name__ == '__main__':
    write_result()
