nelves <- 900
tree_size <- 10000000
orders_size <- 10000000
##orders_size <- 10000
hash_size <- 50000
one_to_150 <- 0
elvesrating <- numeric(nelves)
remaining_task <- numeric(nelves)
working_toy <- numeric(nelves) 
work_start_time <- numeric(nelves)
used_unsanctioned_time <- numeric(nelves)
used_sanctioned_time <- numeric(nelves)

orders_list_data <- numeric(tree_size)
orders_list_next <- numeric(tree_size)

free_orders_list <- 0
orders_list <- 0
orders_list_tail <- 0

zzz <- 0

list_data <- numeric(nelves)
list_next <- numeric(nelves)
list_prev <- numeric(nelves)

orders_tree_data <- numeric(hash_size)
orders_tree_left <- numeric(hash_size)
orders_tree_right <- numeric(hash_size)
orders_tree_root <- 0

orders_free_list <- 1

free_list <- 0
used_list <- 0
used_list_tail <- 0

orders_hash_table <- numeric(hash_size)

avgrating <- 1
add_to_hash_list <- function(duration, ToyId)
{
  if (orders_hash_table[duration] > 0)
  {
    tnode <- free_orders_list
    free_orders_list <<- orders_list_next[free_orders_list]
    
    orders_list_next[tnode] <<- 0
    orders_list_data[tnode] <<- ToyId
    
    head <- orders_hash_table[duration]
    
    orders_list_next[tnode] <<- head
    orders_hash_table[duration] <<- tnode
    
  }
  else
  {
    tnode <- free_orders_list
    free_orders_list <<- orders_list_next[free_orders_list]
    
    orders_list_next[tnode] <<- 0
    orders_list_data[tnode] <<- ToyId
    
    orders_hash_table[duration] <<- tnode
    add_to_orders_tree(duration)
  }
}
 
delete_from_orders_hash_list <- function(duration)
{
  tnode <- 0
  return_value <- 0
  if (orders_hash_table[duration] > 0)
  {
     head <- orders_hash_table[duration]
     orders_hash_table[duration] <<- orders_list_next[head]
     tnode <- head
     return_value <- orders_list_data[head]
  }
  if (tnode != 0)
  {
    orders_list_next[tnode] <<- free_orders_list
    free_orders_list <<- tnode
  }
  if (orders_hash_table[duration] == 0)
  {
    delete_from_orders_tree(duration)
  }
  return_value
}
     
     
 

####



