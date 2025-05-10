#da_values=(0.01, 1)
#db_values=(1, 10, 100)
#alpha_values=(0.005, -0.005, 0.05, -0.05)
#beta_values=(10, -10, 1, -1)

#for L in "${da_values[@]}"; do
#        for M in "${db_values[@]}"; do
#                for N in "${alpha_values[@]}"; do
#                        for O in "${beta_values[@]}"; do
#                                echo "Running with $L, $M, $N, $O"
#                                echo -e "$L\n$M\n$N\n$O" | ./fitzhugh_nagumo
#                                echo -e "$L\n$M\n$N\n$O" | ./source_fitzhugh_nagumo
#                        done
#                done
#        done
#done

da_values=(0.01, 1)
db_values=(1, 10, 100)
source_values=0.01

for L in "${da_values[@]}"; do
        for M in "${db_values[@]}"; do
                for N in "${source_values[@]}"; do
                        echo "Running with $L, $M, $N"
                        echo -e "$L\n$M" | ./diffusion
                        echo -e "$L\n$M\n$N" | ./source_diffusion
                done
        done
done

