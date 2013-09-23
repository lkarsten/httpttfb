CC=clang

httpttfb: httpttfb.c
	$(CC) -Wall -o httpttfb httpttfb.c -lrt
