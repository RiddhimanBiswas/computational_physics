program rk4

    double precision :: x0, y0, dx, x, y_actual, y_rk4, k1_rk4, k2_rk4, k3_rk4, k4_rk4

    x0 = 0.0d0
    y0 = 0.0d0
    dx = 0.01d0
    y_actual = 0.0d0
    y_rk4 = y0
    k1_rk4 = 0.0d0
    k2_rk4 = 0.0d0
    k3_rk4 = 0.0d0
    k4_rk4 = 0.0d0
    x = x0

    open(unit=10, file="q4_values.txt", status="replace")
    write (10,*) x, tan(x), y_rk4

    do while (x <= 1.55d0)
        k1_rk4 = y_rk4**2 + 1
        k2_rk4 = (y_rk4 + (dx * k1_rk4)/2)**2 + 1
        k3_rk4 = (y_rk4 + (dx * k2_rk4)/2)**2 + 1
        k4_rk4 = (y_rk4 + dx * k3_rk4)**2 + 1
        y_rk4 = y_rk4 + (dx * (k1_rk4 + 2*k2_rk4 + 2*k3_rk4 + k4_rk4))/6
        x = x + dx
        y_actual = tan(x)
        write (10,*) x, y_actual, y_rk4
    end do

    close(10)

end program rk4
