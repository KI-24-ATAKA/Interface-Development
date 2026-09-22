import argparse
import re
import sys


class Point:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        
    def __repr__(self):
        x_str = int(self.x) if self.x.is_integer() else self.x
        y_str = int(self.y) if self.y.is_integer() else self.y
        return f"Point({x_str}, {y_str})"

class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        
    def __repr__(self):
        return f"Line({self.p1}, {self.p2})"

class Circle:
    def __init__(self, center, radius):
        self.center = center
        self.radius = float(radius)
        
    def __repr__(self):
        r_str = int(self.radius) if self.radius.is_integer() else self.radius
        return f"Circle({self.center}, {r_str})"

NUM = r"-?\d+(?:\.\d+)?"

PT_RE = re.compile(fr"^Point\(\s*({NUM})\s*,\s*({NUM})\s*\)$")
LINE_RE = re.compile(fr"^Line\(\s*Point\(\s*({NUM})\s*,\s*({NUM})\s*\)\s*,\s*Point\(\s*({NUM})\s*,\s*({NUM})\s*\)\s*\)$")
CIRCLE_RE = re.compile(fr"^Circle\(\s*Point\(\s*({NUM})\s*,\s*({NUM})\s*\)\s*,\s*({NUM})\s*\)$")

def parse_line(line):
    line = line.strip()
    if not line:
        return None

    match = PT_RE.match(line)
    if match:
        return Point(match.group(1), match.group(2))
    match = LINE_RE.match(line)
    if match:
        p1 = Point(match.group(1), match.group(2))
        p2 = Point(match.group(3), match.group(4))
        return Line(p1, p2)
    match = CIRCLE_RE.match(line)
    if match:
        center = Point(match.group(1), match.group(2))
        return Circle(center, match.group(3))
    return None

def main():
    parser = argparse.ArgumentParser(description="Обработка списка геометрических фигур из файла.")
    parser.add_argument('-f', '--file', required=True, help="Путь к обрабатываемому файлу")
    parser.add_argument('-o', '--oper', required=True, choices=['print', 'count'], help="Операция над списком: print (вывод на экран) или count (подсчет объектов)")
    args = parser.parse_args()
    shapes = []

    try:
        with open(args.file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                shape = parse_line(line)
                if shape:
                    shapes.append(shape)
                else:
                    if line.strip():
                        print(f"[Warning] Пропущена некорректная строка {line_num}: {line.strip()}", file=sys.stderr)
    except FileNotFoundError:
        print(f"Ошибка: Файл '{args.file}' не найден.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Произошла ошибка при чтении файла: {e}", file=sys.stderr)
        sys.exit(1)

    if args.oper == 'print':
        for shape in shapes:
            print(shape)
    elif args.oper == 'count':
        print(f"Количество корректных объектов: {len(shapes)}")

if __name__ == "__main__":
    main()