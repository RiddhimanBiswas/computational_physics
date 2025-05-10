program dirichlet_laplace
    implicit none
    integer :: nx, ny, i, j, iter
    double precision :: slope, conv, error
    double precision, allocatable :: T(:,:), T_old(:,:)
    
    nx = 34
    ny = 34
    allocate(T(nx,ny))
    allocate(T_old(nx,ny))
    T = 0.0d0
    T_old = 0.0d0

    ! boundary conditions
    do j = 1, ny
        T(1, j) = 3.7
        T(nx, j) = 0.4
    end do

    slope = (0.4 - 3.7)/(nx - 1)
    do i = 1, nx
        T(i, 1) = 3.7 + slope*(i-1)
        T(i, ny) = 3.7 + slope*(i-1)
    end do

    iter = 0
    conv = 0.0001d0
    error = 1.0d0

    do while (error > conv)
        error = 0.0d0
        T_old = T

        do i = 2, nx-1
            do j = 2, ny-1
                T(i,j) = 0.25d0*(T(i+1,j)+T(i-1,j)+T(i,j+1)+T(i,j-1))
            end do
        end do

        do i = 2, nx-1
            do j = 2, ny-1
                error = max(error, abs(T(i,j) - T_old(i,j)))
            end do
        end do

        iter = iter + 1

    end do

    print *, "Steps till convergence : ", iter

    open(unit=10, file='laplace_dirichlet.txt', status='replace')
    do i = 1, nx
        do j = 1, ny
            write (10,*) i, j, T(i,j)
        end do
    end do

    close(10)

end program dirichlet_laplace
