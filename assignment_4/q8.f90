program particle_ring
    implicit none
    double precision :: y1_0, y26_0, t, dt, k_m, K_E, P_E, E
    integer :: i, niter
    double precision, dimension(50) :: y, v
    double precision, dimension(50) :: y_k1, y_k2, y_k3, y_k4
    double precision, dimension(50) :: v_k1, v_k2, v_k3, v_k4
    double precision, dimension(50) :: y_temp2, y_temp3, y_temp4

    ! assigning initial conditions
    y1_0 = 0.8d0
    y26_0 = 0.8d0
    y = 0.0d0
    y(1) = y1_0
    y(26) = y26_0
    v = 0.0d0
    t = 0.0d0
    dt = 0.02d0
    k_m = 1.0d0
    K_E = 0.0d0
    P_E = 0.0d0
    E = 0.0d0
    niter = 2000
    y_k1 = 0.0d0
    y_k2 = 0.0d0
    y_k3 = 0.0d0
    y_k4 = 0.0d0
    v_k1 = 0.0d0
    v_k2 = 0.0d0
    v_k3 = 0.0d0
    v_k4 = 0.0d0

    ! the coupled differential equations are ::
    ! dy_i/dt = v_i
    ! dv_i/dt = k_m*(y_{i+1} + y_{i-1} - 2y_i)
    ! here k = 1, m = 1, k/m = k_m = 1

    open(unit=10, file='circular_ring.txt', status='replace')
    K_E = 0.5d0*sum(v**2)
    P_E = 0.5d0*(sum((y(2:50)-y(1:49))**2) + (y(1)-y(50))**2)
    E = K_E + P_E
    write (10,*) t, y, v, K_E, P_E, E

    do i = 1, niter
            ! setting temp var to 0 to avoid any error
            y_temp2 = 0.0d0
            y_temp3 = 0.0d0
            y_temp4 = 0.0d0

            y_k1 = v
            v_k1(2:49) = k_m*(y(3:50)+y(1:48)-2*y(2:49))
            v_k1(1) = k_m*(y(2)+y(50)-2*y(1))
            v_k1(50) = k_m*(y(1)+y(49)-2*y(50))

            y_k2 = v + (dt*v_k1)/2
            y_temp2 = y + (dt*y_k1)/2
            v_k2(2:49) = k_m*(y_temp2(3:50)+y_temp2(1:48)-2*y_temp2(2:49))
            v_k2(1) = k_m*(y_temp2(2)+y_temp2(50)-2*y_temp2(1))
            v_k2(50) = k_m*(y_temp2(1)+y_temp2(49)-2*y_temp2(50))

            y_k3 = v + (dt*v_k2)/2
            y_temp3 = y + (dt*y_k2)/2
            v_k3(2:49) = k_m*(y_temp3(3:50)+y_temp3(1:48)-2*y_temp3(2:49))
            v_k3(1) = k_m*(y_temp3(2)+y_temp3(50)-2*y_temp3(1))
            v_k3(50) = k_m*(y_temp3(1)+y_temp3(49)-2*y_temp3(50))

            y_k4 = v + dt*v_k3
            y_temp4 = y + dt*y_k3
            v_k4(2:49) = k_m*(y_temp4(3:50)+y_temp4(1:48)-2*y_temp4(2:49))
            v_k4(1) = k_m*(y_temp4(2)+y_temp4(50)-2*y_temp4(1))
            v_k4(50) = k_m*(y_temp4(1)+y_temp4(49)-2*y_temp4(50))

            y = y + (dt*(y_k1 + 2*y_k2 + 2*y_k3 + y_k4))/6
            v = v + (dt*(v_k1 + 2*v_k2 + 2*v_k3 + v_k4))/6
            
            K_E = 0.5d0*sum(v**2)
            P_E = 0.5d0*(sum((y(2:50)-y(1:49))**2) + (y(1)-y(50))**2)
            E = K_E + P_E
            t = t + dt

            write (10,*) t, y, v, K_E, P_E, E
        end do

        close(10)

end program particle_ring
