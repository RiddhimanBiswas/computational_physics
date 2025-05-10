program differential_eq
    implicit none
    double precision :: x0, y0, dx, x, y_actual, y_euler, y_mod, y_imp, k1_mod, k2_mod, k1_imp, k2_imp

    x0 = 0.0d0
    y0 = 0.0d0
    dx = 0.001d0
    y_actual = 0.0d0
    y_euler = y0
    y_mod = y0
    y_imp = y0
    k1_mod = 0.0d0
    k2_mod = 0.0d0
    k1_imp = 0.0d0
    k2_imp = 0.0d0
    x = x0

    open(unit=10, file="q1_3_values.txt", status="replace")
    write (10,*) x, tan(x), y_euler, y_mod, y_imp

    do while (x <= 1.55d0)
        y_euler = y_euler + dx * (y_euler**2 + 1)
        k1_mod = y_mod**2 + 1
        k2_mod = (y_mod + (dx * k1_mod)/2)**2 + 1
        y_mod = y_mod + dx * k2_mod
        k1_imp = y_imp**2 + 1
        k2_imp = (y_imp + dx * k1_imp)**2 + 1
        y_imp = y_imp + (dx * (k1_imp + k2_imp))/2
        x = x + dx
        y_actual = tan(x)
        write (10,*) x, y_actual, y_euler, y_mod, y_imp
    end do

    close(10)

end program differential_eq

