program random_numbers_generator
    implicit none
    integer :: i
    double precision :: rand_num

    call random_seed()

    open(unit=10, file='random_number.txt', status='replace')
    do i=1,10000
        call random_number(rand_num)
        write (10,*) rand_num
    end do
    close(10)

end program random_numbers_generator
