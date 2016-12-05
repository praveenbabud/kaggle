#include <fcntl.h>
#include <stdio.h>
#include <string.h>
typedef unsigned long int big_int;
int main()
{
   int fd;
   char order[256];
   big_int toy,year,day,month,hours,minutes,duration;

   FILE *fp;
   fp = fopen("toys_rev2.csv", "r");

   fgets(order,256, fp);

    printf("\n%s\n", order); 
  
   strcpy(order, "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa");

   fgets(order,256, fp);

    printf("\n%s\n", order); 

  sscanf(order,"%ld,%ld %ld %ld %ld %ld,%ld",&toy,&year,&month,&day,&hours,&minutes,&duration);
  printf("toy = %ld, year = %ld, month = %ld, day = %ld, hours = %ld, minutes = %ld, duration = %ld\n", toy, year,month,day,hours,minutes, duration);
   fclose(fp);

}
