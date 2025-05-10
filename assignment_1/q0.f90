program variables
        implicit none

        character(len=15) :: name
        integer :: var_int
        real :: var_float
        double precision :: var_double

        name = 'Riddhiman'
        var_int = 2025
        var_float = 3.14159268
        var_double = 2.99D+8

        print *, 'name: ', name
        print *, 'value of the integer: ', var_int
        print *, 'value of the floating point: ', var_float
        print *, 'value of the double precision: ', var_double

end program variables
