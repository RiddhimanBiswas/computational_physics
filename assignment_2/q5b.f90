program importance_sampling_integral
    implicit none
    integer :: i, j, n, sum_num, bound
    double precision :: sum_rand(1000), val_integral, x(3), y(3), x_squared, y_squared, x_y_squared, weight, g_value, q_value
    double precision :: pi

    n = 10000
    sum_num = 1000
    bound = 5

    sum_rand = 0.0d0
    val_integral = 0.0d0
    pi = 2.0d0 * asin(1.0d0)  ! Define pi

    open(unit=10, file='importance_sampling_integral.txt', status='replace')

    do i = 1, sum_num
        do j = 1, n
            x = mod_rand()  
            y = mod_rand()
            x_squared = norm_squared(x)
            y_squared = norm_squared(y)
            x_y_squared = norm_squared(x - y)

            g_value = exp(-x_squared - y_squared - (x_y_squared / 2))
            q_value = (1.0d0/(2.0d0 * pi)**3) * exp(-0.5d0*(x_squared+y_squared))
            weight = g_value/q_value
            sum_rand(i) = sum_rand(i) + weight
        end do

        val_integral = sum_rand(i) / n
        write (10,*) val_integral
    end do

    close(10)

contains
    function mod_rand() result(vec)
        double precision :: vec(3), pi, rand1, rand2, mu, sigma
        integer :: i
        pi = 2*asin(1.0d0)
        mu = 0
        sigma = 1/sqrt(2.0d0)
        call random_seed()
        do i = 1, 3
            call random_number(rand1)
            call random_number(rand2)
            vec(i) = sqrt(-2*log(rand1))*cos(2*pi*rand2)
        end do
    end function mod_rand

    function norm_squared(vec) result(vec_squared)
        double precision, intent(in) :: vec(3)
        double precision :: vec_squared
        integer :: i

        vec_squared = 0.0d0  ! Initialize before summing
        do i = 1, 3
            vec_squared = vec_squared + vec(i) ** 2
        end do
    end function norm_squared

end program importance_sampling_integral

