import numpy
import os
import time
import argparse


def initialize(M = None, N = None, max_h = 1000, max_w = 1000):

    row = M if(M is not None) else numpy.random.randint(3, max_h)
    col = N if(N is not None) else numpy.random.randint(3, max_w)

    matrix = numpy.random.randint(0,2, size=(row, col))

    return matrix


def step(matrix):

    new_matrix = numpy.copy(matrix)
    stop = False

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            new_matrix[i][j] = decision_act(matrix[i][j], neighbors_count_matrix(i, j, matrix))
    
    if(numpy.array_equal(matrix, new_matrix)): stop = True

    return new_matrix, stop


def neighbors_count_matrix(cell_row, cell_col, matrix):
        
    high_row = cell_row - 1 if(cell_row > 0) else cell_row
    left_col = cell_col - 1 if(cell_col > 0) else cell_col

    count = numpy.count_nonzero(matrix[high_row:cell_row + 2, left_col:cell_col + 2])    
    
    if(matrix[cell_row][cell_col] != 0): count -= 1

    return count


def decision_act(cell_state, neighbors_count):
    
    state = cell_state

    if(cell_state != 0):  
        if(neighbors_count < 2): state = 0
        if(neighbors_count == 2 or neighbors_count == 3): state = 1
        if(neighbors_count > 3): state = 0
        
    else:
        if(neighbors_count == 3): state = 1

    return state


def output(matrix):
    
    res_str = ''

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if(matrix[i][j] == 0): res_str += ' ' #u'\u25A1'
            else: res_str += u'\u2588' #u'\u25A0'
        res_str +='\n'

    return res_str


def file_input(file_path):

    if os.path.isfile(file_path):
        try:
            matrix = numpy.loadtxt(file_path, int)
        except:
            matrix = "Data in file is uncorrect!"
    else:
        matrix = "File doesn't exist!"
    
    return matrix


def cls():
    if(os.name == "nt"):
        os.system('cls')
    else:
        os.system('clear')



if __name__ == "__main__":

    input_params = argparse.ArgumentParser(description='no arguments:\n  for randomize the start state matrix', formatter_class=argparse.RawTextHelpFormatter)
    input_params.add_argument('-M','--rows', required=False, dest='rows', type=int, help='amount of rows in start state matrix')
    input_params.add_argument('-N','--columns', required=False, dest='cols', type=int, help='amount of columns in start state matrix')
    input_params.add_argument('-f', '--file', dest='file_name', required=False, help='input file path for start state matrix')
    args = input_params.parse_args()

    if args.file_name:
        
        try:
            matrix = file_input(args.file_name)
            if type(matrix) is str: 
                print('Error: {}'.format(matrix))
                raise SystemExit()
        except Exception as err: 
            print('Error: {}'.format(err))
            raise SystemExit()

    else: matrix = initialize(args.rows, args.cols)

    flag = False

    # os.system("mode con cols={} lines={}".format(len(matrix[0]), len(matrix)))

    while flag == False:
        
        cls()
        matrix, flag = step(matrix)
        print(output(matrix))
        time.sleep(0.0001)


