import numpy as np

def cholesky_LU(A):
    
    n = len(A)
    A = A.copy()
    
    if ((A.shape[0] != A.shape[1])):
        print("Not valid entry!!!")
        return
    
    ###symmetry chechk
    for i in range(n):
        for j in range(n):
            if(A[i][j] != A[j][i]):
                print("Error: Matrix is not symmetric.")
                return
    
    
    L = np.zeros((n, n))
    
    for i in range(n):
        
        ###calculate the diagonal element L[i,i]
        
        #2 sum of squares of elements in row i, before the diagonal
       
        sum_diag = (L[i, :i]**2).sum()
        ### takes the row i and every col of it from 0 >>> i-1 ( :i)
        
        
        val = A[i, i] - sum_diag ###this is the value under the square root 
        if val <= 0: # Check for non-positive (not positive-definite)
            print("Error: matrix is not positive")
            return None
            
        L[i, i] = np.sqrt(val)
        
        
        ### calculate the column elements below the diagonal (for j from i+1 to n)
        # (Code to calculate L[i, i] comes just before this)


        for j in range(i + 1, n):  ###for every row below
    
        # Calculate the sum: SUM( L[j,k] * L[i,k] ) for k from 0 to i-1
            sum_col = 0.0
            for k in range(i): ###all will be the same col number (k) >>> L21*L31 e.g
                sum_col += L[j, k] * L[i, k]
    ####the formula for the single element L[j, i]
            L[j, i] = (A[j, i] - sum_col) / L[i, i]

    return L


def cholesky_Ly_b_subs(L, b):
 
    n = len(L)
    y = np.zeros(n)
    
    for i in range (n):
        s = sum(L[i][j] * y[j] for j in range(i))
        y[i] = (b[i] - s) / L[i, i]
    return y

def Ux_y_subs(U, y):
    
    n = U.shape[0]
    X = np.zeros(n)

    for i in range (n-1, -1, -1):
        s = sum(U[i][j] * X[j] for j in range(i+1, n))
        X[i] = (y[i] - s) / U[i, i]
    return X

####-------------------------------------------------------------------------------------------------



def main():

    n = int(input("Enter the number of equations : "))
    A = np.zeros((n, n))

    print("Enter the symmetric positive matrix : \n")
    for i in range(n):
        row = input(f"Row number {i} :  ").split()
        A[i] = [float (x) for x in row]


    print("\nEnter the constants vector b:")
    b = np.array([float(x) for x in input().split()])
    
    L = cholesky_LU(A)
    
    y = cholesky_Ly_b_subs(L, b)
    X = Ux_y_subs(L.T, y)
    
    print(f"\nThe L matrix is : \n {L}")
    print(f"\nThe L^T matrix is : \n {L.T}")
    print(f"\n y is : \n {y}")
    print(f"\nThe solution X is : \n {X}")



if __name__ == "__main__":
    main()
