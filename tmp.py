from pprint import pprint


def nxn(n):
    array = [i for i in range(1, n ** 2 + 1)]
    coordinates = {}
    side = 'top'  # 'bottom', 'left', 'right'
    cursor = [0, 0]
    for i in array:
        coordinates[i] = cursor.copy()
        if side == 'top':
            cursor[1] += 1
            if cursor[0] + cursor[1] == n-1:
                side = 'right'
            continue
        if side == 'right':
            cursor[0] += 1
            if cursor[0] == cursor[1]:
                side = 'bottom'
            continue
        if side == 'bottom':
            cursor[1] -= 1
            if cursor[0] + cursor[1] == n-1:
                side = 'left'
            continue
        if side == 'left':
            cursor[0] -= 1
            if cursor[0] - 1 == cursor[1]:
                side = 'top'
            continue

    result = [[0 for i in range(n)] for j in range(n)]

    for item, value in coordinates.items():
        result[value[0]][value[1]] = item

    pprint(result)


nxn(10)