import numpy as np

def is_diagonlly_dominant(A):
    n = len(A[0])

    for i in range(n):
        diagonal = abs(A[i][i])
        off_diagonal = sum(abs(A[i][j]) for j in range(n) if i != j)
        if(diagonal < off_diagonal):
            return False
        
    return True

##------------------------------------------------------------------------

def gauss_seidel(A, b, x0, max_iter, tol):
    n = len(b)
    x = x0.copy()
    
    for iteration in range(max_iter):
        x_old = x.copy()

        for i in range(n):     ##same number as the variables and the equations// in each equation i count one var
            sum1= sum(A[i][j] * x[j] for j in range(i))
            ##gets the sum of the lower order variables if i= 2 >>> we sum (a20 x0 + a21 x1) 
            ##means that we are in the equation 3 and we solve for x2
            sum2= sum(A[i][j] * x_old[j] for j in range(i+1, n))
            ##gets the sum of the higher order variables that we did not compute them yet so we use the
            ##values of the last iteration 

            x[i]= (b[i] - (sum1+sum2))/A[i][i]


        error = np.linalg.norm(x - x_old, ord=np.inf)  
        print(f"The error of iteration {iteration} = {error} ") 
        ##after every iteration we calculate the relative error

        if(error < tol):
            return x
        
    print("We have reached the maximum no. of iterations and not satisfied the tolerance")
    return x

##------------------------------------------------------------------------

def main():
    print("<<<<<<<<<<<Gauss Seidel Method>>>>>>>>>>>")

    n= int(input("Enter the number of equations : \n"))
    A= np.zeros((n, n))       
    b= np.zeros(n)
    ###zeros() is a numpy function that generates arrays intialized with zero

    print("\nEnter the matrix row by row : ")
    for i in range(n):
        row= input(f"Row number {i+1} :").split()  ##this gets the input as list of string
        A[i] = [float (x) for x in row]   ##this makes the rows >> lists of floats

    print("/nEnter the constants b : ")
    b= np.array([float(x) for x in input().split()])

    print("\nEnter the initial guesses : ")
    x0 = np.array([float(x) for x in input().split()])

    tol= float(input("\nEnter the tolerance of stopping criteria :"))
    max_iter= int(input("\nEnter the max iteration number : "))

    if not is_diagonlly_dominant(A):
        print("\n Warning: The matrix is NOT diagonally dominant.")
        choice = input("This may cause divergence. Continue anyway? (y/n): ").strip().lower()
        if choice != 'y':
            print("Exiting program.")
            return
        else:
            print("Proceeding anyway...")

    print("\nStarting Gauss-Seidel Iteration...\n")
    result = gauss_seidel(A, b, x0,max_iter, tol )
    

    #===============================================================

    print ("\nThe final solution is : ")
    for i in range(n):
        print(f"X{i} = {result[i]}")


if __name__ == "__main__":
    main()