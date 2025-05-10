program random_numbers_seed
    implicit none

    integer :: i
    double precision :: rand_num

    open(unit=10,file='test_ran.dat',status='old',position='append')

    call random_seed()

    do i=1,10
        call random_number(rand_num)
        write(10,*)rand_num
    end do

    close(10)
end program random_numbers_seed
