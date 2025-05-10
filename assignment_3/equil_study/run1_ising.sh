#!/bin/bash

# Define values for the first loop
L_values=(7 8 9 10)
niter=50000  # Fixed value
T_values=(4.1 4.3 4.5 4.7)
J_values=(-2 -1.75 -1.5 -1.25 -1 -0.75 -0.5 -0.25 0 0.25 0.5 0.75 1 1.25 1.5 1.75 2)

# First loop: Iterate over all combinations of L, T, and J_ising
for L in "${L_values[@]}"; do
    for T in "${T_values[@]}"; do
        for J in "${J_values[@]}"; do
            echo "Running with L=$L, niter=$niter, T=$T, J_ising=$J"
            echo -e "$L\n$niter\n$T\n$J" | ./ising
        done
    done
done

# Define values for the second loop
#L_values=(7 8 9 10)
#J_values=1

# Second loop: Iterate over all combinations of L and J_ising
#for L in "${L_values[@]}"; do
#    for J in "${J_values[@]}"; do
#        echo "Running with L=$L and J_ising=$J"
#        echo -e "$L\n$J" | ./ising2
#    done
#done

