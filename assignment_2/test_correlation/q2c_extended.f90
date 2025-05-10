program random_numbers_generator
    implicit none
    integer :: i, j,  n, step
    double precision :: rand_num,  sum_mean, mean, sum_var, var
    double precision, allocatable :: rand_array(:), sum_acf(:), acf(:)

    n = 1000
    step = 999
    allocate(sum_acf(step))
    allocate(acf(step))
    sum_mean = 0.0d0
    sum_var = 0.0d0
    sum_acf = 0.0d0
    acf = 0.0d0
    allocate(rand_array(n))

    call random_seed()

    do i=1,n
        call random_number(rand_num)
        rand_array(i) = rand_num
        sum_mean = sum_mean + rand_num
        sum_var = sum_var + rand_num**2
    end do

    mean = sum_mean/n
    var = (sum_var/n) - mean**2

    print *, 'The mean of the random numbers is ', mean
    print *, 'The standard deviation of the random numbers is ', sqrt(var)

    open(unit=10, file='correlation_extended2.txt', status='replace')
    do i=1,step
        do j=1,n-i
            sum_acf(i) = sum_acf(i) + (rand_array(j)-mean)*(rand_array(j+i)-mean)/var
        end do
        acf(i) = sum_acf(i)/(n-i)
        write (10,*) i, acf(i)
    end do

    close(10)

end program random_numbers_generator
