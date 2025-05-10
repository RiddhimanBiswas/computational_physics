program exponential_random
    implicit none
    integer :: i
    double precision :: rand_num, exp_rand_num

    call random_seed()

    open(unit=10, file='exponential_random.txt', status='replace')
    do i=1,10000
        call random_number(rand_num)
        exp_rand_num = - log(rand_num)/2
        write (10,*) exp_rand_num
    end do

    close(10)

end program exponential_random
