#include <stdio.h>
#include <time.h>
#include <math.h>
#define nelves  900
#define tree_size 10000000
#define orders_size 10000000
#define hash_size 50000

typedef unsigned long int big_int;
typedef long double frac;

typedef struct orders_s {
                          big_int toy_id;
                          big_int year;
                          big_int month;
                          big_int day;
                          big_int hours;
                          big_int minutes;
                          big_int duration;
                          big_int actual_duration;
                          big_int start_year;
                          big_int start_month;
                          big_int start_day;
                          big_int start_hours;
                          big_int start_minutes;
                          big_int elves_id;
                        }orders_t;

orders_t orders[orders_size + 1]; 

void add_to_orders_tree(big_int duration);
void delete_from_orders_tree(big_int duration);
void read_orders_from_file()
{
   char order[256];
   big_int i;
   big_int toy,year,day,month,hours,minutes,duration;
   FILE *fp;

   fp = fopen("toys_rev2.csv", "r");

   fgets(order,256, fp);

   printf("\n%s\n", order); 
   i = 0; 
   while (fgets(order, 256, fp) != NULL)
   {
     sscanf(order,"%ld,%ld %ld %ld %ld %ld,%ld",
            &toy,&year,&month,&day,&hours,&minutes,&duration);
     orders[i].toy_id = toy;
     orders[i].year = year;
     orders[i].month = month;
     orders[i].day = day;
     orders[i].hours = hours;
     orders[i].minutes = minutes;
     orders[i].duration = duration;
     orders[i].elves_id = orders[i].start_month = orders[i].start_day = orders[i].start_hours = orders[i].start_minutes = orders[i].start_year = 0;
     i++;
   }
   printf("total orders read is %ld\n", i); 
   fclose(fp);
}

frac elvesrating[nelves + 1];
big_int remaining_task[nelves + 1];
big_int working_toy[nelves + 1];
big_int used_unsanctioned_time[nelves + 1];
big_int used_sanctioned_time[nelves + 1];

big_int orders_list_data[tree_size + 1];
big_int orders_list_next [tree_size + 1];

big_int free_orders_list = 0;
big_int orders_list = 0;
big_int orders_list_tail = 0;



big_int list_data[nelves + 1];
big_int list_next[nelves + 1];
big_int list_prev[nelves + 1];

big_int orders_tree_data[hash_size + 1];
big_int orders_tree_left[hash_size + 1];
big_int orders_tree_right[hash_size + 1];
big_int orders_tree_root = 0;

big_int orders_free_list = 1;

big_int free_list = 0;
big_int used_list = 0;
big_int used_list_tail = 0;

big_int orders_hash_table[hash_size + 1];
big_int one_to_150 = 0;
void add_to_hash_list(big_int duration, big_int ToyId)
{
  big_int tnode, head;
  if (orders_hash_table[duration] > 0)
  {
    tnode = free_orders_list;
    free_orders_list = orders_list_next[free_orders_list];
    
    orders_list_next[tnode] = 0;
    orders_list_data[tnode] = ToyId;
    
    head = orders_hash_table[duration];
    
    orders_list_next[tnode] = head;
    orders_hash_table[duration] = tnode;
  }
  else
  {
    tnode = free_orders_list;
    free_orders_list = orders_list_next[free_orders_list];
    
    orders_list_next[tnode] = 0;
    orders_list_data[tnode] = ToyId;
    
    orders_hash_table[duration] = tnode;
    add_to_orders_tree(duration);
  }
}

big_int delete_from_orders_hash_list(big_int duration)
{
  big_int tnode = 0;
  big_int return_value = 0;
  if (orders_hash_table[duration] > 0)
  {
     big_int head;
     head = orders_hash_table[duration];
     orders_hash_table[duration] = orders_list_next[head];
     tnode = head;
     return_value = orders_list_data[head];
  }
  if (tnode != 0)
  {
    orders_list_next[tnode] = free_orders_list;
    free_orders_list = tnode;
  }
  if (orders_hash_table[duration] == 0)
  {
    delete_from_orders_tree(duration);
  }
  return return_value;
}
     
