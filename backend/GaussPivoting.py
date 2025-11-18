import copy
import numpy as np
np.set_printoptions(suppress=True, precision=6)


def gauss_pivoting(A, b):

    if((A.shape[0] != A.shape[1]) or (b.shape[0] != A.shape[1])):
        print("Invalid input")

    n= len(b)

    ##Getting augumented matrix :

    Ab = np.concatenate((A.astype(float), b.astype(float)), axis=1)


    for i in range(n):

        ##pivoting algorithm
        pivot_row= i
        for k in range(i+1, n):
            if(abs(Ab[pivot_row][i]) < abs(Ab[k][i])):      ##pivot row take care
                pivot_row= k
        Ab[[i, pivot_row]] = Ab[[pivot_row, i]]            ##simple way to interchange the rows (numpy exclusively)

        ##Elimination part
        pivot= Ab[i][i]
        if (pivot == 0):
            print("Error")
            return
        
        
                 ###subtracting the whole (pivot row * mult) from the under row
        for j in range(i+1, n):
            multiplier = Ab[j][i] / pivot
            Ab[j] = Ab[j] - (multiplier * Ab[i])
            ##Ab[j, i:] = Ab[j, i:] - multiplier * Ab[i, i:]


    print(f"The matrix after elimination: \n {Ab}")

    ##Backward Substitution:

    X=[0]* n
    for i in range(n-1, -1, -1):

            ###does not work in the first iteration as j will be 3 and there is not X[3]
        s = 0
        for j in range(i+1, n):             ##range i+1 as the I got the higher orders first
            s += Ab[i][j] * X[j]
        X[i] = (Ab[i][n] - s) / Ab[i][i]



    print("The solution is : ")
    for ans in range(n):
        print(f"X{ans}= {X[ans]:.3f}")






##--------------------------------------------------------------------------------
A_example = np.array([
    [10, -7, 0],
    [-3, 2.099, 6],
    [5, -1, 5]
])

b_example = np.array([
    [7],
    [3.901],
    [6]
])

gauss_pivoting(A_example, b_example)

