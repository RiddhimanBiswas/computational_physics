program diff_eq
    implicit none
    double precision :: x0, v0, x, v, t, dt, K_E, P_E, E
    integer :: i, niter
    double precision :: x_k1, x_k2, x_k3, x_k4
    double precision :: v_k1, v_k2, v_k3, v_k4

    x0 = 0.0d0
    v0 = 2.1d0
    x = x0
    v = v0
    t = 0.0d0
    dt = 0.01d0
    niter = 5000
    x_k1 = 0.0d0
    x_k2 = 0.0d0
    x_k3 = 0.0d0
    x_k4 = 0.0d0
    v_k1 = 0.0d0
    v_k2 = 0.0d0
    v_k3 = 0.0d0
    v_k4 = 0.0d0
    K_E = 0.0d0
    P_E = 0.0d0
    E = 0.0d0
    
    ! the coupled first order equations are :
    ! dx/dt = v
    ! dv/dt = -sin x

    open(unit=10, file='nonlinear_rk4_q7b.txt', status='replace')
    K_E = 0.5d0*(v**2)
    P_E = -cos(x)
    E = K_E + P_E
    write (10,*) t, x, v, K_E, P_E, E

    do i = 1, niter
        x_k1 = v
        v_k1 = -sin (x)
        x_k2 = v + (dt*v_k1)/2
        v_k2 = -sin ((x + (dt*x_k1)/2))
        x_k3 = v + (dt*v_k2)/2
        v_k3 = -sin ((x + (dt*x_k2)/2))
        x_k4 = v + dt*v_k3
        v_k4 = -sin ((x + dt*x_k3))

        x = x + (dt*(x_k1 + 2*x_k2 + 2*x_k3 + x_k4))/6
        v = v + (dt*(v_k1 + 2*v_k2 + 2*v_k3 + v_k4))/6
        
        K_E = 0.5d0*(v**2)
        P_E = -cos(x)
        E = K_E + P_E
        t = t + dt
        
        write (10,*) t, x, v, K_E, P_E, E
    end do

    close(10)

end program diff_eq