void delete_from_orders_tree(big_int duration)
{
  big_int pnode,tnode,pmin,itr_for_min;

  if (orders_tree_root != 0)
  {
    tnode =  orders_tree_root;
    pnode =  0;
    while ((tnode != 0) &&
             (duration != orders_tree_data[tnode]))
    {
      pnode = tnode;
      if (duration < 
            orders_tree_data[tnode])
      {
        tnode = orders_tree_left[tnode];
      }
      else
      {
        tnode = orders_tree_right[tnode];
      }
    }
    if (tnode != 0)
    {
      if ((orders_tree_left[tnode] == 0) &&
            (orders_tree_right[tnode] != 0))
      {
        if (pnode != 0)
        {
           if (orders_tree_left[pnode] == tnode)
           {
             orders_tree_left[pnode] = orders_tree_right[tnode];
           }
           else
           {
             orders_tree_right[pnode] = orders_tree_right[tnode];
           }
        }
        else
        {
          orders_tree_root = orders_tree_right[tnode];
        }
      }
      else if ((orders_tree_right[tnode] == 0) &&
                 (orders_tree_left[tnode] != 0))
      {
        if (pnode != 0)
        {
          if (orders_tree_left[pnode] == tnode)
          {
            orders_tree_left[pnode] = orders_tree_left[tnode];
          }
          else
          {
            orders_tree_right[pnode] = orders_tree_left[tnode];
          }
        }
        else
        {
          orders_tree_root = orders_tree_left[tnode];
        }
      }
      else if ((orders_tree_right[tnode] == 0) && 
                 (orders_tree_left[tnode] == 0))
      {
        if (pnode == 0)
        {
          orders_tree_root = 0;
        }
        else
        {
          if (orders_tree_left[pnode] == tnode)
          {
            orders_tree_left[pnode] = 0;
          }
          else
          {
            orders_tree_right[pnode] = 0;
          }
        }
      }
      else
      {
       // ## both right and left child are present
        //## find minimum of right sub tree and make it root
        
        itr_for_min =  orders_tree_right[tnode];
        pmin =  tnode;
        while (orders_tree_left[itr_for_min] != 0)
        {
          pmin = itr_for_min;
          itr_for_min = orders_tree_left[itr_for_min];
        }
        
        if (orders_tree_left[pmin] == itr_for_min)
        {
          orders_tree_left[pmin] = orders_tree_right[itr_for_min];
        }
        else
        {
          orders_tree_right[pmin] = orders_tree_right[itr_for_min];
        }
        
        orders_tree_right[itr_for_min] = orders_tree_right[tnode];
        orders_tree_left[itr_for_min] = orders_tree_left[tnode];
        
        if (pnode == 0)
        {
          orders_tree_root = itr_for_min;
        }
        else
        {
          if (tnode == orders_tree_left[pnode])
          {
            orders_tree_left[pnode] =  itr_for_min;
          }
          else
          {
            orders_tree_right[pnode] = itr_for_min;
          }  
        }
      }
      orders_tree_data[tnode] = orders_free_list;
      orders_free_list = tnode ;
    }
    
  }
}     
 

void add_to_orders_tree(big_int duration)
{
  big_int tnode,pnode,nnode;
  if(orders_tree_root == 0)
  {
    tnode = orders_free_list;
    orders_free_list = orders_tree_data[orders_free_list];
    
    orders_tree_data[tnode] = duration;
    orders_tree_left[tnode] = 0;
    orders_tree_right[tnode] = 0;
    orders_tree_root = tnode;
  }
  else
  {
    tnode = orders_tree_root;
    pnode = 0;
    while ((tnode != 0) &&
           (duration != orders_tree_data[tnode]))
    {
      pnode = tnode;
      if (duration < 
            orders_tree_data[tnode])
      {
        tnode = orders_tree_left[tnode];
      }
      else
      {
        tnode = orders_tree_right[tnode];
      }
    }
    if (tnode == 0)
    {
      nnode = orders_free_list;
      orders_free_list = orders_tree_data[orders_free_list];
      
      orders_tree_data[nnode] = duration;
      orders_tree_left[nnode] = 0;
      orders_tree_right[nnode] = 0;
      if (duration < 
            orders_tree_data[pnode])
      {
        orders_tree_left[pnode] = nnode;
      }
      else
      {
        orders_tree_right[pnode] = nnode;
      }
    }
  }
}
    

big_int get_from_orders_tree_min()
{
  big_int pnode,tnode;
  big_int return_value = 0;
  
  if (orders_tree_root == 0)
  {
    return_value = 0;
  }
  else
  {
    tnode = orders_tree_root;
    pnode = 0;
    while (orders_tree_left[tnode] != 0)
    {
      pnode = tnode;
      tnode = orders_tree_left[tnode];
    }
    return_value = orders_tree_data[tnode];
  }
  return return_value;
}

