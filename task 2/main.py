import argparse
import re
import sys

class RGB:
    def __init__(self, r, g, b):
        self.r = int(r)
        self.g = int(g)
        self.b = int(b)
    def __repr__(self):
        return f"RGB({self.r}, {self.g}, {self.b})"

    def __eq__(self, other):
        if isinstance(other, RGB):
            return (self.r, self.g, self.b) == (other.r, other.g, other.b)
        return False

class Point:
    def __init__(self, x, y, color):
        self.x = float(x)
        self.y = float(y)
        self.color = color
    def __repr__(self):
        x_str = int(self.x) if self.x.is_integer() else self.x
        y_str = int(self.y) if self.y.is_integer() else self.y
        return f"Point({x_str}, {y_str}, {self.color})"
    def has_color(self, target_color):
        return self.color == target_color

class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def __repr__(self):
        return f"Line({self.p1}, {self.p2})"

    def has_color(self, target_color):
        return self.p1.has_color(target_color) or self.p2.has_color(target_color)

class Circle:
    def __init__(self, center, radius):
        self.center = center
        self.radius = float(radius)

    def __repr__(self):
        r_str = int(self.radius) if self.radius.is_integer() else self.radius
        return f"Circle({self.center}, {r_str})"

    def has_color(self, target_color):
        return self.center.has_color(target_color)


NUM = r"-?\d+(?:\.\d+)?"
PT_INNER_RE = re.compile(fr"^\s*Point\(\s*({NUM})\s*,\s*({NUM})\s*,\s*RGB\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)\s*\)\s*$")
LINE_STRUCT_RE = re.compile(r"^\s*Line\(\s*(Point\(.*?\))\s*,\s*(Point\(.*?\))\s*\)\s*$")
CIRCLE_STRUCT_RE = re.compile(fr"^\s*Circle\(\s*(Point\(.*?\))\s*,\s*({NUM})\s*\)\s*$")


def parse_point(pt_str):
    match = PT_INNER_RE.match(pt_str)
    if not match:
        return None
    x, y = match.group(1), match.group(2)
    r, g, b = match.group(3), match.group(4), match.group(5)
    return Point(x, y, RGB(r, g, b))


def parse_line(line_str):
    line_str = line_str.strip()
    if not line_str:
        return None
    pt = parse_point(line_str)
    if pt:
        return pt
    match = LINE_STRUCT_RE.match(line_str)
    if match:
        p1 = parse_point(match.group(1))
        p2 = parse_point(match.group(2))
        if p1 and p2:
            return Line(p1, p2)
    match = CIRCLE_STRUCT_RE.match(line_str)
    if match:
        center = parse_point(match.group(1))
        radius = match.group(2)
        if center:
            return Circle(center, radius)
    return None


def parse_case_color(case_str):
    match = re.search(r"(\d+)\s*,\s*(\d+)\s*,\s*(\d+)", case_str)
    if match:
        return RGB(match.group(1), match.group(2), match.group(3))
    return None

def main():
    parser = argparse.ArgumentParser(description="Обработка геометрических фигур со строгим требованием RGB.")
    parser.add_argument('-f', '--file', required=True, help="Путь к обрабатываемому файлу")
    parser.add_argument('-o', '--oper', required=True, choices=['print', 'count', 'rem'], help="Операция: print (вывод), count (подсчет), rem (удаление)")
    parser.add_argument('-c', '--case', help="Условие фильтрации по цвету, например: 'RGB(255, 241, 67)'")
    args = parser.parse_args()

    target_color = None
    if args.case:
        target_color = parse_case_color(args.case)
        if not target_color:
            print(f"Ошибка: Не удалось распознать RGB в аргументе --case '{args.case}'", file=sys.stderr)
            sys.exit(1)

    shapes = []

    try:
        with open(args.file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                shape = parse_line(line)
                if shape:
                    shapes.append(shape)
                elif line.strip():
                    print(f"[Warning] Пропущена строка {line_num} (возможно, не указан цвет): {line.strip()}", file=sys.stderr)
    except FileNotFoundError:
        print(f"Ошибка: Файл '{args.file}' не найден.", file=sys.stderr)
        sys.exit(1)

    filtered_shapes = shapes
    if target_color:
        filtered_shapes = [s for s in shapes if s.has_color(target_color)]

    if args.oper == 'print':
        for shape in filtered_shapes:
            print(shape)

    elif args.oper == 'count':
        print(f"Количество объектов: {len(filtered_shapes)}")

    elif args.oper == 'rem':
        if target_color:
            remaining_shapes = [s for s in shapes if not s.has_color(target_color)]
            with open(args.file, 'w', encoding='utf-8') as f:
                for shape in remaining_shapes:
                    f.write(f"{shape}\n")
            print(f"Удалено объектов по условию {target_color}: {len(shapes) - len(remaining_shapes)}")
        else:
            open(args.file, 'w', encoding='utf-8').close()
            print("Файл полностью очищен.")

if __name__ == "__main__":
    main()