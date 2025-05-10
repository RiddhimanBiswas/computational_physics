program variables
        implicit none

        integer :: amount, age
        real :: pi
        complex :: frequency
        character :: initial
        logical :: isOkay

        print *, 'enter your age :'
        read (*,*) age

        amount = 10
        pi = 3.1415926873
        frequency = (1.0, -0.5)
        initial = 'R'
        isOkay = .true.

        print *, 'the amount is', amount
        print *, 'the pi is', pi

end program variables
