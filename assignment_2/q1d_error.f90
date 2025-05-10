program trapezoid_pi_bin
    implicit none
    integer :: i, j, a, b, n(4)
    double precision :: h(4), integral(4), error(4), pi
    integer :: unit

    open(unit=unit, file="error_vs_n_gaussian.txt", status="replace")

    a = 0                ! The start point
    b = 1                ! The end point
    h(1) = 0.01d0        ! The rectangle width
    h(2) = 0.001d0
    h(3) = 0.0001d0
    h(4) = 0.00001d0
    do i=1,4
         n(i) = ceiling((b - a) / h(i)) 
    end do
    pi = 2 * asin(1.0d0)  
    integral = 0.0d0       ! The integral
    error = 0.0d0          ! The error

    do i=1,4
        integral(i) = integrand(dble(a)) + integrand(dble(b))
        do j=1, (n(i)-1)
            integral(i) = integral(i) + 2 * integrand(a + j * h(i))
        end do
        integral(i) = (h(i) * integral(i)) / 2.0d0
        error(i) = abs(0.9972 - integral(i))

        write(unit, *) n(i), error(i)
    end do

    close(unit)  

contains

    function integrand(x)
        double precision :: integrand
        double precision, intent(in) :: x
        integrand = (exp(-(x**2)/2))/sqrt(2*pi)
    end function integrand

end program trapezoid_pi_bin