delete_from_orders_tree <- function(duration)
{
  if (orders_tree_root != 0)
  {
    tnode <- orders_tree_root
    pnode <- 0
    while ((tnode != 0) &&
             (duration != orders_tree_data[tnode]))
    {
      pnode <- tnode
      if (duration < 
            orders_tree_data[tnode])
      {
        tnode <- orders_tree_left[tnode]
      }
      else
      {
        tnode <- orders_tree_right[tnode]
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
             orders_tree_left[pnode] <<-  orders_tree_right[tnode]
           }
           else
           {
             orders_tree_right[pnode] <<- orders_tree_right[tnode]
           }
        }
        else
        {
          orders_tree_root <<- orders_tree_right[tnode]
        }
      }
      else if ((orders_tree_right[tnode] == 0) &&
                 (orders_tree_left[tnode] != 0))
      {
        if (pnode != 0)
        {
          if (orders_tree_left[pnode] == tnode)
          {
            orders_tree_left[pnode] <<-  orders_tree_left[tnode]
          }
          else
          {
            orders_tree_right[pnode] <<- orders_tree_left[tnode]
          }
        }
        else
        {
          orders_tree_root <<- orders_tree_left[tnode]
        }
      }
      else if ((orders_tree_right[tnode] == 0) && 
                 (orders_tree_left[tnode] == 0))
      {
        if (pnode == 0)
        {
          orders_tree_root <<- 0
        }
        else
        {
          if (orders_tree_left[pnode] == tnode)
          {
            orders_tree_left[pnode] <<- 0
          }
          else
          {
            orders_tree_right[pnode] <<- 0
          }
        }
      }
      else
      {
        ## both right and left child are present
        ## find minimum of right sub tree and make it root
        
        itr_for_min <- orders_tree_right[tnode]
        pmin <- tnode
        while (orders_tree_left[itr_for_min] != 0)
        {
          pmin <- itr_for_min
          itr_for_min <- orders_tree_left[itr_for_min]
        }
        
        if (orders_tree_left[pmin] == itr_for_min)
        {
          orders_tree_left[pmin] <<- orders_tree_right[itr_for_min]
        }
        else
        {
          orders_tree_right[pmin] <<- orders_tree_right[itr_for_min]
        }
        
        orders_tree_right[itr_for_min] <<- orders_tree_right[tnode]
        orders_tree_left[itr_for_min] <<- orders_tree_left[tnode]
        
        if (pnode == 0)
        {
          orders_tree_root <<- itr_for_min
        }
        else
        {
          if (tnode == orders_tree_left[pnode])
          {
            orders_tree_left[pnode] <<- itr_for_min
          }
          else
          {
            orders_tree_right[pnode] <<- itr_for_min
          }  
        }
      }
      orders_tree_data[tnode] <<- orders_free_list
      orders_free_list <<- tnode 
    }
    
  }
}
add_to_orders_tree <- function(duration)
{
  if(orders_tree_root == 0)
  {
    tnode <- orders_free_list
    orders_free_list <<- orders_tree_data[orders_free_list]
    
    orders_tree_data[tnode] <<- duration
    orders_tree_left[tnode] <<- 0
    orders_tree_right[tnode] <<- 0
    orders_tree_root <<- tnode
  }
  else
  {
    tnode <- orders_tree_root
    pnode <- 0
    while ((tnode != 0) &&
           (duration != orders_tree_data[tnode]))
    {
      pnode <- tnode
      if (duration < 
            orders_tree_data[tnode])
      {
        tnode <- orders_tree_left[tnode]
      }
      else
      {
        tnode <- orders_tree_right[tnode]
      }
    }
    if (tnode == 0)
    {
      nnode <- orders_free_list
      orders_free_list <<- orders_tree_data[orders_free_list]
      
      orders_tree_data[nnode] <<- duration
      orders_tree_left[nnode] <<- 0
      orders_tree_right[nnode] <<- 0
      if (duration < 
            orders_tree_data[pnode])
      {
        orders_tree_left[pnode] <<- nnode
      }
      else
      {
        orders_tree_right[pnode] <<- nnode
      }
    }
  }
}
    
get_from_orders_tree_lt <- function(lt)
{
  return_value <- 0
  if (orders_tree_root == 0)
  {
    return_value <- 0
  }
  else
  {
    min <- 0
    tnode <- orders_tree_root
    pnode <- 0
    while ((tnode != 0)  && 
           (orders_tree_data[tnode] != lt))
    {
      pnode <- tnode
      
      if (lt < orders_tree_data[tnode])
      {
        tnode <- orders_tree_left[tnode]
      }
      else
      {
          min <- orders_tree_data[tnode]
          tnode <- orders_tree_right[tnode]
      }
    }
    if (tnode == 0)
    {
      return_value <- min
    }
    else
    {
      return_value <- orders_tree_data[tnode]
    }
  }
  return_value
}
get_from_orders_tree_min <- function()
{
  return_value <- 0
  
  if (orders_tree_root == 0)
  {
    return_value <- 0
  }
  else
  {
    tnode <- orders_tree_root
    pnode <- 0
    while (orders_tree_left[tnode] != 0)
    {
      pnode <- tnode
      tnode <- orders_tree_left[tnode]
    }
    return_value <- orders_tree_data[tnode]
    if (1 == 3)
    if (pnode == 0)
    {
      return_value <- orders_tree_data[tnode]
      orders_tree_root <<- orders_tree_right[orders_tree_root]
      
      orders_tree_data[tnode] <<- orders_free_list
      orders_free_list <<- tnode 
    }
    else
    {
      return_value <- orders_tree_data[tnode]
      orders_tree_left[pnode] <<- orders_tree_right[tnode]
      
      orders_tree_data[tnode] <<- orders_free_list
      orders_free_list <<- tnode 
    } 
  }
  return_value
}

