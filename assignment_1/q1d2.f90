program random_numbers_10seeds
    implicit none

    integer :: i,j
    double precision :: rand_num
    double precision :: rand_num_10(10,10)

    open(unit=10,file='test_ran_10_seeds.dat',status='replace')

    do i=1,10
        call random_seed()
        do j=1,10
            call random_number(rand_num)
            rand_num_10(i,j) = rand_num
        end do
    end do

    do i=1,10
        write(10,*)(rand_num_10(i,j), j=1,10)
    end do

    close(10)
end program random_numbers_10seeds
