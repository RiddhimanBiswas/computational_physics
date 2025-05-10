program gauss_seidel
    implicit none
    double precision :: dx, conv, b, a, c1, d1, d2, d3, error
    integer :: n, i,  maxiter, iter
    logical :: converged
    double precision, allocatable :: x(:), y(:), y_old(:)

    dx =  0.01d0
    conv = 0.0001d0
    
    ! boundary condition for x
    b = 1.0d0
    a = 0.0d0
    
    ! creating initial array for x and y
    n = int((b - a)/dx) + 1
    allocate(x(n))
    allocate(y(n))
    allocate(y_old(n))
    
    ! forall does vectorized operation
    forall (i=1:n)
        x(i) = (i-1)*dx
    end forall
    y = 0.0d0
    
    ! boundary condition for y
    y(1) = 0.0d0
    y(n) = 2.0d0
    
    ! the differential equation is :
    ! y" - 5y' + 10y = 10x
    ! writing the eq as finite difference
    ! y_i = c1*(d1*y_old(i+1) + d2*y_new(i-1) + d3*x(i))

    c1 = 1/(2-10*dx**2)
    d1 = 1 - (5*dx)/2
    d2 = 1 + (5*dx)/2
    d3 = -10*dx**2

    ! initial guess for y
    forall (i=2:n-1)
        y(i) = 2*(i-1)*dx
    end forall

    ! max iteration defined, try with better guess if maxiter exceeded
    maxiter = 10000
    converged = .false.
    
    open(unit=10, file='gauss_seidel.txt', status='replace')
    write (10,*) x

    do iter = 1, maxiter
        y_old = y
        error = 0.0d0

        do i = 2, n-1
            y(i) = c1*(d1*y_old(i+1) + d2*y(i-1) + d3*x(i))
            error = max(error, abs(y(i) - y_old(i)))
        end do
        
        write (10,*) y

        if (error < conv) then
            converged = .true.
            exit
        end if

    end do

    close(10)

    if (converged) then
        print *, "Solution converged in ", iter, "steps"
    else
        print *, "Solution didn't converge"
    end if

end program gauss_seidel
