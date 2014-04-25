CC=clang

all: httpttfb

httpttfb: httpttfb.c
	$(CC) -Wall -o httpttfb httpttfb.c -lrt

uncrustify: httpttfb.c
	uncrustify -c /usr/share/uncrustify/linux.cfg httpttfb.c
