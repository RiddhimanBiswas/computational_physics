program average_rand_10
    implicit none

    integer :: i
    double precision :: rand_num, average, sum

    sum = 0.0d0
    open(unit=10,file='test_ran.dat',status='old',position='append')

    do i=1,10
        call random_number(rand_num)
        sum = sum + rand_num
    end do

    average = sum/10.0d0
    write(10,*) "Now calculating average of 10 random numbers"
    write(10,*) average

    close(10)
end program average_rand_10
