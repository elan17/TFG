#include <stdlib.h>

int main(int argc, char const *argv[]) {
    int n = atoi(argv[1]);
    return fac(n);
}

int fac(int n){
    int y = 1;
    for (int i = 1; i < n-1; i++) {
      y = y = (y*i) % n;
    }
    return y;
}