big_int get_from_orders_tree_max()
{
  big_int return_value = 0;
  big_int pnode,tnode; 
  
  if (orders_tree_root == 0)
  {
    return_value = 0;
  }
  else
  {
    tnode = orders_tree_root;
    pnode = 0;
    while (orders_tree_right[tnode] != 0)
    {
      pnode = tnode;
      tnode = orders_tree_right[tnode];
    }
    return_value = orders_tree_data[tnode];
  }
  return return_value;
}


big_int get_from_orders_tree_lt(big_int lt)
{
  big_int return_value,min,tnode,pnode;
  return_value =  0;
  if (orders_tree_root == 0)
  {
    return_value =  0;
  }
  else
  {
    min = 0;
    tnode =  orders_tree_root;
    pnode =  0;
    while ((tnode != 0)  && 
           (orders_tree_data[tnode] != lt))
    {
      pnode = tnode;
      
      if (lt < orders_tree_data[tnode])
      {
        tnode =  orders_tree_left[tnode];
      }
      else
      {
          min = orders_tree_data[tnode];
          tnode = orders_tree_right[tnode];
      }
    }
    if (tnode == 0)
    {
      return_value =  min;
    }
    else
    {
      return_value = orders_tree_data[tnode];
    }
  }
  return return_value;
}


/*balance_tree  = function()
{
  sorted_orders = numeric(0)
  while(orders_tree_root != 0)
  {
    sorted_orders = c(sorted_orders, get_from_orders_tree_min())
  } 
  real_balance_tree(sorted_orders)
} */

typedef struct stack_s {
                       big_int array[hash_size];
                       big_int size;
                     }stack;

void init_stack(stack *s)
{
   s->size = 0;
}
void push(stack *s, big_int data)
{
    if (s->size == hash_size)
    {
       printf("\n stack overflow\n");
    }
    else
    {
       (s->array)[s->size] = data;
       s->size  = s->size + 1;
    }
}
big_int pop(stack *s)
{
   if (s->size == 0)
   {
      return 0;
   }
   else
   {
      s->size = s->size - 1; 
      return (s->array)[s->size];
   }
}
void real_balance_tree(stack *sorted_orders)
{
  stack start,end;
  big_int s,e,r;
  
  init_stack(&start);
  init_stack(&end);
 
  if (sorted_orders->size > 0)
  {
    init_stack(&start);
    init_stack(&end);
    push(&start,0);
    push(&end,(sorted_orders->size - 1));
  
    while (start.size > 0)
    {
      s = pop(&start);
      e = pop(&end);
      if (s == e)
      {
        add_to_orders_tree(sorted_orders->array[s]);
      }
      else if ((e - s) == 1)
      {
        add_to_orders_tree(sorted_orders->array[s]);
        add_to_orders_tree(sorted_orders->array[e]);
      }
      else
      {
        r = ((s + e)/2);
        add_to_orders_tree(sorted_orders->array[r]);
        push(&start, (r + 1));
        push(&end, e);
      
        push(&start, s);
        push(&end, (r - 1));
      }
    }
  }
}
  
 


void add_to_list(big_int elvesId)
{
   big_int tnode, pnode,fnode;
  
   if(used_list == 0)
   {
     used_list = elvesId;
     list_next[used_list] = 0;
     list_prev[used_list] = 0;
     list_data[used_list] = elvesId;
     used_list_tail = used_list;
   }
   else
   {
     if (elvesrating[elvesId] >= elvesrating[list_data[used_list]])
     {
       tnode = elvesId;
       list_next[tnode] = used_list;
       list_data[tnode] = elvesId;
       list_prev[tnode] = 0;
       list_prev[used_list] = tnode;
       used_list = tnode;
     }
     else
     {
       pnode = used_list;
       tnode = list_next[used_list];
       while(tnode != 0 && (elvesrating[elvesId] <= elvesrating[tnode]))
       {
         pnode = tnode;
         tnode = list_next[tnode];
       }
       fnode = elvesId;
       list_data[fnode] = elvesId;
       list_next[fnode] = tnode;
       list_prev[fnode] = pnode;
       list_next[pnode] = fnode;
       if (tnode == 0)
       {
          used_list_tail = fnode;
       }
       else
       {
         list_prev[tnode] = fnode;
       }
       
     }
     
   }
}