get_from_orders_tree_max <- function()
{
  return_value <- 0
  
  if (orders_tree_root == 0)
  {
    return_value <- 0
  }
  else
  {
    tnode <- orders_tree_root
    pnode <- 0
    while (orders_tree_right[tnode] != 0)
    {
      pnode <- tnode
      tnode <- orders_tree_right[tnode]
    }
    return_value <- orders_tree_data[tnode]
    if (1 == 3)
    if (pnode == 0)
    {
      return_value <- orders_tree_data[tnode]
      orders_tree_root <<- orders_tree_left[orders_tree_root]
      
      orders_tree_data[tnode] <<- orders_free_list
      orders_free_list <<- tnode 
    }
    else
    {
      return_value <- orders_tree_data[tnode]
      orders_tree_right[pnode] <<- orders_tree_left[tnode]
      
      orders_tree_data[tnode] <<- orders_free_list
      orders_free_list <<- tnode 
    } 
  }
  return_value
}


balance_tree  <- function()
{
  ##sorted_orders <- numeric(0)
  ##while(orders_tree_root != 0)
  {
   ## sorted_orders <- c(sorted_orders, get_from_orders_tree_min())
  } 
  ##real_balance_tree(sorted_orders)
}
real_balance_tree <- function(sorted_orders)
{
  if (length(sorted_orders) > 0)
  {
  stack_start <- numeric(0)
  stack_end <- numeric(0)
  stack_start <- c(stack_start,1)
  stack_end <- c(stack_end, length(sorted_orders))
  
  while (length(stack_start) > 0)
  {
    s <- stack_start[1]
    e <- stack_end[1]
    if (length(stack_start) == 1)
    {
      stack_start <- numeric(0)
      stack_end <- numeric(0)
    }
    else
    {
      stack_start <- stack_start[2:length(stack_start)]
      stack_end <- stack_end[2:length(stack_end)]
    }
    if (s == e)
    {
      add_to_orders_tree(sorted_orders[s])
    }
    else if ((e - s) == 1)
    {
      add_to_orders_tree(sorted_orders[s])
      add_to_orders_tree(sorted_orders[e])
    }
    else
    {
      r <- as.integer((s + e)/2)
      add_to_orders_tree(sorted_orders[r])
      stack_start <- c((r + 1), stack_start)
      stack_end <- c(e, stack_end)
      
      stack_start <- c(s, stack_start)
      stack_end <- c((r - 1), stack_end)
    }
  }
  }
}
  
 


add_to_list <- function(elvesId)
{
  
   if(used_list == 0)
   {
     used_list <<- elvesId
     list_next[used_list] <<- 0
     list_prev[used_list] <<- 0
     list_data[used_list] <<- elvesId
     used_list_tail <<- used_list
   }
   else
   {
     if (elvesrating[elvesId] >= elvesrating[list_data[used_list]])
     {
       tnode <- elvesId
       list_next[tnode] <<- used_list
       list_data[tnode] <<- elvesId
       list_prev[tnode] <<- 0
       list_prev[used_list] <<- tnode
       used_list <<- tnode
     }
     else
     {
       pnode <- used_list
       tnode <- list_next[used_list]
      ##cat("pnode", pnode, "tnode", tnode,
       ##  "\n", sep=" ", file=zz, append=TRUE)
       while(tnode != 0 && (elvesrating[elvesId] <= elvesrating[tnode]))
       {
         pnode <- tnode
         tnode <- list_next[tnode]
         ##cat("in loop pnode", pnode, "tnode", tnode,
           ##"\n", sep=" ", file=zz, append=TRUE)
       }
       fnode <- elvesId
       list_data[fnode] <<- elvesId
       list_next[fnode] <<- tnode
       list_prev[fnode] <<- pnode
       list_next[pnode] <<- fnode
       if (tnode == 0)
       {
          used_list_tail <<- fnode
       }
       else
       {
         list_prev[tnode] <<- fnode
       }
       
     }
     
   }
}

