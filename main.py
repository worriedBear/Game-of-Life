from copy import deepcopy
from random import randint

FIELD_SIZE = 15
SIMULATION_LENGTH = 100
NUMBER_OF_SIMULATIONS = 20

UNDERPOPULATION_LOWER_BOUNDARY = 2
UNDERPOPULATION_UPPER_BOUNDARY = 3
REPRODUCTION_BOUNDARY = 3


def main():
    file = open("simulations.txt", "a+")

    for simulation_index in range(NUMBER_OF_SIMULATIONS):
        _simulate_single_run_(simulation_index, file)

    file.close()


def _simulate_single_run_(nr_runs, file):
    nr_iterations = SIMULATION_LENGTH
    abort_run = False

    # initialize matrix with zeros
    state = [[0 for col in range(FIELD_SIZE)] for row in range(FIELD_SIZE)]
    _initialize_randomly_(state)
    starting_state = deepcopy(state)

    for it in range(SIMULATION_LENGTH):
        previous_state = deepcopy(state)
        _update_state_(state)
        # if the game isn't progressing anymore, end the simulation
        if state == previous_state:
            nr_iterations = it
            break
        # if all cells are dead, abort the simulation
        if not _count_living_cells_(state):
            abort_run = True
            nr_iterations = it
            break

    if abort_run:
        _append_abort_message_to_file_(nr_iterations, nr_runs, file)
        return

    _append_run_header_to_file_(nr_iterations, nr_runs, file)
    file.write("          [Starting field:]\n")
    _append_state_to_file_(starting_state, file)
    file.write("          [Ending field:]\n")
    _append_state_to_file_(state, file)
    file.write("////////////////////////////////////////////////////\n\n\n\n\n\n")


def _append_abort_message_to_file_(nr_iterations, nr_runs, file):
    file.write("////////////////////////////////////////////////////\n")
    file.write("    + + + + + + + + + + + + + + + +")
    file.write("\n    + ALL CELLS DEAD AFTER " + str(nr_iterations) + " iterations")
    file.write("\n    + Simulation index: " + str(nr_runs))
    file.write("\n    + + + + + + + + + + + + + + + +\n")
    file.write("////////////////////////////////////////////////////\n\n\n\n\n\n")


def _append_run_header_to_file_(nr_iterations, nr_runs, file):
    file.write("////////////////////////////////////////////////////\n")
    file.write("    + + + + + + + + + + + + + + + +")
    file.write("\n    + Number of iterations: " + str(nr_iterations))
    file.write("\n    + Simulation index: " + str(nr_runs))
    file.write("\n    + + + + + + + + + + + + + + + +\n")


def _append_state_to_file_(state, file):
    file.write("  ")
    for it in range(int(1.5 * FIELD_SIZE)):
        file.write("- ")
    file.write("-\n")

    for row_index in range(FIELD_SIZE):
        file.write(" | ")
        for col_index in range(FIELD_SIZE):
            if state[row_index][col_index]:
                file.write(" " + "O" + " ")
            else:
                file.write(" " + " " + " ")
        file.write("| \n")

    file.write("  ")
    for it in range(int(1.5 * FIELD_SIZE)):
        file.write("- ",)
    file.write("-\n")


def _initialize_randomly_(state):
    for row_index in range(FIELD_SIZE):
        for col_index in range(FIELD_SIZE):
            state[row_index][col_index] = randint(0, 1)


def _initialize_blinker_(state, starting_row, starting_col):
    state[starting_row][starting_col] = 1
    state[starting_row + 1][starting_col] = 1
    state[starting_row + 2][starting_col] = 1


def _initialize_cool_figure_(state, starting_row, starting_col):
    state[starting_row][starting_col + 1] = 1
    state[starting_row + 1][starting_col + 1] = 1
    state[starting_row][starting_col +2] = 1
    state[starting_row + 1][starting_col] = 1
    state[starting_row + 2][starting_col + 1] = 1


def _count_living_cells_(state):
    number_living_cells = 0

    for row_index in range(FIELD_SIZE):
        for col_index in range(FIELD_SIZE):
            number_living_cells += state[row_index][col_index]
    return number_living_cells


def _print_state_(state):
    print("  ", end="")
    for it in range(int(1.5 * FIELD_SIZE)):
        print("- ", end="")
    print("-")

    for row_index in range(FIELD_SIZE):
        print(" | ", end="")
        for col_index in range(FIELD_SIZE):
            if state[row_index][col_index]:
                print(" " + "O" + " ", end="")
            else:
                print(" " + " " + " ", end="")
        print("| ")

    print("  ", end="")
    for it in range(int(1.5 * FIELD_SIZE)):
        print("- ", end="")
    print("-")


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
