program correlation_random
    implicit none
    integer :: i, j, n, step
    double precision :: rand(10000), sum_mean, sum_var, mean, var
    double precision, allocatable :: sum_acf(:), rand_array(:), acf(:)

    n = 10000
    step = 100
    allocate(sum_acf(step))
    allocate(acf(step))
    sum_acf = 0.0d0
    acf = 0.0d0
    
    sum_mean = 0.0d0
    sum_var = 0.0d0
    mean = 0.0d0
    var = 0.0d0

    open(unit=10, file='exponential_random.txt', status='old', action='read')
    do i=1,n
        read(10,*) rand(i)
        sum_mean = sum_mean + rand(i)
        sum_var = sum_var + rand(i)**2
    end do
    close(10)

    mean = sum_mean/n
    var = sum_var/n - mean**2

    open(unit=10, file='correlation_exponential.txt', status='replace')
    do i=1,step
        do j=1,n-i
            sum_acf(i) = sum_acf(i) + ((rand(j)-mean)*(rand(j+i)-mean)/var)
        end do
        acf(i) = sum_acf(i)/(n-i)
        write (10,*) i, acf(i)
    end do
    close(10)

    sum_mean = 0.0d0
    sum_var = 0.0d0
    mean = 0.0d0
    var = 0.0d0

    open(unit=20, file='gaussian_random.txt', status='old', action='read')
    do i=1,n
        read(20,*) rand(i)
        sum_mean = sum_mean + rand(i)
        sum_var = sum_var + rand(i)**2
    end do
    close(20)

    mean = sum_mean/n
    var = sum_var/n - mean**2

    open(unit=20, file='correlation_gaussian.txt', status='replace')
    do i=1,step
        do j=1,n-i
            sum_acf(i) = sum_acf(i) + ((rand(j)-mean)*(rand(j+i)-mean)/var)
        end do
        acf(i) = sum_acf(i)/(n-i)
        write (20,*) i, acf(i)
    end do
    close(20)
end program correlation_random