get_from_list <- function()
{
  return_value <- 0
  if (used_list != 0)
  {
    return_value <- used_list
    tnode <- used_list
    used_list <<- list_next[used_list]
    if (used_list == 0)
    {
      used_list_tail <<- 0
    }
    else
    {
      list_prev[used_list] <<- 0
    }
    
  }
  return_value
}
add_to_free_list <- function(elvesId)
{
  list_next[elvesId] <<- free_list
  free_list <<- elvesId
}
delete_from_free_list <- function(elvesId)
{
  tnode <- free_list
  pnode <- 0
  while ((tnode != 0) && (tnode != elvesId))
  {
    pnode <- tnode
    tnode <- list_next[tnode]
  }
  if (tnode != 0)
  {
    if (pnode == 0)
    {
      tnode <- list_next[tnode]
      free_list <<- tnode
    }
    else
    {
      list_next[pnode] <<- list_next[tnode]
    }
  }    
}
  

get_from_list_bottom <- function()
{
  return_value <- 0
  if (used_list != 0)
  {
    return_value <- used_list_tail
    tnode <- used_list_tail
    used_list_tail <<- list_prev[used_list_tail]
    if (used_list_tail == 0)
    {
      used_list <<- 0
    }
    else
    {
      list_next[used_list_tail] <<- 0
    }
  }
  return_value
}
zz <- 0
##orders <- read.csv("toys_rev2.csv",colClasses=c("numeric","character","numeric"))
##orders$Start_time <- character(nrow(orders))
##orders$End_time <- character(nrow(orders))
##orders$ElvesId <- numeric(nrow(orders))
##orders$ElvesRating <- numeric(nrow(orders))
index_orders_received <- 1
##queued_orders <- data.frame(ToyId=numeric(0),Arrival_time=character(0),Duration=numeric(0))

queued_orders <- numeric(0)


should_we_take_up_order <- function(hours, minutes, rating, duration)
{
  return_value <- 0
  
  mins_to_finish <- ceiling(duration/rating)
  
  mins_to_end_of_day <- (19 - hours) * 60 - minutes
  if (mins_to_finish <= mins_to_end_of_day)
  {
    return_value <- 1
  }
  else if (mins_to_finish > 2880)
  {
    return_value <- 1
  }
  else if ((mins_to_finish >=600) && (mins_to_finish <= 2880) && 
             (mins_to_end_of_day == 600))
 {
   ##if (mins_to_finish > (mins_to_end_of_day + 840))
   ###{
   ##  ratio <- (mins_to_finish - 840)/mins_to_finish
  ## }
 ##  else
  ## {
 ##    ration <- mins_to_end_of_day/mins_to_finish
  ## }
  ## if (mins_to_finish > 0.41)
   ##{
     return_value <- 1
   ##}
 }
 else
 {
   
  ## if (((mins_to_end_of_day)/(mins_to_finish - mins_to_end_of_day)) > 5.321)
 ## {
   ##  return_value <- 1
 ## }
 }
 return_value
}       

