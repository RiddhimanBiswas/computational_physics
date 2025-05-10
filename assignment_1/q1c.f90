program comment
    implicit none

    open(unit=10,file="test_ran.dat",status="old",position="append")

    write(10,'(A)') "Changing seed and generating 10 new random numbers"

    close(10)
end program comment
