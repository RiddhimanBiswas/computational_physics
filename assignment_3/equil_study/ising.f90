program ising3d
    implicit none
    integer :: L, niter
    real :: T, J_ising
    integer :: N, i
    integer, allocatable :: lattice(:,:,:)
    real :: energy, magnetic
    real :: magnetic_avg, energy_avg
    character(len=50) :: filename  ! String to store the filename

    ! User Input
    print *, "Enter lattice size (L) : "
    read *, L
    print *, "Enter the number of iterations (niter) : "
    read *, niter
    print *, "Enter temperature T : "
    read *, T
    print *, "Enter the strength of coupling (J_ising) : "
    read *, J_ising

    write(filename, '(A,I0,A,I0,A,F0.2,A,F0.2,A)') "ising3d_L", L, "_n", niter, "_T", T, "_J", J_ising, ".txt"
    filename = trim(adjustl(filename))
    
    N = L*L*L
    allocate(lattice(L,L,L))
    
    call random_seed()

    energy = 0.0
    magnetic = 0.0

    call initialize_spins(J_ising, L, lattice, magnetic, energy)
    
    ! Open file with dynamic name
    open(unit=10, file=filename, status='replace')
    
    do i = 1, niter
        call mcs(J_ising, L, lattice, T, magnetic, energy)
        magnetic_avg = magnetic / N
        energy_avg = energy / N
        write(10, *) i, magnetic_avg, energy_avg
    end do
    
    close(10)

contains

    subroutine initialize_spins(J_ising, L, lattice, magnetic, energy)
        implicit none
        real, intent(in) :: J_ising
        integer, intent(in) :: L
        integer, intent(inout) :: lattice(L,L,L)
        real, intent(inout) :: energy, magnetic
        integer :: i, j, k
        real :: r

        do i = 1, L
            do j = 1, L
                do k = 1, L
                    call random_number(r)
                    if (r < 0.5) then
                        lattice(i,j,k) = 1
                        magnetic = magnetic + 1
                    else
                        lattice(i,j,k) = -1
                        magnetic = magnetic - 1
                    end if
                end do
            end do
        end do

        do i = 1, L
            do j = 1, L
                do k = 1, L
                    energy = energy - 0.5 * J_ising * lattice(i,j,k) * &
                                    (lattice(mod(i,L)+1,j,k) + lattice(mod(i-2+L,L)+1,j,k) + &
                                     lattice(i,mod(j,L)+1,k) + lattice(i,mod(j-2+L,L)+1,k) + &
                                     lattice(i,j,mod(k,L)+1) + lattice(i,j,mod(k-2+L,L)+1))
                end do
            end do
        end do
    end subroutine initialize_spins

    subroutine mcs(J_ising, L, lattice, T, magnetic_prev, energy_prev)
        implicit none
        real, intent(in) :: J_ising, T
        integer, intent(in) :: L
        integer, intent(inout) :: lattice(L,L,L)
        real, intent(inout) :: energy_prev, magnetic_prev
        integer :: i, x, y, z
        real :: r, energy, dE

        do i = 1, L*L*L
            call random_number(r)
            x = int(r * L) + 1
            call random_number(r)
            y = int(r * L) + 1
            call random_number(r)
            z = int(r * L) + 1

            energy = -J_ising * lattice(x,y,z) * &
                                    (lattice(mod(x,L)+1,y,z) + lattice(mod(x-2+L,L)+1,y,z) + &
                                     lattice(x,mod(y,L)+1,z) + lattice(x,mod(y-2+L,L)+1,z) + &
                                     lattice(x,y,mod(z,L)+1) + lattice(x,y,mod(z-2+L,L)+1))

            dE = 2 * (-energy)

            if (dE <= 0) then
                lattice(x,y,z) = -lattice(x,y,z)
                energy_prev = energy_prev + dE
                magnetic_prev = magnetic_prev + 2 * lattice(x,y,z)
            else
                call random_number(r)
                if (r <= exp(-dE / T)) then
                    lattice(x,y,z) = -lattice(x,y,z)
                    energy_prev = energy_prev + dE
                    magnetic_prev = magnetic_prev + 2 * lattice(x,y,z)
                end if
            end if
       end do
   end subroutine mcs

end program ising3d

