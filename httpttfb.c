/*

httpttfb - measure time to first byte.

See the README file for more information.
License: MIT

Author: Lasse Karstensen <lkarsten@varnish-software.com>, September 2013.
*/

#include <sys/types.h>
#include <sys/socket.h>
#include <stdio.h>
#include <errno.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <netdb.h>

#define timersub(a, b, result)                                       \
  do {                                                               \
    result.tv_sec = a.tv_sec - b.tv_sec;                             \
    result.tv_nsec = a.tv_nsec - b.tv_nsec;                          \
    if (result.tv_nsec < 0) {                                        \
      --result.tv_sec;                                               \
      result.tv_nsec += 1000000000;                                  \
    }                                                                \
  } while (0)

const char req[] = \
	"GET / HTTP/1.1\r\nHost: localhost\nAccept-Encoding: gzip\r\n\r\n";

#define USE_TCP_FASTOPEN 1

/*
 *  Run `runs` requests against an addrinfo `dest` (-ination) and
 *  write timing information to stdout.
*/
int do_run(struct addrinfo * dest, int runs) {
	int sockfd, i;

	struct timespec t1, t2;
	struct timespec delta;

	char buf[128] = "";

	ssize_t r;

	for (i=0; i < runs; i++) {
		sockfd = socket(dest->ai_family, dest->ai_socktype, dest->ai_protocol);

		if (clock_gettime(CLOCK_MONOTONIC_RAW, &t1) != 0) {
			perror("clock");
		}
#ifdef USE_TCP_FASTOPEN
		r = sendto(sockfd, req, sizeof req, MSG_FASTOPEN, dest->ai_addr, dest->ai_addrlen);
		if (r < 0) {
			fprintf(stderr, "%s\n", strerror(errno));
			close(sockfd);
			exit(EXIT_FAILURE);
		}
#else
		r = connect(sockfd, dest->ai_addr, dest->ai_addrlen);
		if (r < 0) {
			fprintf(stderr, "%s\n", strerror(errno));
			close(sockfd);
			exit(EXIT_FAILURE);
		}
		write(sockfd, req, sizeof req);
#endif

		r = read(sockfd, &buf, 1);

		if (clock_gettime(CLOCK_MONOTONIC_RAW, &t2) != 0) {
			perror("clock");
		}
		// printf("%s", buf);

		if (!r) {
			fprintf(stderr, "read error: %s\n", strerror(errno));
			printf("NaN\n");
		} else {
			timersub(t2, t1, delta);
			printf("%lld.%.9ld\n", (long long)delta.tv_sec, delta.tv_nsec);
		}
		close(sockfd);
	}
	return(0);
}



int main(int argc, char *argv[]) {
	struct addrinfo hints;
	struct addrinfo *result;

	int s, runs;

	printf(req);

	if (argc < 4) {
	   fprintf(stderr, "Usage: %s <host> <port> <runs>\n", argv[0]);
	   exit(EXIT_FAILURE);
	}

	runs = atoi(argv[3]);

	memset(&hints, 0, sizeof(struct addrinfo));
	hints.ai_family = AF_UNSPEC;
	hints.ai_socktype = SOCK_STREAM;

	s = getaddrinfo(argv[1], argv[2], &hints, &result);
	if (s != 0) {
	   fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(s));
	   exit(EXIT_FAILURE);
	}

	// use the first result returned by getaddrinfo.
	do_run(result, runs);

	freeaddrinfo(result);
	return(EXIT_SUCCESS);
}


