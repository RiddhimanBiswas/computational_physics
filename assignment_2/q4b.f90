program gaussian_random
    implicit none
    integer :: i
    double precision :: mu, sigma, rand_num1, rand_num2, gaussian_rand_num, pi

    mu = 0
    sigma = 2
    pi = 2*asin(1.0d0)
    call random_seed()

    open(unit=10, file='gaussian_random.txt', status='replace')
    do i=1,10000
        call random_number(rand_num1)
        call random_number(rand_num2)
        gaussian_rand_num = sqrt(-2*log(rand_num1))*cos(2*pi*rand_num2)
        gaussian_rand_num = gaussian_rand_num*sigma + mu
        write (10,*) gaussian_rand_num
    end do

    close(10)

end program gaussian_random
