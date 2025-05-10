program fitzhugh_nagumo_RD
    implicit none
    integer :: nx, ny, niter, iter, save_niter, next_save, i, j
    double precision :: d_a, d_b, alpha, beta, dt, t, time
    double precision, allocatable :: a(:,:), b(:,:), a_old(:,:), b_old(:,:)
    double precision, allocatable :: laplace_a(:,:), laplace_b(:,:)
    character(len=200) :: filename

    ! This is a reaction diffusion system based on Fitzhugh Nagumo - a bit different albeit
    ! The governing equations are:
    ! da/dt = d_a * Laplacian(a) + (a - a^3 - b + alpha)
    ! db/dt = d_b * Laplacian(b) + beta*(a - b)
    ! using finite differences and explicit Euler time integration.

    print *, "Enter the value of diffusion constant for A : "
    read *, d_a

    print *, "Enter the value of diffusion constant for B : "
    read *, d_b

    print *, "Enter the value of alpha : "
    read *, alpha

    print *, "Enter the value of beta : "
    read *, beta

    nx = 100
    ny = 100
    ! Choosing grid spacing of 1: dx = dy = 1
    allocate(a(nx,ny))
    allocate(b(nx,ny))
    allocate(a_old(nx,ny))
    allocate(b_old(nx,ny))
    allocate(laplace_a(nx,ny))
    allocate(laplace_b(nx,ny))

    ! Stability criteria for the algorithm
    dt = 0.1d0 / max(d_a, d_b)
    niter = 50000
    t = niter*dt
    save_niter = 1000
    next_save = save_niter
    time = 0.0d0

    a = 0.0d0
    b = 0.0d0
    a_old = 0.0d0
    b_old = 0.0d0
    call random_number(a)
    call random_number(b)
    write(filename, '(A, F0.3, A, F0.3, A, F0.3, A, F0.3, A)') &
        'Turing_', d_a, '_', d_b, '_', alpha, '_', beta, '.txt'
    filename = trim(adjustl(filename))

    open(unit=10, file=filename, status='replace')
    write(10,*) time, a, b

    do iter = 1, niter

        a_old = a
        b_old = b

        ! Call the laplacian subroutine for both fields
        call laplacian(a_old, laplace_a, nx, ny)
        call laplacian(b_old, laplace_b, nx, ny)

        do i = 1, nx
            do j = 1, ny
                a(i,j) = a_old(i,j) + dt*(d_a*laplace_a(i,j) + a_old(i,j) - a_old(i,j)**3 - b_old(i,j) + alpha)
                b(i,j) = b_old(i,j) + dt*(d_b*laplace_b(i,j) + beta*(a_old(i,j) - b_old(i,j)))
            end do
        end do

        if (iter == next_save) then
            time = iter * dt
            write(10,*) time, a, b
            next_save = next_save + save_niter
        end if

    end do

    close(10)

contains

    subroutine laplacian(a, laplacian_out, nx, ny)
        implicit none
        integer, intent(in) :: nx, ny
        integer :: i, j
        double precision, intent(in) :: a(nx,ny)
        double precision, intent(out) :: laplacian_out(nx,ny)

        ! Interior points
        do i = 2, nx-1
            do j = 2, ny-1
                laplacian_out(i,j) = a(i+1,j) + a(i-1,j) + a(i,j+1) + a(i,j-1) - 4.0d0 * a(i,j)
            end do
        end do

        ! Boundaries with periodic boundary conditions
        do j = 2, ny-1
            laplacian_out(1,j) = a(2,j) + a(nx,j) + a(1,j+1) + a(1,j-1) - 4.0d0 * a(1,j)
            laplacian_out(nx,j) = a(1,j) + a(nx-1,j) + a(nx,j+1) + a(nx,j-1) - 4.0d0 * a(nx,j)
        end do

        do i = 2, nx-1
            laplacian_out(i,1) = a(i+1,1) + a(i-1,1) + a(i,2) + a(i,ny) - 4.0d0 * a(i,1)
            laplacian_out(i,ny) = a(i+1,ny) + a(i-1,ny) + a(i,1) + a(i,ny-1) - 4.0d0 * a(i,ny)
        end do

        laplacian_out(1,1)    = a(2,1)    + a(nx,1)   + a(1,2)   + a(1,ny)   - 4.0d0 * a(1,1)
        laplacian_out(nx,1)   = a(1,1)    + a(nx-1,1) + a(nx,2)  + a(nx,ny)  - 4.0d0 * a(nx,1)
        laplacian_out(1,ny)   = a(2,ny)   + a(nx,ny)  + a(1,1)   + a(1,ny-1) - 4.0d0 * a(1,ny)
        laplacian_out(nx,ny)  = a(1,ny)   + a(nx-1,ny)+ a(nx,1)  + a(nx,ny-1)- 4.0d0 * a(nx,ny)
    end subroutine laplacian

end program fitzhugh_nagumo_RD

