all: main

main: main.o
	gcc -o main main.o game.o

main.o: main.c 
	gcc -c main.c

clean:
	rm main main.o