assign_orders_to_elves <- function(current_time)
{
  can_we_assign_now <- 0
  str_current_time <- strftime(current_time, "%Y %m %d %H %M")
  hours <- as.numeric(strftime(current_time, "%H"))
  minutes <- as.numeric(strftime(current_time, "%M"))
  
  if ((hours == 9) && (minutes == 0))
  {
    one_to_150 <<- sum(orders_hash_table[1:150])
    ##balance_tree()
  }
  
  if (hours >= 9 && hours <=18)
  {
    can_we_assign_now <- 1
  }
  else
  {
    can_we_assign_now <- 0
  }
  
  if (can_we_assign_now == 1)
  {
    ## sort elves based on rating
    ## sort queued orders based on duration
    
    ##cat("orders in queue", nrow(queued_orders),
       ## "\n", sep=" ", file=zz, append=TRUE)
  ##  if (nrow(queued_orders) > 0)
    ##if (length(queued_orders) > 0)
   ## {
      ##s_orders <- order(queued_orders$Duration, decreasing=TRUE)
      ##a_elves <- numeric(0)
     ## a_orders <- numeric(0)
      
      ## find an elve to work on the order
     ## j <- 0
     ## for (i in 1:length(queued_orders))
     ## {
      ##  j <- get_from_list()
      ##  
      ##  if (j == 0)
       ## {
       ##   break
      ##  }
      ##  else
      ##  {
       ##   a_elves <- c(a_elves, j)
       ##   a_orders <- c(a_orders, i)
      ##  }
      ##}## end of assigning tasks
    mins_to_end_of_day <- (19 - hours) * 60 - minutes
    a_elves <- numeric(0)
    a_orders <- numeric(0)
    add_back_elves <- numeric(0)
    add_back_orders <- numeric(0)
      toggle <- 1
    current_max_list <- 0
    current_min_list <- 0
    while(used_list != 0 && orders_tree_root != 0)
    {
      te <- get_from_list()
      ##if ((elvesrating[te] > avgrating) && (mins_to_end_of_day == 600))
      if ((elvesrating[te] >= 1) && (mins_to_end_of_day == 600))
      ##if ((elvesrating[te] >= 1))
      {
          ta <- get_from_orders_tree_max()
          if (ta == 0)
            break
          toyId <- delete_from_orders_hash_list(ta)
          a_elves <- c(a_elves, te)
          a_orders <- c(a_orders, toyId) 
      } 
      else
      {
        ta <- get_from_orders_tree_max()
        if (ta == 0)
          break
        can_do <- 0
        mins_to_finish <- ceiling(ta/elvesrating[te])
        if ((elvesrating[te] >= 1) && (mins_to_finish >= 2880))
        {
          can_do <- ta
        }
        else if (one_to_150 == 0)
        {
          can_do <- ta
        }
        else
        {
          can_do <- as.integer(elvesrating[te] * mins_to_end_of_day)
        }
        
        if (can_do > 0)
        {
          can_do <- get_from_orders_tree_lt(can_do)
        }
      
        if (can_do != 0)
        {
          ##if (((elvesrating[te] >= 1) && (can_do > 599)) || (elvesrating[te] < 1))
          {
            toyId <- delete_from_orders_hash_list(can_do)
            a_elves <- c(a_elves, te)
            a_orders <- c(a_orders, toyId)
          }
         ## else
         ## {
         ##   ta <- get_from_orders_tree_max()
          ##  toyId <- delete_from_orders_hash_list(ta)
          ##  a_elves <- c(a_elves, te)
         ##   a_orders <- c(a_orders, toyId)
            ##add_back_elves <- c(add_back_elves, te)
         ## }
        }
        else
        {
          add_back_elves <- c(add_back_elves, te)
          break
        }
      }
    }
        
        
     ## cat("a_elves", a_elves, "a_orders", a_orders, 
         ## "add_back_elves", add_back_elves, "add_back_orders", add_back_orders,
         ##"\n", sep=" ", file=zz, append=TRUE)
      if (length(add_back_elves) > 0)
      {
        for (zi in 1:length(add_back_elves))
        {
          add_to_list(add_back_elves[zi])
        }
      }
      if (length(add_back_orders) > 0)
      {
        real_balance_tree(add_back_orders)
        ##for (zi in 1:length(add_back_orders))
        ##{
        ##  add_to_orders_tree(add_back_orders[zi])
        ##}
      }
      if (length(a_orders) > 0)
      {
        for (k in 1:length(a_elves))
        {
          add_to_free_list(a_elves[k])
          remaining_task[a_elves[k]] <<- 
            ceiling((orders$Duration[a_orders[k]])/elvesrating[a_elves[k]])
            ##ceiling((queued_orders$Duration[a_orders[k]])/elvesrating[a_elves[k]])
          
          working_toy[a_elves[k]] <<- a_orders[k]
          work_start_time[a_elves[k]] <<- str_current_time
          ##orders$Start_time[queued_orders[a_orders[k]]] <<- str_current_time
          ##orders$ElvesId[queued_orders[a_orders[k]]] <<- a_elves[k]
          ##orders$ElvesRating[queued_orders[a_orders[k]]] <<- elvesrating[a_elves[k]]
         ## #cat("ElvesId", a_elves[k], "started working on order for toy",
            ## working_toy[a_elves[k]], "at", 
             ##work_start_time[a_elves[k]],               
             ##"rating is", elvesrating[a_elves[k]],
            ##  "\n", sep=" ", file=zz, append=TRUE)
        }
       ## queued_orders <<- queued_orders[-a_orders]
     ## }  
      
    }## end of orders are present
   
    ##cat("free elves after loop", toprint, 
      ##  "\n", sep=" ", file=zz, append=TRUE)
  }## end of time to assign
  
  
}