big_int get_from_list()
{
  big_int return_value, tnode;
  return_value = 0;
  if (used_list != 0)
  {
    return_value = used_list;
    tnode = used_list;
    used_list = list_next[used_list];
    if (used_list == 0)
    {
      used_list_tail = 0;
    }
    else
    {
      list_prev[used_list] = 0;
    }
    
  }
  return return_value;
}
void add_to_free_list(big_int elvesId)
{
  list_next[elvesId] = free_list;
  free_list = elvesId;
}
void delete_from_free_list(big_int elvesId)
{
  big_int tnode, pnode;
  tnode = free_list;
  pnode = 0;
  while ((tnode != 0) && (tnode != elvesId))
  {
    pnode = tnode;
    tnode = list_next[tnode];
  }
  if (tnode != 0)
  {
    if (pnode == 0)
    {
      tnode = list_next[tnode];
      free_list = tnode;
    }
    else
    {
      list_next[pnode] = list_next[tnode];
    }
  }    
}
  

big_int get_from_list_bottom()
{
  big_int  tnode;
  big_int return_value = 0;
  if (used_list != 0)
  {
    return_value = used_list_tail;
    tnode = used_list_tail;
    used_list_tail = list_prev[used_list_tail];
    if (used_list_tail == 0)
    {
      used_list = 0;
    }
    else
    {
      list_next[used_list_tail] = 0;
    }
  }
  return return_value;
}
big_int index_orders_received = 0;


/*
should_we_take_up_order = function(hours, minutes, rating, duration)
{
  return_value = 0
  
  mins_to_finish = ceiling(duration/rating)
  
  mins_to_end_of_day = (19 - hours) * 60 - minutes
  if (mins_to_finish <= mins_to_end_of_day)
  {
    return_value = 1
  }
  else if (mins_to_finish > 2880)
  {
    return_value = 1
  }
  else if ((mins_to_finish >=600) && (mins_to_finish <= 2880) && 
             (mins_to_end_of_day == 600))
 {
   ##if (mins_to_finish > (mins_to_end_of_day + 840))
   ###{
   ##  ratio = (mins_to_finish - 840)/mins_to_finish
  ## }
 ##  else
  ## {
 ##    ration = mins_to_end_of_day/mins_to_finish
  ## }
  ## if (mins_to_finish > 0.41)
   ##{
     return_value = 1
   ##}
 }
 else
 {
   
   if (((mins_to_end_of_day)/(mins_to_finish - mins_to_end_of_day)) > 5.321)
  {
     return_value = 1
  }
 }
 return_value
}
*/       
big_int sum_of(const big_int array[], big_int size)
{
  big_int i,sum;
  sum = 0; 
  for (i=1;i <= size;i++)
    sum = sum + array[i];
 return sum;
}
void assign_orders_to_elves(big_int year, big_int month, big_int day, big_int hours, big_int minutes)
{
  big_int can_we_assign_now;
  can_we_assign_now = 0;
  
  if ((hours == 9) && (minutes == 0))
  {
    one_to_150 = sum_of(orders_hash_table, 150);
    //lbalance_tree();
  }
  
  if (hours >= 9 && hours <=18)
  {
    can_we_assign_now = 1;
  }
  
  if (can_we_assign_now == 1)
  {
    stack a_elves,a_orders,add_back_elves,add_back_orders;
    big_int mins_to_end_of_day, ta, te, can_do,toyId;
    init_stack(&a_elves);
    init_stack(&a_orders);
    init_stack(&add_back_elves);
    init_stack(&add_back_orders);

    mins_to_end_of_day =  (19 - hours) * 60 - minutes;
    while(used_list != 0 && orders_tree_root != 0)
    {
      te = get_from_list();
      if ((elvesrating[te] >= 1) && (mins_to_end_of_day == 600))
      {
          ta = get_from_orders_tree_max();
          if (ta == 0)
            break;
          toyId = delete_from_orders_hash_list(ta);
          push(&a_elves, te);
          push(&a_orders, toyId);
      } 
      else
      {
        frac mins_to_finish;
        ta = get_from_orders_tree_max();
        if (ta == 0)
          break;
        can_do = 0;
        mins_to_finish = ceil((frac )ta/elvesrating[te]);
        if ((elvesrating[te] >= 1) && (mins_to_finish >= 2880))
        {
          can_do = ta;
        }
        else if (one_to_150 == 0)
        {
          can_do = ta;
        }
        else
        {
          can_do = (big_int) ceil(elvesrating[te] * mins_to_end_of_day);
        }
        
        if (can_do > 0)
        {
          can_do = get_from_orders_tree_lt(can_do);
        }
      
        if (can_do != 0)
        {
            toyId = delete_from_orders_hash_list(can_do);
            push(&a_elves, te);
            push(&a_orders, toyId);
        }
        else
        {
          push(&add_back_elves, te);
          break;
        }
      }
    }
    if (add_back_elves.size > 0)
    {
        big_int zi;
        for (zi = 0; zi < add_back_elves.size; zi++)
        {
          add_to_list(add_back_elves.array[zi]);
        }
    }
    if (add_back_orders.size > 0)
    {
        real_balance_tree(&add_back_orders);
    }
    if (a_orders.size > 0)
    {
      big_int k;
      for (k = 0; k < a_elves.size; k++)
      {
        add_to_free_list(a_elves.array[k]);
        remaining_task[a_elves.array[k]] = 
            ceil((orders[a_orders.array[k]].duration)/elvesrating[a_elves.array[k]]);
          
        working_toy[a_elves.array[k]] = a_orders.array[k];
        orders[a_orders.array[k]].start_year = year;
        orders[a_orders.array[k]].start_month = month;
        orders[a_orders.array[k]].start_day = day;
        orders[a_orders.array[k]].start_hours = hours;
        orders[a_orders.array[k]].start_minutes = minutes;
          
          /* cat("ElvesId", a_elves[k], "started working on order for toy",
             working_toy[a_elves[k]], "at", 
             work_start_time[a_elves[k]],               
             "rating is", elvesrating[a_elves[k]],
              "\n", sep=" ", file=zz, append=TRUE) */
      }
    }
   
  }
  
  
}

