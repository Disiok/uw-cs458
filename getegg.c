#include <stdio.h>
#include <stdlib.h>

int main(void) {
  printf("Running getegg.\n");
  printf("EGG Address: %p\n", getenv("EGG"));
}
