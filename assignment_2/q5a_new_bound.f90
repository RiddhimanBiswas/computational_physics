program brute_force_integral
    implicit none
    integer :: i, j, n, sum_num, bound
    double precision :: sum_rand(1000), val_integral(1000), x(3), y(3), x_squared, y_squared, x_y_squared, avg

    ! Parameters
    n = 10000
    sum_num = 1000
    bound = 8

    ! Initialize arrays
    sum_rand = 0.0d0
    val_integral = 0.0d0

    open(unit=10, file='brute_force_integral_new_bound.txt', status='replace')

    do i = 1, sum_num
        do j = 1, n
            x = mod_rand()  ! Corrected function call
            y = mod_rand()
            x_squared = norm_squared(x)
            y_squared = norm_squared(y)
            x_y_squared = norm_squared(x - y)
            sum_rand(i) = sum_rand(i) + exp(-x_squared - y_squared - (x_y_squared / 2))
        end do
        avg = sum_rand(i) / n
        val_integral(i) = avg * ((2.0d0 * bound) ** 6)
        write (10,*) val_integral(i)
    end do

    close(10)

contains

    function mod_rand() result(vec)
        double precision :: vec(3)
        integer :: i
        call random_seed()
        do i = 1, 3
            call random_number(vec(i))
            vec(i) = vec(i) * (2.0d0 * bound) - bound
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

end program brute_force_integral

