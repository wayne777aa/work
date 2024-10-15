all: main

main: 112550020_lab10-2.o
	gcc -o main 112550020_lab10-2.o

112550020_lab10-2.o: 112550020_lab10-2.c 
	gcc -c 112550020_lab10-2.c

clean:
	rm main 112550020_lab10-2.o


# ./main < sample_input.in
# // input
# ./main > output.out 
# // output
# ./main < sample_input.in > output.out 
# // input + output

# diff sample_output.out output.out 