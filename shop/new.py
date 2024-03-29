def plusy(index, coordinate):

    new_coordinates = []
    x, y = coordinate
    for i in range(index):
        y += 1
        new_coordinates.append((x, y))

    return new_coordinates


def plusx(index, coordinate):

    new_coordinates = []
    x, y = coordinate
    for i in range(index):
        x += 1
        new_coordinates.append((x, y))

    return new_coordinates


def minusy(index, coordinate):

    new_coordinates = []
    x, y = coordinate

    for i in range(index):
        y -= 1
        new_coordinates.append((x, y))

    return new_coordinates


def minusx(index, coordinate):

    new_coordinates = []
    x, y = coordinate

    for i in range(index):
        x -= 1
        new_coordinates.append((x, y))

    return new_coordinates


def robotWalk(a):
    coordinate_list = [(0, 0)]
    turn = 0

    for index, num in enumerate(a):

        if turn == 0:
            coordinates = plusy(num, coordinate_list[-1], "+")
        elif turn == 1:
            coordinates = plusx(num, coordinate_list[-1])
        elif turn == 2:
            coordinates = minusy(num, coordinate_list[-1])
        else:
            coordinates = minusx(num, coordinate_list[-1])

        for point in coordinates:
            if point in coordinate_list:
                return True

        coordinate_list.extend(coordinates)

        turn = (index + 1) % 4

    return False


print(robotWalk([34241, 23434, 2341]))
