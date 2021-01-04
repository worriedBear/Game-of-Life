from copy import deepcopy
from time import sleep

FIELD_SIZE = 10
TIME_BETWEEN_PRINTS = 0.5

UNDERPOPULATION_LOWER_BOUNDARY = 2
UNDERPOPULATION_UPPER_BOUNDARY = 3
REPRODUCTION_BOUNDARY = 3


def main():
    # initialize matrix with zeros
    state = [[0 for col in range(FIELD_SIZE)] for row in range(FIELD_SIZE)]

    _initialize_blinker(state, 3, 3)
    _initialize_blinker(state, 6, 7)

    while _count_living_cells_(state):
        _print_state_(state)
        _update_state_(state)                      
        sleep(TIME_BETWEEN_PRINTS)

    _print_state_(state)
    return 0


def _initialize_blinker(state, starting_row, starting_col):
    state[starting_row][starting_col] = 1
    state[starting_row + 1][starting_col] = 1
    state[starting_row + 2][starting_col] = 1


def _count_living_cells_(state):
    number_living_cells = 0

    for row_index in range(FIELD_SIZE):
        for col_index in range(FIELD_SIZE):
            number_living_cells += state[row_index][col_index]
    return number_living_cells


def _print_state_(state):
    print("  - - - - - - - - - - - - - - - -")

    for row_index in range(FIELD_SIZE):
        print(" | ", end="")
        for col_index in range(FIELD_SIZE):
            if state[row_index][col_index]:
                print(" " + "O" + " ", end="")
            else:
                print(" " + " " + " ", end="")
        print("| ")

    print("  - - - - - - - - - - - - - - - -")


def _update_state_(state):
    old_state = deepcopy(state)
    neighbors = -1

    for row_index in range(FIELD_SIZE):
        for col_index in range(FIELD_SIZE):
            neighbors = _count_neighbors_(old_state, row_index, col_index)
            new_cell_state = _check_if_alive_(neighbors, state[row_index][col_index])
            state[row_index][col_index] = new_cell_state


def _check_if_alive_(number_of_neighbors, is_alive):
    if is_alive:
        if number_of_neighbors < UNDERPOPULATION_LOWER_BOUNDARY:
            return 0
        if number_of_neighbors > UNDERPOPULATION_UPPER_BOUNDARY:
            return 0

        return 1
    # else respective cell is dead
    if number_of_neighbors == REPRODUCTION_BOUNDARY:
        return 1

    return 0


def _count_neighbors_(old_state, row_index, col_index):
    number_neighbors = 0

    if 0 < row_index:
        number_neighbors += old_state[row_index - 1][col_index]
        if 0 < col_index:
            number_neighbors += old_state[row_index - 1][col_index - 1]
        if col_index < (FIELD_SIZE - 1):
            number_neighbors += old_state[row_index - 1][col_index + 1]

    if row_index < (FIELD_SIZE - 1):
        number_neighbors += old_state[row_index + 1][col_index]
        if 0 < col_index:
            number_neighbors += old_state[row_index + 1][col_index - 1]
        if col_index < (FIELD_SIZE - 1):
            number_neighbors += old_state[row_index + 1][col_index + 1]

    if 0 < col_index:
        number_neighbors += old_state[row_index][col_index - 1]
    if col_index < (FIELD_SIZE - 1):
        number_neighbors += old_state[row_index][col_index + 1]

    return number_neighbors


if __name__ == '__main__':
    main()
