import pycosat
from sudoku import Sudoku
from pprint import pprint
import timeit

input = 5
N = input ** 2
time_sum = 0

def v(i, j, d):
    # Encoding cell
    return N * N * (i - 1) + N * (j - 1) + d


def sudoku_clauses(encoding="sequential"):
    res = []
    num_cell = N * N * N

    for i in range(1, N + 1):
        for j in range(1, N + 1):
            res.append([v(i, j, d) for d in range(1, N + 1)])
            if encoding == "binomial":
                for d in range(1, 10):
                    for dp in range(d + 1, 10):
                        res.append([-v(i, j, d), -v(i, j, dp)])

            if encoding == "sequential":
                for d in range(1, N + 1):
                    s_i = v(i, j, d) + num_cell
                    if d == 1:
                        res.append([-v(i, j, d), s_i])
                    else:
                        s_i1 = v(i, j, d - 1) + num_cell
                        if d == N:
                            res.append([-s_i1, -v(i, j, d)])
                        else:
                            res.append([-v(i, j, d), s_i])
                            res.append([-s_i1, s_i])
                            res.append([-s_i1, -v(i, j, d)])

    def valid(cells):
        for i, xi in enumerate(cells):
            for j, xj in enumerate(cells):
                if i < j:
                    for d in range(1, N + 1):
                        res.append([-v(xi[0], xi[1], d), -v(xj[0], xj[1], d)])

    for i in range(1, N + 1):
        valid([(i, j) for j in range(1, N + 1)])
        valid([(j, i) for j in range(1, N + 1)])

    # 1 - 9 [1, 4, 7]
    # 1 - 16 [1, 5, 9, 13]
    # 1 - 25 [1, 6, 11, 16, 21]
    for i in range(1, N, input):
        for j in range(1, N, input):
            valid([(i + k % input, j + k // input) for k in range(N)])

    return res


def solve(grid):
    start = timeit.default_timer()
    clauses = sudoku_clauses("binomial")
    #clauses = sudoku_clauses()
    for i in range(1, N + 1):
        for j in range(1, N + 1):
            d = grid[i - 1][j - 1]
            if d:
                clauses.append([v(i, j, d)])

   #print("Ma hoa xong")
    stop = timeit.default_timer()

    # solve the SAT problem
    print(len(clauses))
    sol = set(pycosat.solve(clauses))

    print(stop - start)
    return (stop - start)


    def read_cell(i, j):
        for d in range(1, N + 1):
            if v(i, j, d) in sol:
                return d

    for i in range(1, N + 1):
        for j in range(1, N + 1):
            grid[i - 1][j - 1] = read_cell(i, j)


if __name__ == '__main__':
    time_sum = 0.0
    for i in range(0, 1):
        puzzle = Sudoku(input).difficulty(0.4)
        #print(puzzle)
        puzzle_check = puzzle
        for i in range(0, N):
            for j in range(0, N):
                if puzzle.board[i][j] is None:
                    puzzle.board[i][j] = 0
        #pprint(puzzle.board)
        t_time = solve(puzzle.board)
        time_sum += t_time
        #pprint(puzzle.board)



    print('Time: ', time_sum)

    #solution = puzzle_check.solve()

    # pprint(solution.board)

    #assert puzzle.board == solution.board
