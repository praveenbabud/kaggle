#include <stdio.h>
#include <time.h>

typedef unsigned long int big_int;

big_int a;

int main()
{
  struct tm time_str;
  time_t now = time( NULL);

    struct tm now_tm = *localtime( &now);


    struct tm then_tm = now_tm;
    then_tm.tm_sec += 50;   // add 50 seconds to the time

    mktime( &then_tm);      // normalize it

    printf( "%s\n", asctime( &now_tm));
    printf( "%s\n", asctime( &then_tm));
    printf( "%ld, %d\n", sizeof(a), 2^2);


    time_str.tm_year = 2001 - 1900;
    time_str.tm_mon = 7; 
    time_str.tm_mday = 4;
    time_str.tm_hour = 0;
    time_str.tm_min = 0;
    time_str.tm_sec = 1;
    time_str.tm_isdst = -1;
    now = mktime(&time_str);
    printf("%lu\n", sizeof(now));

    now_tm = *localtime(&now);
    printf( "%s\n", asctime( &now_tm));

    now = now + 60;
    now_tm = *localtime(&now);
    printf( "%s\n", asctime( &now_tm));

    return 0;
 //printf("%s", asctime(mktime((const struct tm *)(0)))); 
}

