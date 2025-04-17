def matrices_is_similar(matrix_1: list[list[int]], matrix_2: list[list[int]]):
    if len(matrix_1) != len(matrix_2):
        return False

    for row_index in range(len(matrix_1)):
        if len(matrix_1[row_index]) != len(matrix_2[row_index]):
            return False

        for column_index in range(len(matrix_1[row_index])):
            if matrix_1[row_index][column_index] != matrix_2[row_index][column_index]:
                return False

    return True
