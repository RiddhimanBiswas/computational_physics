program random_numbers_distribution
    implicit none
    integer :: i, j, num_bins, sum_bin, tot_rand_num, tot_sum, max_value, min_value
    integer, allocatable :: hist_values(:)
    double precision, allocatable :: rand_num_dist(:), norm_hist_values(:)
    double precision :: rand_num, sum
    real :: bin_width

    tot_rand_num = 10000
    min_value = -1*tot_rand_num
    max_value = 1*tot_rand_num
    tot_sum = 10000
    bin_width = 5
    num_bins = int((max_value-min_value)/bin_width)
    allocate(rand_num_dist(tot_sum))
    allocate(hist_values(num_bins))
    allocate(norm_hist_values(num_bins))
    hist_values = 0
    norm_hist_values = 0

    call random_seed()

    do i=1,tot_sum
        sum = 0.0d0
        do j=1,tot_rand_num
            call random_number(rand_num)
            if (rand_num>=0.5) then
                sum = sum + 1
            else
                sum = sum - 1
            end if
        end do
        rand_num_dist(i) = sum
        sum_bin = int((sum-min_value)/bin_width)+1
        if (sum_bin>num_bins) then
            sum_bin = num_bins
        end if
        hist_values(sum_bin) = hist_values(sum_bin) + 1
    end do

    do i=1,num_bins
        norm_hist_values(i) = real(hist_values(i))/real(tot_sum*bin_width)
    end do

    open(unit=10, file='random_walk_bin_data_10.txt', status='replace')
    do i = 1, num_bins
        write(10, *)(min_value + (i - 0.5) * bin_width), hist_values(i), norm_hist_values(i)
    end do
    close(10)

end program random_numbers_distribution

