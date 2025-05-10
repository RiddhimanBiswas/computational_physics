program ising3d
    implicit none
    integer :: L, niter, i, j
    real :: T, J_ising
    integer, allocatable :: lattice(:,:,:)
    real :: energy, magnetic, cv, chi
    real :: magnetic_avg, magnetic_abs_avg, energy_avg, magnetic_sq_avg, energy_sq_avg, magnetic_qd_avg
    character(len=100) :: filename

    print *, "Enter lattice size (L) : "
    read *, L
    print *, "Enter the strength of coupling (J_ising) : "
    read *, J_ising

    allocate(lattice(L,L,L))
    call random_seed()

    write(filename, '(A, I0, A, F0.2, A)') 'ising3d_L', L, '_n1000000_J', J_ising, '.txt'
    filename = trim(adjustl(filename))
    
    open(unit=10, file=filename, status='replace')
    
    T = 3.6

    do while (T <= 4.8)  ! Temperature loop
        call initialize_spins(J_ising, L, lattice, magnetic, energy)

        ! Equilibration phase (10000 MCS, no recording)
        do i = 1, 10000
            call mcs(J_ising, L, lattice, T, magnetic, energy)
        end do

        ! Statistical collection phase (1,000,000 MCS)
        magnetic_avg = 0.0
        magnetic_abs_avg = 0.0
        energy_avg = 0.0
        magnetic_sq_avg = 0.0
        energy_sq_avg = 0.0
        magnetic_qd_avg = 0.0

        do i = 1, 1000000
            call mcs(J_ising, L, lattice, T, magnetic, energy)
            magnetic_avg = magnetic_avg + magnetic
            magnetic_abs_avg = magnetic_abs_avg + abs(magnetic)
            energy_avg = energy_avg + energy
            magnetic_sq_avg = magnetic_sq_avg + magnetic**2
            energy_sq_avg = energy_sq_avg + energy**2
            magnetic_qd_avg = magnetic_qd_avg + magnetic**4
        end do

        ! Compute averages
        magnetic_avg = magnetic_avg / 1e6
        magnetic_abs_avg = magnetic_abs_avg / 1e6
        energy_avg = energy_avg / 1e6
        magnetic_sq_avg = magnetic_sq_avg / 1e6
        energy_sq_avg = energy_sq_avg / 1e6
        magnetic_qd_avg = magnetic_qd_avg / 1e6

        ! Compute Cv and Chi
        cv = (energy_sq_avg - energy_avg**2) / (T**2)
        chi = (magnetic_sq_avg - magnetic_abs_avg**2) / T

        ! Write to file
        write(10,*) T, magnetic_avg/L**3, energy_avg/L**3, cv, chi, magnetic_sq_avg, magnetic_qd_avg

        T = T + 0.02
    end do

    close(10)
    deallocate(lattice)

contains

    subroutine initialize_spins(J_ising, L, lattice, magnetic, energy)
        implicit none
        real, intent(in) :: J_ising
        integer, intent(in) :: L
        integer, intent(inout) :: lattice(L,L,L)
        real, intent(inout) :: energy, magnetic
        integer :: i, j, k
        real :: r

        energy = 0.0
        magnetic = 0.0

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
            x = int(r*L) + 1
            call random_number(r)
            y = int(r*L) + 1
            call random_number(r)
            z = int(r*L) + 1

            energy = -J_ising*lattice(x,y,z)*(lattice(mod(x,L)+1,y,z) + lattice(mod(x-2+L,L)+1,y,z) + &
                                    lattice(x,mod(y,L)+1,z) + lattice(x,mod(y-2+L,L)+1,z) + &
                                    lattice(x,y,mod(z,L)+1) + lattice(x,y,mod(z-2+L,L)+1))

            dE = 2*(-energy)

            if (dE <= 0) then
                lattice(x,y,z) = -lattice(x,y,z)
                energy_prev = energy_prev + dE
                magnetic_prev = magnetic_prev + 2*lattice(x,y,z)
            else
                call random_number(r)
                if (r <= exp(-dE/T)) then
                    lattice(x,y,z) = -lattice(x,y,z)
                    energy_prev = energy_prev + dE
                    magnetic_prev = magnetic_prev + 2*lattice(x,y,z)
                end if
            end if
       end do
   end subroutine mcs

end program ising3d

