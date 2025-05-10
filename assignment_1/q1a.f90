program random_numbers
        implicit none

        integer :: i
        real*8 :: rand_num

        call random_seed()
        print *, '10 random numbers are :'
        do i = 1, 10
            call random_number(rand_num)
            print *, rand_num
        end do
end program random_numbers
