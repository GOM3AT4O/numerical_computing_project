import numpy as np



def dolittle_LU(A, b):

    if ((A.shape[0] != A.shape[1])):              ##checks for the input
        print("Not valid entry!!!")
        return
    
    n = len(A)
    L = np.zeros((n, n))
    ##U = np.zeros((n, n))


    ### U & L ::::::
    for i in range(n):
        row_pivot = i
        for k in range(i+1, n):
            if(abs(A[k][i]) > abs(A[row_pivot][i])):
                row_pivot = k
            
        if row_pivot != i:   ##if the pivot is not the same our initialization
            A[[row_pivot, i]] = A[[i, row_pivot]]       ### to interchange two rows in numpy
            b[[i, row_pivot]] = b[[row_pivot, i]]       ##must do the swapping in b also

        ###safety check after pivoting
        pivot= A[i][i]
        if (pivot == 0):
            print("Error")
            return
        
        ###dolittle
        for j in range(i+1, n):
            multiplier = A[j][i]/A[i][i]
            L[j][i] = multiplier          ###############################
            A[j] = A[j] - (multiplier * A[i])

    ##L main diagonal :
    for i in range(n):
        L[i][i] = 1

    ##U = A.copy()
    return L, A, b
        
    


def Ly_b_subs(L, b):        ###forward substitution
    n = L.shape[0]
    y = np.zeros(n)
    ##y = [0] * n              ###this is ordinary python list
    for i in range (n):
        y[i] = b[i] - sum(L[i][j] * y[j] for j in range (i+1))

    #print(f"The vector y is : \n {y}")
    return y

def Ux_y_subs(U, y):
    n = U.shape[0]
    X = np.zeros(n)

    for i in range (n-1, -1, -1):
        X[i] = (y[i] - sum(U[i][j] * X[j] for j in range(i+1, n)))/U[i][i]
    ##here i will never equal to (j) as j = i+1/ and we calculate the sum of the values over the main diagonal
    ##in every row as j > i

    return X



####-------------------------------------------------------------------------------------------------

def main():

    n = int(input("Enter the number of equations : "))

    A = np.zeros((n, n))

    print("Enter the squared matrix : \n")
    for i in range(n):
        row = input(f"Row number {i} :  ").split()
        A[i] = [float (x) for x in row]       ##typecasting then loops over the elements of the row


    print("\nEnter the constants vector b:")
    b = np.array([float(x) for x in input().split()])          ##the basic way to enter the vector

    
    
    L, U, b_edit = dolittle_LU(A, b)
    y = Ly_b_subs(L, b_edit)
    X = Ux_y_subs(U, y)
    print(f"The U matrix is : \n {U}")
    print(f"The L matrix is : \n {L}")
    print(f"The vector y is : \n {y}")
    print(f"The solution X is : \n {X}")

    
     


if __name__ == "__main__":
    main()



    

