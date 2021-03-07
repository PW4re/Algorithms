import sys


class FileProcessor:
    @classmethod
    def read_lines(cls, in_path):
        try:
            with open(in_path, 'r') as file:
                return list(file)
        except FileNotFoundError:
            print('Файл in.txt не найден')
            sys.exit(9)
        except IOError:
            print('Ошибка при чтении из файла')
            sys.exit(11)

    @classmethod
    def write_result(cls, out_path: str, result: str):
        try:
            with open(out_path, 'w') as file:
                file.write(result)
        except IOError:
            print('Ошибка при записи в файл')
            sys.exit(10)
