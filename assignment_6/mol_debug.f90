program mol4
    implicit none
    integer, parameter :: n_particles = 1200
    double precision, parameter :: l = 20.0d0 ! cubic box
    integer, parameter :: niter_eq = 30000, niter_prod = 10000
    double precision, parameter :: dt = 0.0025d0
    double precision, parameter :: esp = 1.0d0, sig = 1.0d0
    double precision :: r_c, r_s
    double precision, parameter :: T_target = 1.0d0
    integer, parameter :: neighbour_interval = 40
    ! m = 1.0d0 has been assumed
    ! k_B = 1.0d0 has been assumed

    double precision, allocatable :: pos(:), pos_new(:)
    double precision, allocatable :: F(:), F_new(:)
    double precision, allocatable :: vel(:), vel_new(:)

    integer, allocatable :: num_neigh(:)
    integer, allocatable :: nb_list(:,:)
    double precision, allocatable :: distance_list(:,:)
    integer :: max_neigh
    double precision :: V_s, V_tot, K_tot, E_tot
    double precision, allocatable :: gr(:)
    double precision :: dr
    integer :: n_bins

    integer :: iter, i

    allocate(pos(3*n_particles))
    allocate(pos_new(3*n_particles))
    allocate(F(3*n_particles))
    allocate(F_new(3*n_particles))
    allocate(vel(3*n_particles))
    allocate(vel_new(3*n_particles))

    r_c = 2.5d0*sig
    r_s = 4.5d0*sig

    pos = 0.0d0
    pos_new = 0.0d0
    vel = 0.0d0
    vel_new = 0.0d0
    F = 0.0d0
    F_new = 0.0d0

    V_s = (4.0d0/3.0d0)*3.14159d0*r_s**3
    max_neigh = int(10*n_particles*V_s/(l**3))
    allocate(num_neigh(n_particles))
    allocate(nb_list(n_particles, max_neigh))
    allocate(distance_list(n_particles, max_neigh))
    num_neigh = 0
    nb_list = 0
    distance_list = 0

    dr = 0.1d0*sig
    n_bins = int(0.5d0*l/dr)
    allocate(gr(n_bins))
    gr = 0.0d0  ! Initialize to zero

    ! initialization steps
    !call initialize_position(pos, n_particles, l, sig)
    !call initialize_position_random(pos, n_particles, l, sig)
    call initialize_position(pos, n_particles, l, sig)
    call initialize_velocity(vel, n_particles, T_target)

    call neighbour_list(n_particles, max_neigh, l, r_s, pos, num_neigh, nb_list, distance_list)
    call compute_F_V(n_particles, pos, num_neigh, nb_list, distance_list, r_c, sig, esp, l, F, V_tot)
    call compute_KE(n_particles, vel, K_tot)
    E_tot = V_tot + K_tot

    print *, "Initialization done!"
    print *, "Initial potential energy: ", V_tot
    print *, "Initial kinetic energy: ", K_tot
    print *, "Initial total energy: ", E_tot

    ! Main MD code
    
    ! Equilibration
    do iter = 1, niter_eq
        call update_position(n_particles, dt, l, pos, vel, F, pos_new)
        pos = pos_new
        call pbc(n_particles, l, pos)
        if (mod(iter, 1000) == 0) then
            print *, "Iteration: ", iter
        end if

        if (mod(iter, neighbour_interval) == 0) then
            call neighbour_list(n_particles, max_neigh, l, r_s, pos, num_neigh, nb_list, distance_list)
        end if

        call compute_F_V(n_particles, pos, num_neigh, nb_list, distance_list, r_c, sig, esp, l, F_new, V_tot)
        call update_velocity(n_particles, dt, vel, F, F_new, vel_new)

        vel = vel_new
        F = F_new

        if (mod(iter, 100) == 0) then
            call thermostat(vel, n_particles, T_target)
        end if

        if (mod(iter, 100) == 0) then
            call compute_KE(n_particles, vel, K_tot)
            E_tot = V_tot + K_tot
            ! print *, "Iteration: ", iter
            ! print *, "Potential energy: ", V_tot
            ! print *, "Kinetic energy: ", K_tot
            ! print *, "Total energy: ", E_tot
        end if
    end do

    print *, "Equilibration done!"

    open(unit=10, file='energy_debug.txt', status='replace')
    open(unit=20, file='gr_debug.txt', status='replace')
    open(unit=30, file='vel_data_debug.txt', status='replace')
    open(unit=40, file='pos_data_debug.txt', status='replace')

    ! Production run
    do iter = 1, niter_prod
        call update_position(n_particles, dt, l, pos, vel, F, pos_new)
        pos = pos_new
        call pbc(n_particles, l, pos)
        if (mod(iter, 1000) == 0) then
            print *, "Iteration: ", (iter + niter_eq)
        end if

        if (mod(iter, neighbour_interval) == 0) then
            call neighbour_list(n_particles, max_neigh, l, r_s, pos, num_neigh, nb_list, distance_list)
        end if

        call compute_F_V(n_particles, pos, num_neigh, nb_list, distance_list, r_c, sig, esp, l, F_new, V_tot)
        call update_velocity(n_particles, dt, vel, F, F_new, vel_new)
        
        vel = vel_new
        F = F_new

        if (mod(iter, 100) == 0) then
            call thermostat(vel, n_particles, T_target)
        end if

        if (mod(iter, 100) == 0) then
            call compute_KE(n_particles, vel, K_tot)
            E_tot = V_tot + K_tot
            write(10,*) iter, V_tot, K_tot, E_tot
            ! print *, "Iteration: ", iter
            ! print *, "Potential energy: ", V_tot
            ! print *, "Kinetic energy: ", K_tot
            ! print *, "Total energy: ", E_tot
        end if

        if (mod(iter, 100) == 0) then
        !if (iter == niter_prod) then
            call correlation(n_particles, pos, l, dr, n_bins, gr)
            write(20,*) iter, gr
        end if

        if (mod(iter, 1000) == 0) then
            write(30,*) iter, vel
            write(40,*) iter, pos
        end if

    end do

    print *, "Production run done!"

    close(40)
    close(30)
    close(20)
    close(10)

    deallocate(num_neigh)
    deallocate(nb_list)
    deallocate(distance_list)