take_orders <- function(current_time)
{
  while ((index_orders_received <= orders_size) &&
         (current_time == strptime(orders$Arrival_time[index_orders_received],
                                   "%Y %m %d %H %M")))
  {
    ##tqo <- data.frame(ToyId=orders$ToyId[index_orders_received],
              ##        Arrival_time=orders$Arrival_time[index_orders_received],
                ##      Duration=orders$Duration[index_orders_received])
      ## cat("Queued order for toy", orders$ToyId[index_orders_received],
      ##  "at", orders$Arrival_time[index_orders_received], 
       ## "Duration is", orders$Duration[index_orders_received],
      ##  "\n", sep=" ", file=zz, append=TRUE)
    
    ##queued_orders <<- rbind(queued_orders, tqo)
    ##cat("orders in queue", nrow(queued_orders),
      ##  "\n", sep=" ", file=zz, append=TRUE)
    ##queued_orders <<- c(queued_orders, index_orders_received)
    add_to_hash_list(orders$Duration[index_orders_received], index_orders_received)
    index_orders_received <<- index_orders_received + 1
  }
}

calculate_rating_for_finished_tasks <- function (current_time)
{ 
  ##str_current_time <- strftime(current_time, "%Y %m %d %H %M")
  
  free_elves <- numeric(0)
  tnode <- free_list
  while (tnode != 0)
  {
    if(remaining_task[tnode] == 0 &&
       (used_sanctioned_time[tnode] > 0))
    {
      ##orders$End_time[working_toy[i]] <<- str_current_time
      dur <- used_sanctioned_time[tnode] + used_unsanctioned_time[tnode]
      elvesrating[tnode] <<- elvesrating[tnode] * (1.02 ^ (used_sanctioned_time[tnode]/60)) *
                        (0.9 ^ (used_unsanctioned_time[tnode]/60))
      if (elvesrating[tnode] > 4.0)
      {
        elvesrating[tnode] <<- 4.0
      }
      else if (elvesrating[tnode] < 0.25)
      {
        elvesrating[tnode] <<- 0.25
      }
      
      
      ##cat("Finished toy", working_toy[tnode], "by ElveId", tnode, "new rating", elvesrating[tnode],
          ##"Start Time", work_start_time[tnode], 
          ##"Duration", orders$Duration[working_toy[tnode]],
         ## "Used", dur,
         ## "\n", sep=" ", file=zz, append=TRUE)
      cat(working_toy[tnode], tnode, work_start_time[tnode], dur,
          "\n", sep=",", file=zzz, append=TRUE)
      used_sanctioned_time[tnode] <<- 0
      working_toy[tnode] <<- 0
    }
    if(remaining_task[tnode] == 0 &&
         (used_sanctioned_time[tnode] == 0) &&
         (used_unsanctioned_time[tnode] == 0))
    {
      free_elves <- c(free_elves, tnode)
    }
    tnode <- list_next[tnode]
  }
  if (length(free_elves) > 0)
  {
    for (i in 1:length(free_elves))
    {
      delete_from_free_list(free_elves[i])
      add_to_list(free_elves[i])
    }
  }
}

