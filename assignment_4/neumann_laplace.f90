program neumann_laplace
    implicit none
    integer :: nx, ny, i, j, iter
    double precision :: A, B, C, D
    double precision :: conv, error
    double precision, allocatable :: T(:,:), T_old(:,:)

    nx = 34
    ny = 34
    allocate(T(nx,ny))
    allocate(T_old(nx,ny))
    T = 0.0d0
    T_old = 0.0d0

    ! neumann boundary conditions
    A = -70.0d0
    B = -40.0d0
    C = 20.0d0
    D = -10.0d0

    iter = 0
    conv = 0.00001d0
    error = 1.0d0

    do while (error > conv)
        error = 0.0d0
        T_old = T

        do i = 2, nx-1
            do j = 2, ny-1
                T(i,j) = 0.25d0*(T(i+1,j)+T(i-1,j)+T(i,j+1)+T(i,j-1))
            end do
        end do

        do j = 2, ny-1
            T(1,j) = 0.25d0*(2*T(2,j) + T(1,j-1) + T(1,j+1) - 2*A)
            T(nx,j) = 0.25d0*(2*T(nx-1,j) + T(nx,j-1) + T(nx,j+1) + 2*B)
        end do

        do i = 2, nx-1
            T(i,1) = 0.25d0*(2*T(i,2) + T(i+1,1) + T(i-1,1) - 2*C)
            T(i,ny) = 0.25d0*(2*T(i,ny-1) + T(i+1,ny) + T(i-1,ny) +  2*D)
        end do

        T(1,1) = 0.5d0*(T(2,1) - A + T(1,2) - C)
        T(1,ny) = 0.5d0*(T(2,ny) - A + T(1,ny-1) + D)
        T(nx,1) = 0.5d0*(T(nx-1,1) + B + T(nx,2) - C)
        T(nx,ny) = 0.5d0*(T(nx-1,ny) + B + T(nx,ny-1) + D)

        do i = 1, nx-1
            do j = 1, ny-1
                error = max(error, abs(T(i,j) - T_old(i,j)))
            end do
        end do
        
        do i = 1, nx
            do j = 1, ny
                T(i,j) = T(i,j) + 2000 - T(1,1)
            end do
        end do

        iter = iter + 1

    end do

    print *, "Steps till convergence : ", iter

    open(unit=10, file='laplace_neumann.txt', status='replace')
    do i = 1, nx
        do j = 1, ny
            write (10,*) i, j, T(i,j)
        end do
    end do

    close(10)

end program neumann_laplace
