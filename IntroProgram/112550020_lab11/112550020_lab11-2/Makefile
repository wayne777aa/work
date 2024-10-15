all: main

main: main.o ta_lib.o
	gcc -o main main.o ta_lib.o

main.o: main.c 
	gcc -c main.c

clean:
	rm main main.o
