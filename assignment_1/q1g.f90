program average_rand_10
    implicit none

    integer :: i
    double precision :: rand_num, average, sum, diff

    open(unit=10,file='test_ran.dat',status='old',position='append')

    sum = 0.0d0
    do i=1,100
        call random_number(rand_num)
        sum = sum + rand_num
    end do

    average = sum/100.0d0
    diff = abs(0.50d0-average)
    write(10,*) "Now calculating average of 100 random numbers"
    write(10,*) average
    write(10,*) "The absolute difference from 0.50"
    write(10,*) diff

    sum = 0.0d0
    do i=1,10000
        call random_number(rand_num)
        sum = sum + rand_num
    end do

    average = sum/10000.0d0
    diff = abs(0.50d0-average)
    write(10,*) "Now calculating average of 10000 random numbers"
    write(10,*) average
    write(10,*) "The absolute difference from 0.50"
    write(10,*) diff

    sum = 0.0d0
    do i=1,1000000
        call random_number(rand_num)
        sum = sum + rand_num
    end do

    average = sum/1000000.0d0
    diff = abs(0.50d0-average)
    write(10,*) "Now calculating average of 1000000 random numbers"
    write(10,*) average
    write(10,*) "The absolute difference from 0.50"
    write(10,*) diff


    close(10)
end program average_rand_10
