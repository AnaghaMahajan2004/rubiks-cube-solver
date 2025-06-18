def rotate(face, direction):
    if direction == "":
        return [face[i] for i in [6, 3, 0, 7, 4, 1, 8, 5, 2]]
    elif direction == "'":
        return [face[i] for i in [2, 5, 8, 1, 4, 7, 0, 3, 6]]
    elif direction == "2":
        return [face[i] for i in [8, 7, 6, 5, 4, 3, 2, 1, 0]]

def apply_move(cube_str, move):
    cube = list(cube_str)

    FACE_INDICES = {
        'U': list(range(0, 9)),
        'R': list(range(9, 18)),
        'F': list(range(18, 27)),
        'D': list(range(27, 36)),
        'L': list(range(36, 45)),
        'B': list(range(45, 54)),
    }

    ADJACENT = {
        'U': [[36, 37, 38], [18, 19, 20], [9, 10, 11], [45, 46, 47]],
        'D': [[24, 25, 26], [42, 43, 44], [15, 16, 17], [51, 52, 53]],
        'F': [[6, 7, 8], [38, 41, 44], [27, 28, 29], [11, 14, 17]],
        'B': [[2, 1, 0], [20, 23, 26], [33, 34, 35], [47, 50, 53]],
        'L': [[0, 3, 6], [18, 21, 24], [27, 30, 33], [45, 48, 51]],
        'R': [[8, 5, 2], [26, 23, 20], [29, 32, 35], [53, 50, 47]],
    }

    def rotate_face(face, direction):
        face_indices = FACE_INDICES[face]
        values = [cube[i] for i in face_indices]
        rotated = rotate(values, direction)
        for idx, val in zip(face_indices, rotated):
            cube[idx] = val

    def cycle(indices, direction):
        if direction == "2":
            cycle(indices, "")
            cycle(indices, "")
            return
        if direction == "'":
            indices = indices[::-1]
        temp = [cube[i] for i in indices[-1]]
        for i in range(len(indices)-1, 0, -1):
            for j in range(len(indices[i])):
                cube[indices[i][j]] = cube[indices[i-1][j]]
        for j in range(len(indices[0])):
            cube[indices[0][j]] = temp[j]

    move = move.strip()
    face = move[0]
    direction = move[1] if len(move) > 1 else ""

    rotate_face(face, direction)
    cycle(ADJACENT[face], direction)

    return ''.join(cube)