void take_orders(big_int year, big_int month,
                 big_int day,  big_int hours,
                 big_int minutes)
{
  while ((index_orders_received < orders_size) &&
         (year == orders[index_orders_received].year) &&
         (month == orders[index_orders_received].month) &&
         (day == orders[index_orders_received].day) &&
         (hours == orders[index_orders_received].hours) &&
         (minutes == orders[index_orders_received].minutes))
  {
       /*cat("Queued order for toy", orders$ToyId[index_orders_received],
        "at", orders$Arrival_time[index_orders_received], 
        "Duration is", orders$Duration[index_orders_received],
        "\n", sep=" ", file=zz, append=TRUE) */
    
    add_to_hash_list(orders[index_orders_received].duration, index_orders_received);
    index_orders_received = index_orders_received + 1;
  }
}

void calculate_rating_for_finished_tasks()
{ 
  big_int tnode, toy;
  stack free_elves; 
  init_stack(&free_elves);
  tnode = free_list;
  while (tnode != 0)
  {
    if(remaining_task[tnode] == 0 &&
       (used_sanctioned_time[tnode] > 0))
    {
      big_int dur;
      dur = used_sanctioned_time[tnode] + used_unsanctioned_time[tnode];
      elvesrating[tnode] = elvesrating[tnode] * powl(1.02 , (frac )used_sanctioned_time[tnode]/(frac)60) *
                        powl(0.9 , (frac )used_unsanctioned_time[tnode]/(frac )60);
      if (elvesrating[tnode] > 4.0)
      {
        elvesrating[tnode] = 4.0;
      }
      else if (elvesrating[tnode] < 0.25)
      {
        elvesrating[tnode] = 0.25;
      }
      toy = working_toy[tnode];
      printf("%ld,%ld,%ld %ld %ld %ld %ld,%ld\n",toy, tnode,orders[toy].start_year, orders[toy].start_month, orders[toy].start_day,
             orders[toy].start_hours, orders[toy].start_minutes, dur);
     /* 
      cat("Finished toy",  "by ElveId", tnode, "new rating", elvesrating[tnode],
          "Start Time", work_start_time[tnode], 
          "End Time", str_current_time,
          "\n", sep=" ", file=zz, append=TRUE)
      cat(working_toy[tnode], tnode, work_start_time[tnode], dur,
          "\n", sep=",", file="final.txt", append=TRUE) */
      used_sanctioned_time[tnode] = 0;
      working_toy[tnode] = 0;
    }
    if(remaining_task[tnode] == 0 &&
         (used_sanctioned_time[tnode] == 0) &&
         (used_unsanctioned_time[tnode] == 0))
    {
      push(&free_elves,tnode);
    }
    tnode = list_next[tnode];
  }
  if (free_elves.size > 0)
  {
    big_int i;
    for (i = 0; i < free_elves.size; i++)
    {
      delete_from_free_list(free_elves.array[i]);
      add_to_list(free_elves.array[i]);
    }
  }
}