contains
    ! input pairwise distance
    subroutine force(F, r, r_c, sig, esp)
        ! Lennard-Jones force
        implicit none
        double precision, intent(in) :: r(3), r_c, sig, esp
        double precision, intent(inout) :: F(:)
        double precision :: r_mod
        double precision :: F_mag

        r_mod = sqrt(dot_product(r, r))

        if (r_mod > r_c) then
            F(1) = 0.0d0
            F(2) = 0.0d0
            F(3) = 0.0d0
            return
        end if

        F_mag = 4.0d0*esp*((12*sig**12)/(r_mod**13)-(6*sig**6)/(r_mod**7))
        F(1) = F_mag*r(1)/r_mod
        F(2) = F_mag*r(2)/r_mod
        F(3) = F_mag*r(3)/r_mod

    end subroutine force   

    ! input pairwise distance
    subroutine potential(V, r, r_c, sig, esp)
        ! Lennard-Jones potential
        implicit none
        double precision, intent(in) :: r(3), r_c, sig, esp
        double precision, intent(inout) :: V
        double precision :: r_mod

        r_mod = sqrt(dot_product(r, r))

        if (r_mod > r_c) then
            V = 0.0d0
            return
        end if
        V = 4.0d0*esp*((sig/r_mod)**12 - (sig/r_mod)**6)

    end subroutine potential

    subroutine initialize_position_random(pos, n_particles, l, sig)
        implicit none
        integer, intent(in) :: n_particles
        double precision, intent(in) :: l, sig
        double precision, intent(inout) :: pos(:)
        double precision :: rand_x, rand_y, rand_z
        integer :: i
    
        ! Place particles randomly in the box with proper spacing from boundaries
        do i = 1, n_particles
            ! Generate a new random number for each coordinate
            call random_number(rand_x)
            call random_number(rand_y)
            call random_number(rand_z)
        
            ! Set positions with proper scaling
            pos(3*i-2) = rand_x * (l - sig) + 0.5d0*sig  ! x-coordinate
            pos(3*i-1) = rand_y * (l - sig) + 0.5d0*sig  ! y-coordinate
            pos(3*i)   = rand_z * (l - sig) + 0.5d0*sig  ! z-coordinate
        end do
    
    end subroutine initialize_position_random

    subroutine initialize_position_random_all(pos, n_particles, l, sig)
        implicit none
        integer, intent(in) :: n_particles
        double precision, intent(in) :: l, sig
        double precision, intent(inout) :: pos(:)
        double precision :: rand_x, rand_y, rand_z
        integer :: i
    
        ! Place particles randomly in the box with proper spacing from boundaries
        do i = 1, n_particles
            ! Generate a new random number for each coordinate
            call random_number(rand_x)
            call random_number(rand_y)
            call random_number(rand_z)
        
            ! Set positions with proper scaling
            pos(3*i-2) = rand_x * l   ! x-coordinate
            pos(3*i-1) = rand_y * l   ! y-coordinate
            pos(3*i)   = rand_z * l   ! z-coordinate
        end do
    
    end subroutine initialize_position_random_all

    subroutine initialize_position(pos, n_particles, l, sig)
        implicit none
        integer, intent(in) :: n_particles
        double precision, intent(in) :: l, sig
        double precision, intent(inout) :: pos(:)
        integer :: i, j, k, n_side, i_part
        double precision :: l_particle, l_mod

        ! considering pbc
        l_mod = l - sig
        n_side = ceiling(dble(n_particles)**(1.0d0/3.0d0))
        l_particle = l_mod/n_side

        if (l_particle < sig) then
            print *, "Error: Particle number large to uniformly distribute"
            stop
        end if

        i_part = 1

        do i = 1, n_side
            do j = 1, n_side
                do k = 1, n_side
                    if (i_part > n_particles) then
                        exit
                    end if
                    pos(3*i_part-2) = (i-1)*l_particle + 0.5d0*sig
                    pos(3*i_part-1) = (j-1)*l_particle + 0.5d0*sig
                    pos(3*i_part) = (k-1)*l_particle + 0.5d0*sig
                    i_part = i_part + 1
                end do
                if (i_part > n_particles) then
                    exit
                end if
            end do
            if (i_part > n_particles) then
                exit
            end if
        end do

        print *, "Initialized positions of particles!"

    end subroutine initialize_position

    subroutine initialize_velocity(vel, n_particles, T)
        implicit none
        integer, intent(in) :: n_particles
        double precision, intent(in) :: T
        double precision, intent(inout) :: vel(:)
        double precision, allocatable :: rand_number(:)

        allocate(rand_number(3*n_particles))
        call random_number(rand_number)
        
        ! the sqrt(12*T) is to ensure equipartition of energy
        ! velocity is rand(-0.5, 0.5) scaled
        vel = sqrt(12*T)*(rand_number - 0.5d0)
        call momentum_correct(vel, n_particles)

        print *, "Initialized velocities of particles!"

    end subroutine initialize_velocity

    subroutine momentum_correct(vel, n_particles)
        implicit none
        integer, intent(in) :: n_particles
        double precision, intent(inout) :: vel(:)
        double precision :: p_total, p_avg
        double precision :: p_total_x, p_total_y, p_total_z
        integer :: i

        p_total_x = sum(vel(1:3*n_particles:3))
        p_total_y = sum(vel(2:3*n_particles:3))
        p_total_z = sum(vel(3:3*n_particles:3))
        p_total_x = p_total_x/n_particles
        p_total_y = p_total_y/n_particles
        p_total_z = p_total_z/n_particles

        print *, "Momentum before correction: ", p_total_x, p_total_y, p_total_z
        
        do i = 1, n_particles
            vel(3*i-2) = vel(3*i-2) - p_total_x
            vel(3*i-1) = vel(3*i-1) - p_total_y
            vel(3*i) = vel(3*i) - p_total_z
        end do

        p_total_x = sum(vel(1:3*n_particles:3))
        p_total_y = sum(vel(2:3*n_particles:3))
        p_total_z = sum(vel(3:3*n_particles:3))
        p_total_x = p_total_x/n_particles
        p_total_y = p_total_y/n_particles
        p_total_z = p_total_z/n_particles

        print *, "Momentum after correction: ", p_total_x, p_total_y, p_total_z

        ! Check if momentum is zero
        if (abs(p_total_x) > 1.0d-6 .or. abs(p_total_y) > 1.0d-6 .or. abs(p_total_z) > 1.0d-6) then
            print *, "Error: Momentum correction failed!"
            stop
        end if
        print *, "Momentum correction successful!"
        print *, "-------------------------------------"

    end subroutine momentum_correct

    subroutine correct_F_V(F_mod, V_mod, r, r_c, sig, esp)
        implicit none
        double precision, intent(in) :: r(3), r_c, sig, esp
        double precision, intent(inout) :: F_mod(:), V_mod
        double precision :: F_r(3), F_r_c(3)
        double precision :: V_r, V_c, r_mod
        double precision :: r_c_array(3)
        
        r_mod = sqrt(dot_product(r, r))

        if (r_mod > r_c) then
            F_mod(1) = 0.0d0
            F_mod(2) = 0.0d0
            F_mod(3) = 0.0d0
            V_mod = 0.0d0
            return
        end if

        call force(F_r, r, r_c, sig, esp)
        r_c_array = r_c * r/r_mod
        call force(F_r_c, r_c_array, r_c, sig, esp)
        F_mod = F_r - F_r_c
        call potential(V_r, r, r_c, sig, esp)
        call potential(V_c, r_c_array, r_c, sig, esp)
        V_mod = V_r - V_c + (r_mod - r_c)*dot_product(F_r_c, r_c_array)/r_c

    end subroutine correct_F_V

    subroutine update_position(n_particles, dt, l, pos, vel, F, pos_new)
        ! Update positions using the Verlet algorithm
        implicit none
        integer, intent(in) :: n_particles
        double precision, intent(in) :: dt, l
        double precision, intent(in) :: pos(:), vel(:)
        double precision, intent(in) :: F(:)
        double precision, intent(inout) :: pos_new(:)
        
        pos_new = pos + vel*dt + 0.5d0*F*dt**2
        call pbc(n_particles, l, pos_new)

    end subroutine update_position

    subroutine update_velocity(n_particles, dt, vel, F, F_new, vel_new)
        ! Update velocities using the Verlet algorithm
        implicit none
        integer, intent(in) :: n_particles
        double precision, intent(in) :: dt
        double precision, intent(in) :: vel(:)
        double precision, intent(in) :: F(:), F_new(:)
        double precision, intent(inout) :: vel_new(:)
        
        vel_new = vel + 0.5d0*(F + F_new)*dt

    end subroutine update_velocity

    subroutine pbc(n_particles , l, pos)
        implicit none
        integer, intent(in) :: n_particles
        double precision, intent(in) :: l
        double precision, intent(inout) :: pos(:)
        integer :: i

        do i = 1, n_particles
            pos(3*i-2) = pos(3*i-2) - l*floor(pos(3*i-2)/l)
            pos(3*i-1) = pos(3*i-1) - l*floor(pos(3*i-1)/l)
            pos(3*i)   = pos(3*i)   - l*floor(pos(3*i)/l)
        end do

    end subroutine pbc
    
    subroutine thermostat(vel, n_particles, T_target)
        implicit none
        integer, intent(in) :: n_particles
        double precision, intent(inout) :: vel(:)
        double precision :: T_target
        double precision :: T_current, T_factor
        integer :: i

        ! Calculate current temperature
        T_current = sum(vel**2)/(3*n_particles)
        T_factor = sqrt(T_target/T_current)

        vel = vel * T_factor

    end subroutine thermostat

    subroutine distance(r1, r2, l, r_mod)
        ! Calculate distance between two particles
        implicit none
        double precision, intent(in) :: r1(3), r2(3), l
        double precision :: r(3)
        integer :: i 
        double precision, intent(inout) :: r_mod
        
        r = r2 - r1
        do i = 1, 3
            if (abs(r(i)) > l*0.5d0) then
                r(i) = r(i) - sign(l, r(i))
            end if
        end do

        r_mod = sqrt(dot_product(r, r))

    end subroutine distance

    subroutine neighbour_list(n_particles, max_neigh, l, r_s, pos, num_neigh, nb_list, distance_list)
        ! Create a neighbour list for each particle
        implicit none
        integer :: i, j
        integer, intent(in) :: n_particles, max_neigh
        double precision, intent(in) :: l, r_s
        double precision, intent(in) :: pos(:)
        double precision :: r_mod
        integer, intent(inout) :: num_neigh(:)
        integer, intent(inout) :: nb_list(:,:)
        double precision, intent(inout) :: distance_list(:,:)

        num_neigh = 0
        nb_list = 0
        distance_list = 0

        do i = 1, n_particles
            do j = 1, n_particles
                if (i /= j) then
                    call distance(pos(3*i-2:3*i), pos(3*j-2:3*j), l, r_mod)
                    if (r_mod < r_s) then
                        ! Add to neighbour list
                        num_neigh(i) = num_neigh(i) + 1
                        if (num_neigh(i) <= max_neigh) then
                            nb_list(i, num_neigh(i)) = j
                            distance_list(i, num_neigh(i)) = r_mod
                        else
                            print *, "Error: Neighbour list exceeded"
                            stop
                        end if
                    end if
                end if
            end do
        end do


    end subroutine neighbour_list

    subroutine compute_F_V(n_particles, pos, num_neigh, nb_list, distance_list, r_c, sig, esp, l, F_total, V_total)
        implicit none
        ! Inputs
        integer, intent(in) :: n_particles
        double precision, intent(in) :: pos(:)
        integer, intent(in) :: num_neigh(:)
        integer, intent(in) :: nb_list(:, :)
        double precision, intent(in) :: distance_list(:, :)
        double precision, intent(in) :: r_c, sig, esp, l

        ! Outputs
        double precision, intent(inout) :: F_total(:)
        double precision, intent(inout) :: V_total

        ! Local variables
        integer :: i, n, j, nb
        double precision :: disp(3), r_mod_pair
        double precision :: F_pair(3), V_pair
        integer :: k

        ! Initialize total force array to zero
        F_total = 0.0d0
        V_total = 0.0d0

        ! Loop over each particle i
        do i = 1, n_particles
            ! Loop over each neighbor of particle i
            do n = 1, num_neigh(i)
                nb = nb_list(i, n)
                
                ! Only compute forces for pairs where i < nb to avoid double counting
                if (i < nb) then
                    disp(1) = pos(3*i-2) - pos(3*nb-2)
                    disp(2) = pos(3*i-1) - pos(3*nb-1)
                    disp(3) = pos(3*i)   - pos(3*nb)
                    do k = 1, 3
                        if (abs(disp(k)) > 0.5d0*l) then
                            disp(k) = disp(k) - sign(l, disp(k))
                        end if
                    end do
                    r_mod_pair = sqrt(dot_product(disp, disp))

                    ! compute the force if the pair separation is less than r_c.
                    if (r_mod_pair < r_c) then
                        ! Compute the force and potential for this pair
                        call correct_F_V(F_pair, V_pair, disp, r_c, sig, esp)
                        
                        ! Add the force on particle i and subtract it on particle nb.
                        ! (Newton's third law: F_ij = - F_ji)
                        F_total(3*i-2) = F_total(3*i-2) + F_pair(1)
                        F_total(3*i-1) = F_total(3*i-1) + F_pair(2)
                        F_total(3*i)   = F_total(3*i)   + F_pair(3)
                        F_total(3*nb-2) = F_total(3*nb-2) - F_pair(1)
                        F_total(3*nb-1) = F_total(3*nb-1) - F_pair(2)
                        F_total(3*nb)   = F_total(3*nb)   - F_pair(3)
                        
                        V_total = V_total + V_pair
                    end if
                end if
            end do
        end do

        ! No need to divide by 2 since we're only counting each pair once now
        V_total = V_total/n_particles

    end subroutine compute_F_V

    subroutine compute_KE(n_particles, vel, KE)
        implicit none
        integer :: i
        integer, intent(in) :: n_particles
        double precision, intent(in) :: vel(:)
        double precision, intent(inout) :: KE

        KE = 0.0d0
        do i = 1, n_particles
            KE = KE + 0.5d0 * (vel(3*i-2)**2 + vel(3*i-1)**2 + vel(3*i)**2)
        end do
        KE = KE/n_particles

    end subroutine compute_KE
    
    subroutine correlation(n_particles, pos, l, dr, n_bins, gr)
        ! finding the pair correlation function
        implicit none
        double precision, intent(in) :: pos(:), l, dr
        integer, intent(in) :: n_particles
        integer, intent(in) :: n_bins
        double precision, intent(inout) :: gr(:)
        double precision :: r_mod, r, V_shell, rho
        integer :: i, j, bin

        rho = dble(n_particles)/(l**3)

        ! Initialize the pair correlation function to zero
        gr = 0.0d0
        
        do i = 1, n_particles
            do j = 1, n_particles
                if (i == j) then
                    cycle
                end if
                call distance(pos(3*i-2:3*i), pos(3*j-2:3*j), l, r_mod)
                if (r_mod < 0.5d0*l) then
                    bin = int(r_mod/dr) + 1
                    gr(bin) = gr(bin) + 1.0d0
                end if
            end do
        end do

        ! Normalize the pair correlation function
        do i = 1, n_bins
            r = (i - 0.5d0)*dr
            V_shell = 4.0d0*3.14159d0*r**2*dr
            gr(i) = gr(i)/(n_particles*rho*V_shell)
        end do

    end subroutine correlation

end program mol4
