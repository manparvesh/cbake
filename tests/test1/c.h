#ifndef C_H
#define C_H

#include<stdio.h>
int print_something_from_c(){
    printf("c.h included\n");
    // return 0; // <- this will create a warnning, but since we are using the `-w` flag, it won't be displayed
}

#endif //C_H