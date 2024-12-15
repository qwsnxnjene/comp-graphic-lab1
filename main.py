import numpy as np


def read_obj(file_path):
    vertices = []
    faces = []
    with open(file_path, 'r') as f:
        for line in f:
            elems = line.strip().split()
            if len(elems) == 0:
                continue
            if elems[0] == 'v':
                coords = list(map(float, elems[1:3]))
                vertices.append(coords)
            elif elems[0] == 'f':
                indices = [int(index) - 1 for index in elems[1:]]
                faces.append(indices)
    return np.array(vertices), np.array(faces)


def is_convex(quadrilateral):
    points = quadrilateral
    cross = []
    for i in range(len(points)):
        p1 = points[i]
        p2 = points[(i + 1) % 4]
        p3 = points[(i + 2) % 4]  # замыкание вершин четырехугольника
        cp = (p2[0] - p1[0]) * (p3[1] - p2[1]) - (p2[1] - p1[1]) * (p3[0] - p2[0])
        cross.append(cp)
    # проверяем выпуклость путём проверки знаков векторных произведений
    return all(cp > 0 for cp in cross) or all(cp < 0 for cp in cross)


def shoelace_area(polygon):
    # находим площадь многоугольника по формуле шнурования(идём по точкам в порядке их соединения)
    n = len(polygon)
    area = 0.0
    for i in range(n):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % n]  # реализуем замыкание(xn+1 = x0)
        area += (x1 * y2 - x2 * y1)
    return abs(area) * 0.5 if area != 0.0 else 999  # мин. площадь получается слишком маленькой,
    # она округляется до нуля, для этого делаю защиту, чтобы минимум не занулился


# Main execution
def main():
    vertices, faces = read_obj('teapot.obj')

    # словарь рёбер и граней, ключом будет выступать пара вершин, образующих ребро,
    # а значением - список граней, использующих это ребро
    edge_to_faces = {}
    for face_idx, face in enumerate(faces):
        v1, v2, v3 = face
        edges = [(v1, v2), (v2, v3), (v3, v1)]
        for edge in edges:
            # Order the vertices in the edge tuple
            edge_sorted = tuple(sorted(edge))
            if edge_sorted not in edge_to_faces:
                edge_to_faces[edge_sorted] = []
            edge_to_faces[edge_sorted].append(face_idx)

    # ищем ребра, которые используются ровно двумя гранями(общие ребра)
    internal_edges = [edge for edge, faces in edge_to_faces.items() if len(faces) == 2]

    max_convex_area = 0
    min_non_convex_area = float('inf')

    for edge in internal_edges:
        # получаем две грани, которые используют общее ребро
        face1_idx, face2_idx = edge_to_faces[edge]
        face1 = faces[face1_idx]
        face2 = faces[face2_idx]

        # собираем список вершин без повторов
        vertices_indices = set(face1).union(set(face2))
        vertices_indices = sorted(vertices_indices)
        quadrilateral = vertices[list(vertices_indices)]

        if len(quadrilateral) != 4:
            continue

        convex = is_convex(quadrilateral)
        area = shoelace_area(quadrilateral)

        # если четырехугольник - выпуклый и нынешняя площадь больше максимума, обновляем максимум
        if convex and area > max_convex_area:
            max_convex_area = area

        # если четырехугольник - невыпуклый и нынешняя площадь меньше минимума, обновляем минимум
        if not convex and area < min_non_convex_area:
            min_non_convex_area = area

    # Output the results
    print(f"наибольшая площадь среди выпуклых четырехугольников: {max_convex_area}")
    print(f"наименьшая площадь среди невыпуклых четырехугольников: {min_non_convex_area}")


if __name__ == "__main__":
    main()
