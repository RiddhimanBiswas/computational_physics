program trapezoid_pi
    implicit none
    integer :: i, a, b, n
    double precision :: h, sum

    a = 0 ! the start point
    b = 2*asin(1.0d0) ! the end point
    h = 0.0001d0 ! the rectangle width
    n = int((b-a)/h) ! the # of bins
    sum = 0.0d0 ! the integral

    sum = integrand(dble(a)) + integrand(dble(b))
    do i=1,(n-1)
        sum = sum + 2*integrand(a+i*h)
    end do

    sum = (h*sum)/2.0d0

    print *, 'The value of the integral is ', sum

contains

    function integrand(x)
        double precision :: integrand
        double precision, intent(in) :: x
        integrand = sin(x)
    end function integrand

end program trapezoid_pi
        