void remove_one_minute_from_everything(big_int hours, big_int minutes)                                           
{
  big_int tnode;
  big_int is_sanctioned_time = 0;
   
  if (hours == 9 && minutes >= 1)
  {
    is_sanctioned_time = 1;
  }
  else if (hours > 9 && hours < 19)
  {
    is_sanctioned_time = 1;
  }
  else if (hours == 19 && minutes == 0)
  {
    is_sanctioned_time = 1;
  }

  if (is_sanctioned_time == 1)
  {
    tnode = free_list;
    while(tnode != 0)
    {
      if (remaining_task[tnode] == 0)
      {
        if (used_unsanctioned_time[tnode] > 0)
        {
          used_unsanctioned_time[tnode] = used_unsanctioned_time[tnode] - 1;
        }
      }
      else
      {
        remaining_task[tnode] = remaining_task[tnode] - 1;
        used_sanctioned_time[tnode] = used_sanctioned_time[tnode] + 1;
      }
      
      tnode = list_next[tnode];
    }
  }
  else if (hours == 9 && minutes == 0)
  {
    tnode = free_list;
    while(tnode != 0)
    {
      if (remaining_task[tnode] == 0)
      {
                ;
      }
      else
      {
        if (remaining_task[tnode] >= 840)
        {
          remaining_task[tnode] = remaining_task[tnode] - 840;
          used_unsanctioned_time[tnode] = used_unsanctioned_time[tnode] + 840;
        }
        else
        {
          big_int ttask;
          ttask = remaining_task[tnode];
          remaining_task[tnode] =  0;
          used_unsanctioned_time[tnode] = used_unsanctioned_time[tnode] + ttask;
        }
      }
      tnode = list_next[tnode];
    }
  } 
}


int main()
{
  big_int i;
  struct tm current_time;
  time_t current_time_t;
  big_int all_toys_built = 0;
 
  for (i=1; i <= nelves; i++)
  {
    elvesrating[i] = 1.0;
    remaining_task[i] = 0;
    used_unsanctioned_time[i] = 0;
    used_sanctioned_time[i] = 0;
    working_toy[i] = 0;
    list_data[i] = i;
    list_next[i] = i + 1 ;
    list_prev[i] = i - 1;
  }
  free_list = 0;
  used_list = 1;
  used_list_tail = nelves;
  list_next[nelves] = 0;
  
  orders_tree_root = 0;
  orders_free_list = 1;
  
  for (i =1; i <= hash_size; i++)
  {
    orders_tree_data[i] = i + 1;
    orders_hash_table[i] = 0;
  }
  orders_tree_data[hash_size] = 0;
  
  for (i = 1;i <= tree_size; i++)
  {
    orders_list_next[i] = i + 1;
  }
  free_orders_list = 1;
  orders_list_next[tree_size] = 0;
  
  index_orders_received = 0;
  
  
  current_time.tm_year = 2014 - 1900;
  current_time.tm_mon = 0; 
  current_time.tm_mday = 1;
  current_time.tm_hour = 0;
  current_time.tm_min = 0;
  current_time.tm_sec = 0;
  current_time.tm_isdst = -1;
  current_time_t = mktime(&current_time);
  
  read_orders_from_file();
  while (all_toys_built == 0)
  {
    current_time = *localtime(&current_time_t);
    
    remove_one_minute_from_everything(current_time.tm_hour, current_time.tm_min);
    
    calculate_rating_for_finished_tasks();
    
    take_orders(current_time.tm_year + 1900, (current_time.tm_mon + 1), current_time.tm_mday, current_time.tm_hour, current_time.tm_min);
    
    assign_orders_to_elves(current_time.tm_year + 1900, (current_time.tm_mon + 1), current_time.tm_mday, current_time.tm_hour, current_time.tm_min);
    
    if (index_orders_received > orders_size)
    {
      if (orders_tree_root == 0)
      {
        if (sum_of(remaining_task, nelves) == 0)
        {
          all_toys_built = 1;
        }
      }
    }
    current_time_t = current_time_t + 60;

  }
  printf("Its Done\n");
  current_time = *localtime(&current_time_t);
  printf( "%s\n", asctime(&current_time));
}
