import numpy as np


def crout_LU(A, b):
    
    A = A.copy()
    b = b.copy()
    
    if ((A.shape[0] != A.shape[1])):
        print("Not valid entry!!!")
        return
    
    n = len(A)
    L = np.zeros((n, n))
    
    for i in range(n):
        row_pivot = i
        for k in range(i+1, n):
            if(abs(A[k][i]) > abs(A[row_pivot][i])):
                row_pivot = k
        
        if row_pivot != i:  ###take care if needed onlyl
            A[[i, row_pivot]] = A[[row_pivot, i]]
            b[[i, row_pivot]] = b[[row_pivot, i]] 
            # We must also swap the computed parts of L
            L[[i, row_pivot], :i] = L[[row_pivot, i], :i] 
        
        
        pivot = A[i][i]
        if (pivot == 0): 
            print("Error: Zero pivot detected")
            return
        
        ##crout
        for j in range(i, n):  ###the first column of L is same as A // i here is the column number
            L[j][i] = A[j][i]   ###and after the first column we take the under diagonal elements
            ##same as the multipliers 

        ##calculating U as usula which is A here 
        for k in range(i+1, n):
            A[i][k] = A[i][k] / pivot  ###the first row of U is very easy to calculte as we know
            ##we normalize the row i of A (dividing by the pivot) to create the i-th row of u
            ##[L21 0 0][U12 1 0]>> (L21 * U12)= A12   and L21 is same as the pivot A11
        A[i][i] = 1.0  ## we then make it one 
        
        
        for j in range(i+1, n): ## for rows below the pivot row
            multiplier = A[j][i]   ##A[j][i]/ 1
            ###we say that as the pivot above it is one A[i][i] = 1
            A[j] = A[j] - (multiplier * A[i])  ##we make this as usual

 
    return L, A, b


def crout_Ly_b_subs(L, b):   ### forward substitution for Crout
    n = L.shape[0]
    y = np.zeros(n)
    
    for i in range (n):
        # Corrected sum: range(i) only includes terms before i
        s = sum(L[i][j] * y[j] for j in range(i))
        
        if ( L[i][i] == 0):
             print("Error")
             return 
             
        y[i] = (b[i] - s) / L[i][i]

    return y

def Ux_y_subs(U, y):
    n = U.shape[0]
    X = np.zeros(n)

    for i in range (n-1, -1, -1):
        
        s = sum(U[i][j] * X[j] for j in range(i+1, n))
        X[i] = (y[i] - s) / U[i][i]
    return X

####-------------------------------------------------------------------------------------------------

def main():

    n = int(input("Enter the number of equations : "))

    A = np.zeros((n, n))

    print("Enter the squared matrix : \n")
    for i in range(n):
        row = input(f"Row number {i} :  ").split()
        A[i] = [float (x) for x in row]


    print("\nEnter the constants vector b:")
    b = np.array([float(x) for x in input().split()])
    
    # Call the new Crout function
    # It returns L, U, and the permuted vector b
    L, U, b_permuted = crout_LU(A, b)
    
    if L is None:
        print("Decomposition failed.")
        return

    # Use the permuted b for forward substitution
    y = crout_Ly_b_subs(L, b_permuted)
    
    if y is None:
        print("Forward substitution failed.")
        return
        
    X = Ux_y_subs(U, y)
    
    print(f"\nThe U matrix is : \n {U}")
    print(f"\nThe L matrix is : \n {L}")
    print(f"\n y is : \n {y}")
    print(f"\nThe solution X is : \n {X}")

    


if __name__ == "__main__":
    main()