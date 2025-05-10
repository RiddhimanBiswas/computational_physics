program pbc
    implicit none
    double precision :: x, y, z
    double precision :: lx = 30

    x = mod(27.05d0, lx)
    y = mod(30.05d0, lx)
    z = mod(-0.03d0, lx)

    print *, "x = ", x
    print *, "y = ", y
    print *, "z = ", z

end program pbc