remove_one_minute_from_everything <- function (hours, minutes)                                           
{
  is_sanctioned_time <- 0
  
  
  if (hours == 9 && minutes > 0)
  {
    is_sanctioned_time <- 1
  }
  else if (hours > 9 && hours < 19)
  {
    is_sanctioned_time <- 1
  }
  else if (hours == 19 && minutes == 0)
  {
    is_sanctioned_time <- 1
  }
  

  if (is_sanctioned_time == 1)
  {
    ##cat("sanctioned time to remove a minute", 
      ##  "\n", sep=" ", file="logs.txt", append=TRUE)
    tnode <- free_list
    while(tnode != 0)
    {
      if (remaining_task[tnode] == 0)
      {
        if (used_unsanctioned_time[tnode] > 0)
        {
          used_unsanctioned_time[tnode] <<- used_unsanctioned_time[tnode] - 1
        }
      }
      else
      {
        remaining_task[tnode] <<- remaining_task[tnode] - 1
        used_sanctioned_time[tnode] <<- used_sanctioned_time[tnode] + 1
      }
      
      tnode <- list_next[tnode]
    }
  }## sanctioned
  else if ((hours == 9) && (minutes == 0))
  {
    ##cat("is not sanctioned time to remove a minute", 
     ##   "\n", sep=" ", file="logs.txt", append=TRUE)
    tnode <- free_list
    while(tnode != 0)
    {
      if (remaining_task[tnode] == 0)
      {
        ## nothing
      }
      else
      {
        if (remaining_task[tnode] >= 840)
        {
          remaining_task[tnode] <<- remaining_task[tnode] - 840
          used_unsanctioned_time[tnode] <<- used_unsanctioned_time[tnode] + 840
        }
        else
        {
          ttask <- remaining_task[tnode] 
          remaining_task[tnode] <<- 0
          used_unsanctioned_time[tnode] <<- used_unsanctioned_time[tnode] + ttask
        }
      }
      tnode <- list_next[tnode]
    }
  } 
}


runit <- function()
{
  ##elves id goes from 1 to nelves
  
  ##zz <<- file("logs.txt",open="at")
  zzz <<- file("final.txt",open="at")
  cat("ToyId","ElfId","StartTime","Duration",
      "\n", sep=",", file=zzz, append=FALSE)
  
  ##cat("Starting the Run", 
    ##  "\n", sep=" ", file=zz, append=FALSE)
  
  all_toys_built <- 0
  for (i in 1:nelves)
  {
    elvesrating[i] <<- 1.0
    remaining_task[i] <<- 0
    used_unsanctioned_time[i] <<- 0
    used_sanctioned_time[i] <<- 0
    working_toy[i] <<- 0
    list_data[i] <<- i
    list_next[i] <<- i + 1 
    list_prev[i] <<- i - 1
  }
  free_list <<- 0
  used_list <<- 1
  used_list_tail <<- nelves
  list_next[nelves] <<- 0
  
  orders_tree_root <<- 0
  orders_free_list <<- 1
  
  for (i in 1:hash_size)
  {
    orders_tree_data[i] <<- i + 1
    orders_hash_table[i] <<- 0
  }
  orders_tree_data[hash_size] <<- 0
  
  for (i in 1:tree_size)
  {
    orders_list_next[i] <<- i + 1
  }
  free_orders_list <<- 1
  orders_list_next[tree_size] <<- 0
  
  index_orders_received <<- 1
  
  
  start_time <- strptime("2014-01-01-00-00","%Y-%m-%d-%H-%M")
  
  current_time <- start_time
  
 ##Rprof("rprof_data.txt")
  
  while (all_toys_built == 0)
  {
    ## one minute is over so reduce one minute from all tasks
    hours <- as.numeric(strftime(current_time, "%H"))
    minutes <- as.numeric(strftime(current_time, "%M"))
    
    remove_one_minute_from_everything(hours, minutes)
    
    calculate_rating_for_finished_tasks(current_time)
    
    take_orders(current_time)
    if ( hours >= 9  && hours <= 18)
    {
      assign_orders_to_elves(current_time)
    }
  
    current_time <- current_time + 60 
    
   ## cat("current time =", strftime(current_time,"%Y %m %d %H %M"), 
       ## "orders received =", index_orders_received,
      ##  "orders_free_list =", orders_free_list,
      ##  "queued orders =", length(queued_orders),
     ##   "\n", sep=" ", file=zz, append=TRUE)
    
    if (index_orders_received > orders_size)
    {
      if (orders_tree_root == 0)
      {
        if (sum(remaining_task) == 0)
        {
          all_toys_built <- 1
        }
      }
    }

  }
  ##Rprof()
  ##summaryRprof("rprof_data.txt")
  print("Its Done")
  print(strftime(current_time,"%Y %m %d %H %M"))
  close(zz)
  
}