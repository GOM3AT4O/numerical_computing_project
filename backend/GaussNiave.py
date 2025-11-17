import copy
import numpy as np
np.set_printoptions(suppress=True, precision=6)


def gauss_naive(A, b):

    n = len(b)

    if ((A.shape[0] != A.shape[1]) or (A.shape[1] != b.shape[0]) or (b.shape[1] > 1)):              ##checks for the input
        print("Not valid entry!!!")
        return
    

    Ab = np.concatenate((A.astype(float), b.astype(float)), axis=1)        ##axis=1 means that as a column
    print(f"The augumented matrix is : \n {Ab}")

    ##Forward Elimintion process
    for i in range(n):
        pivot=Ab[i][i]
        if(pivot == 0):
            print("Error!! The Algrithm fails")
            return 

        for j in range(i+1, n):
            multiplier = Ab[j][i] / pivot
            Ab[j] = Ab[j] - (multiplier * Ab[i])

            ##Ab[j, i:] = Ab[j, i:] - multiplier * Ab[i, i:]          ### i: >> means all the i's
        ## (j) >> represents the under rows index // (i) >> number of columns
            
    print(f"The matrix after the forward elimination: \n {Ab}")

##----------------------------------------------------------------

    ##Backward Substitution 
    X = [0] * n
             
    for i in range (n-1 , -1, -1):                       
        s = 0
        for j in range(i+1, n):
            s += Ab[i][j] * X[j]
        X[i] = (Ab[i][n] - s) / Ab[i][i]

        ## step= -1/ the final value= -1 (exclusive) >>> 0
        ##this sum is the sum of the knowns terms in the equation
        ##we set it to zero whenever we deal with new equation
        ##j represents the columns and is always greater than the
    
        ##Ab[i][n] >> n is permanent as this is the column of (b) and we always consider it
        ## Ab[i][i] >> is permanent as the unknown is always at the diagonal
    

    print(f"The solution is : ")
    for ans in range(n):
        print(f"X{ans} = {X[ans]}")
        
    ##return X

    


    """
    Ab = copy.deepcopy(A)      ## this is the augumented matrix creation // deep copy to be another reference 
    for i in range(n):
        Ab[i].append(b[i])
    print(f"The initial augumented matrix is : \n{Ab}")        ##take care of the f inside the bracket
        
    x = [0] * n                ##x = np.zeros(n)   same as it
    """


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

gauss_naive(A_example, b_example)

