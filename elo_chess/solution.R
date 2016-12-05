
library(stringr)

getPowerOfBlackMoves <- function(moves_in_game) {
        black_moves <- numeric()
        break_game_into_moves <- as.integer(unlist(str_split(str_trim(moves_in_game), " +")))
        for (i in 1:length(break_game_into_moves)) { 
                if (is.na(break_game_into_moves[i]) == TRUE) {
                  break
                }
                if (i %% 2 == 0){
                       black_moves <- c(black_moves, (break_game_into_moves[i - 1] - break_game_into_moves[i]))
                  if (break_game_into_moves[i - 1] != 0)
                  {
                    ##black_moves <- c(black_moves, (break_game_into_moves[i - 1] - break_game_into_moves[i])*100/abs(break_game_into_moves[i -1]))
                  }
                  else
                  {
                    ##black_moves <- c(black_moves, (break_game_into_moves[i - 1] - break_game_into_moves[i]))
                  }
                }
        }
        black_moves
}
getPowerOfWhiteMoves <- function(moves_in_game) {
  white_moves <- numeric()
  break_game_into_moves <- as.integer(unlist(str_split(str_trim(moves_in_game)," +")))
  for (i in 1:length(break_game_into_moves)) {
    if (is.na(break_game_into_moves[i]) == TRUE) {
      break
    }
    if (i %% 2 == 1){
      if ( i == 1) {
        white_moves <- c(white_moves,break_game_into_moves[1])
      }
      else {
         white_moves <- c(white_moves, (break_game_into_moves[i] - break_game_into_moves[i - 1]))
        if (break_game_into_moves[i - 1] != 0)
        {
          ##white_moves <- c(white_moves, ((break_game_into_moves[i]) - break_game_into_moves[i - 1])*100/abs(break_game_into_moves[i -1]))
          ##white_moves <- c(white_moves, ((break_game_into_moves[i]) - break_game_into_moves[i - 1])*100/abs(break_game_into_moves[i -1]))
          
        }
        else
        {
          ##white_moves <- c(white_moves, ((break_game_into_moves[i]) - break_game_into_moves[i - 1]))
        }
      }
    }
  }
  white_moves
}
extractGameDetails <- function(gamesFile) {
  
        cleanEvents <- numeric(25000)
        cleanWhiteElo <- numeric(25000)
        cleanBlackElo <- numeric(2500)
       
        dirtyEvents = grep(pattern="Event", x=gamesFile, value=TRUE)
        dirtyWhiteElo = grep(pattern="WhiteElo", x=gamesFile, value=TRUE)
        dirtyBlackElo = grep(pattern="BlackElo", x=gamesFile, value=TRUE)
        
        for (i in 1:25000)  {
          cleanEvents[i] <- as.integer(str_extract(dirtyEvents[i], "\\d+"))
          cleanWhiteElo[i] <- as.integer(str_extract(dirtyWhiteElo[i], "\\d+"))
          cleanBlackElo[i] <- as.integer(str_extract(dirtyBlackElo[i], "\\d+"))
                    
        }
        data.frame(cleanEvents, cleanWhiteElo, cleanBlackElo)
}

### compress data
##games <- readLines("data.pgn")
##moves <- read.csv("stockfish.csv", colClasses=c("integer", "character"))

##df <- extractGameDetails(games)
##uElo <- unique(c(df$cleanWhiteElo,df$cleanBlackElo))


compressData <- function(df, moves) {
  
         mean_of_good_moves <- numeric()
         mean_of_bad_moves <- numeric()
         mean_of_all_moves <- numeric()
         sd_of_good_moves <- numeric()
         sd_of_bad_moves <- numeric()
         sd_of_all_moves <- numeric()
         var_of_all_moves <- numeric()
         var_of_good_moves <- numeric()
         var_of_bad_moves <- numeric()
         df_elo_power <- data.frame(elo=numeric(0), power=numeric(0))
         
         uElo <- unique(c(df$cleanWhiteElo,df$cleanBlackElo))
        
         for (i in 1:length(uElo)) {
                 array_of_all_moves <- numeric()
                 
                 tdf <- df[df$cleanWhiteElo == uElo[i],]
                 ## loop through all white games of an ELO
                 for (j in 1:length(tdf$cleanEvents)) {
                          
                         singlegame <- moves$MoveScores[tdf$cleanEvents[j]]
                         ##print(singlegame)
                         array_of_all_moves <- c(array_of_all_moves, getPowerOfWhiteMoves(singlegame))    
                 }
                 ## df_e_p <- data.frame(elo=uElo[i],power=array_of_all_moves)
                ## df_elo_power <- rbind(df_elo_power, df_e_p)
                 
                 tdf <- df[df$cleanBlackElo == uElo[i],]
                 ## loop through all white games of an ELO
                 for (j in 1:length(tdf$cleanEvents)) {
                       singlegame <- moves$MoveScores[tdf$cleanEvents[j]]
                       array_of_all_moves <- c(array_of_all_moves, getPowerOfBlackMoves(singlegame))  
                 }
                 if (length(array_of_all_moves) > 0) {
                 df_e_p <- data.frame(elo=uElo[i],power=array_of_all_moves)
                 df_elo_power <- rbind(df_elo_power, df_e_p)
                 }
                 
                 mean_of_all_moves <- c(mean_of_all_moves,mean(array_of_all_moves))
                 sd_of_all_moves <- c(sd_of_all_moves,sd(array_of_all_moves))
                 var_of_all_moves <- c(var_of_all_moves,var(array_of_all_moves))
                 mean_of_good_moves <- c(mean_of_good_moves,mean(array_of_all_moves[array_of_all_moves > 0]))
                 sd_of_good_moves <- c(sd_of_good_moves,sd(array_of_all_moves[array_of_all_moves > 0]))
                 var_of_good_moves <- c(var_of_good_moves,var(array_of_all_moves[array_of_all_moves > 0]))
                 mean_of_bad_moves <- c(mean_of_bad_moves,mean(abs(array_of_all_moves[array_of_all_moves < 0])))
                 sd_of_bad_moves <- c(sd_of_bad_moves,sd(abs(array_of_all_moves[array_of_all_moves < 0])))
                 var_of_bad_moves <- c(var_of_bad_moves,var(abs(array_of_all_moves[array_of_all_moves < 0])))
         }
         ##data.frame(uElo, mean_of_all_moves, sd_of_all_moves, var_of_all_moves,
            ##        mean_of_good_moves, sd_of_good_moves, var_of_good_moves,
             ##       mean_of_bad_moves, sd_of_bad_moves, var_of_bad_moves)
         df_elo_power
}
estimateElo <- function(power_of_moves) {
 ##elo <- 0.0291 * (2056.6663 + 0.3748 * mean(power_of_moves)) +
       ## 0.2018 * (2226.1171 - 0.4443 * sd(power_of_moves)) +
  ##     0.1172 * (2140.5897 - 0.2389 * sd(power_of_moves[power_of_moves > 0])) +
       ## 0.2747 * (2219.243 - 2.417 * mean(power_of_moves[power_of_moves > 0])) +
        ## 0.2325 * (2152.120 + 1.275 * mean(power_of_moves[power_of_moves < 0])) +
        ##0.1447 * (2151.7559 - 0.2566 * sd(power_of_moves[power_of_moves < 0]))
  
  elo <- 0.3333 * (2226.1171 - 0.4443 * sd(power_of_moves)) +
         0.3333 * (2140.5897 - 0.2389 * sd(power_of_moves[power_of_moves > 0])) +
         0.3333 * (2151.7559 - 0.2566 * sd(power_of_moves[power_of_moves < 0]))
 elo
}

estimateWhiteBlackElo <- function(list_of_moves) {
  black <- getPowerOfBlackMoves(list_of_moves)
  white <- getPowerOfWhiteMoves(list_of_moves)
  print("White : ")
  print(estimateElo(white))
  print("Black : ")
  print(estimateElo(black))
    
}

predictElo <- function(df, moves) {
        wElo <- numeric()
        bElo <- numeric()
        for ( i in 1 : length(df$cleanEvents)) {
           black <- getPowerOfBlackMoves(moves$MoveScores[i])
           white <- getPowerOfWhiteMoves(moves$MoveScores[i])
          
           wElo <- c(wElo, estimateElo(white))
           bElo <- c(bElo, estimateElo(black))
        }
        data.frame(wElo,bElo)
}

createSample <- function(df){

        ## 1000 to 3000 sample at 50 elo point interval
        sampleEvents <- numeric()
        interval <- 50
        samples_per_interval <- 10
        minElo <- 1000
        maxElo <- 3000
        for (i in 1:((maxElo - minElo)/interval)) {
          tdf <- df[(df$cleanWhiteElo > (minElo + (i - 1) * interval) & df$cleanWhiteElo <= (minElo + i * interval)) |
                    (df$cleanBlackElo > (minElo + (i - 1) * interval) & df$cleanBlackElo <= (minElo + i * interval)),]
          sampleEvents <- c(sampleEvents, sample(df$cleanEvents, 
                                                 size = samples_per_interval, 
                                                 replace = FALSE))
        }
        df[df$cleanEvents %in% sampleEvents,]
}



buildTable <- function(df, moves) {
  
  minElo <- 1001
  maxElo <- 3000
  intervals <- 200
  isize <- 10
  
  
  mean_of_all_moves <- numeric(intervals)
  sd_of_all_moves <- numeric(intervals)
  
  for (i in 1:intervals)
  { 
          lelo <- minElo + (i - 1) * isize
          helo <- minElo +  i * isize
          array_of_all_moves <- numeric()
    
    
         for (j in 1:length(df$cleanEvents))
         {
                 singlegame <- moves$MoveScores[df$cleanEvents[j]]
      
                 if (df$cleanWhiteElo[j] >= lelo & df$cleanWhiteElo[j] <= helo)
                 {
                         array_of_all_moves <- c(array_of_all_moves, getPowerOfWhiteMoves(singlegame))
                }
                if (df$cleanBlackElo[j] >= lelo & df$cleanBlackElo[j] <= helo)
                {
                         array_of_all_moves <- c(array_of_all_moves, getPowerOfBlackMoves(singlegame))
                }
         }
         array_of_all_moves <- preprocessmoves(array_of_all_moves)
        
         if (length(array_of_all_moves) == 0)
         {
           mean_of_all_moves[i] <- 0
         
           sd_of_all_moves[i] <- 0
           
         }
         else
         {
          mean_of_all_moves[i] <- mean(array_of_all_moves, na.rm=TRUE)
          sd_of_all_moves[i] <- sd(array_of_all_moves, na.rm=TRUE)
         }
  }
  ta <- data.frame(mu=mean_of_all_moves,sigma=sd_of_all_moves)
  ta
         
}

int_f <- function(x, mu1, mu2, sd1, sd2) {
  f1 <- dnorm(x, mean=mu1, sd=sd1)
  f2 <- dnorm(x, mean=mu2, sd=sd2)
  pmin(f1, f2)
}


estimateEloTblN1 <- function(power_of_moves, tbl) 
{
  
  minElo <- 1001
  maxElo <- 3000
  intervals <- 200
  isize <- 10
  total_elo_for_all_moves <- numeric(0)
  weight <- 0
  
  ex <- 2.718 
  
  if (length(power_of_moves) > 0)
{
    for (k in 1:length(power_of_moves))
    {
      if (is.na(power_of_moves[k]) == FALSE)
      {
        if (power_of_moves[k] > 500)
          power_of_moves[k] <- 500
        
        if (power_of_moves[k] < -500)
          power_of_moves[k] <- -500
      }
    }
  }
if (length(power_of_moves) == 0)
{
  mu <- 0
  
  sigma <- 0
  
}
else
{
  mu <- mean(power_of_moves,na.rm=TRUE)
  sigma <- sd(power_of_moves,na.rm=TRUE)
}
  if (length(power_of_moves) > 0 & !is.na(mu) & !is.na(sigma))
  {
    
    
        for (j in 1:nrow(tbl))
        {
          if (tbl$sigma[j] != 0)
          {
            gu <- integrate(int_f, -501, 501, mu1=mu, mu2=tbl$mu[j], sd1=sigma, sd2=tbl$sigma[j])
            
             we <-  gu$value
               ##we <- 3 ^ (10 *  gu$value)
                 weight <- weight +  we
                 total_elo_for_all_moves <- c(total_elo_for_all_moves, (we * (minElo + (j - 0.5)*isize)))
             
          }
        }
        zk <- round(sum(total_elo_for_all_moves)/weight)
        zk
  }
  else
  {
         k <- 2245
         k
  }
}

estimateEloTblN2 <- function(power_of_moves, tbl) 
{
  
  minElo <- 1001
  maxElo <- 3000
  intervals <- 20
  isize <- 100
  total_elo_for_all_moves <- numeric(0)
  weight <- 0
  
  ex <- 2.718 
  
  mu <- mean(power_of_moves,na.rm=TRUE)
  sigma <- sd(power_of_moves,na.rm=TRUE)
  
  print(sigma)
  sigma
}
## integrate(int_f, -Inf, Inf, mu1=0, mu2=0.8, sd1=1, sd2=1)

estimateEloTbl <- function(power_of_moves, tbl) 
{
  
  minElo <- 1001
  maxElo <- 3000
  intervals <- 40
  isize <- 50
  total_elo_for_all_moves <- numeric(0)
  if (length(power_of_moves) > 0)
  {
    moves_used <- 0
  for (i in 1:length(power_of_moves)) {
       total_prob <- 0
       total_elo <- 0
       if (power_of_moves[i] != 500 & power_of_moves[i] != -500)
       {
         moves_used <- moves_used + 1
       for (j in 1:nrow(tbl))
       {
          if (tbl$sigma[j] != 0)
          {
              p_of_move <- pnorm(power_of_moves[i],mean=tbl$mu[j],sd=tbl$sigma[j], lower.tail=FALSE)
              ## pnorm(power_of_moves[i],mean=tbl$mu[j],sd=tbl$sigma[j], lower.tail=TRUE)
              total_prob <- total_prob + p_of_move
              total_elo <- total_elo + p_of_move * (minElo + (j - 0.5) * isize)      
          }
       }
       total_elo_for_all_moves <- c(total_elo_for_all_moves, total_elo/total_prob)
       }
  }
  sum(total_elo_for_all_moves/moves_used)
  }
  else
  {
    k <- 2245
    k
  }
}
predictEloTbl <- function(df, moves, tbl) {
  wElo <- numeric()
  bElo <- numeric()
  for ( i in 1 : length(df$cleanEvents)) {
    black <- getPowerOfBlackMoves(moves$MoveScores[i])
    white <- getPowerOfWhiteMoves(moves$MoveScores[i])
    
    wElo <- c(wElo, estimateEloTblN1(white,tbl))
    bElo <- c(bElo, estimateEloTblN1(black,tbl))
  }
  data.frame(wElo,bElo)
}
preprocessmoves <- function(moves)
{
  finalmoves <- numeric()
  if (length(moves) > 0)
  {
    for (k in 1:length(moves))
    {
      if (is.na(moves[k]) == FALSE) 
      {
        if (moves[k] < 300 && moves[k] > -300)
        {
          finalmoves <- c(finalmoves, moves[k])
        }
        else
        {
          if (moves[k] > 0)
            finalmoves <- c(finalmoves, 300)
          else
            finalmoves <- c(finalmoves, -300)
        }
      }
    }
  }
  finalmoves
}
getMeanSdGames <- function(df, moves) {
  
  maxmoves <- length(allmoves)
  mu <- numeric()
  sigma <- numeric()
  elos <- numeric()
  for ( i in 1 : length(df$cleanEvents)) {
    black <- getPowerOfBlackMoves(moves$MoveScores[df$cleanEvents[i]])
    white <- getPowerOfWhiteMoves(moves$MoveScores[df$cleanEvents[i]])
    
    black <- prob_of_better_move(black,maxmoves)
    white <- prob_of_better_move(white,maxmoves)
    
    
    if (sum(!is.na(white)) > 0)
    {
    mu <- c(mu, mean(white,na.rm=TRUE))
    
    sigma <- c(sigma, sd(white, na.rm=TRUE))
    }
    else
    {
      mu <- c(mu, 0)
      
      sigma <- c(sigma, 0)
    }
    elos <- c(elos,df$cleanWhiteElo[i])
    if (sum(!is.na(black)) > 0)
    {
    mu <- c(mu, mean(black,na.rm=TRUE))
    
    sigma <- c(sigma, sd(black, na.rm=TRUE))
    }
    else
    {
      mu <- c(mu, 0)
      
      sigma <- c(sigma, 0)
    }
    elos <- c(elos,df$cleanBlackElo[i])
  }
  data.frame(mu,sigma,elos)
}

getallmoves <- function(df, moves) {
 movesa <- numeric()
  
  for ( i in 1 : length(df$cleanEvents)) {
    black <- getPowerOfBlackMoves(moves$MoveScores[df$cleanEvents[i]])
    white <- getPowerOfWhiteMoves(moves$MoveScores[df$cleanEvents[i]])
    movesa <- c(movesa,black,white)
    
    
  }
  movesa
}
cumbettermoves <- function(allmoves)
{
  cum_sum <- numeric(length(allmoves))
  for (i in 1:length(allmoves))
  {
    cum_sum[i] <- 0
    if (i != length(allmoves))
    {
    for (j in (i+1):length(allmoves))
    {
      cum_sum[i] <- cum_sum[i] + allmoves[j]
    }
    }
  }
  cum_sum
}

prob_of_better_move <- function (moves, maxmoves)
{
  tw <- length(moves) * (length(moves) + 1)/2
  p_array <- numeric(0)
  if (length(moves) > 0)
  {
    p_array <- numeric(length(moves))
      for (i in 1:length(moves))
      {
        z  <- moves[i] + 12296
        if (z <= 0)
        {
          p_array[i] <- 1
        }
        else if (z > length(cumsum))
        {
          p_array[i] <- 0
        }
        else
        {
          p_array[i] <- (cumsum[z]/maxmoves) * i/tw
        }
        
      }
  }
  p_array
}
buildpTable <- function(df, moves, allmoves) {
  
  minElo <- 1001
  maxElo <- 3000
  intervals <- 100
  isize <- 20
  
  maxmoves <- length(allmoves)
  mean_of_p_moves <- numeric(intervals)
  sd_of_p_moves <- numeric(intervals)
  
  for (i in 1:intervals)
  { 
    lelo <- minElo + (i - 1) * isize
    helo <- minElo + i * isize
    ##helo <- lelo
    array_of_all_moves <- numeric()
    
    
    for (j in 1:length(df$cleanEvents))
    {
      singlegame <- moves$MoveScores[df$cleanEvents[j]]
      
      if (df$cleanWhiteElo[j] >= lelo & df$cleanWhiteElo[j] <= helo)
      {
        array_of_all_moves <- c(array_of_all_moves, getPowerOfWhiteMoves(singlegame))
      }
      if (df$cleanBlackElo[j] >= lelo & df$cleanBlackElo[j] <= helo)
      {
        array_of_all_moves <- c(array_of_all_moves, getPowerOfBlackMoves(singlegame))
      }
    }
    ##array_of_all_moves <- preprocessmoves(array_of_all_moves)
    
    if (length(array_of_all_moves) == 0)
    {
      mean_of_p_moves[i] <- 0
      
      sd_of_p_moves[i] <- 0
      
    }
    else
    {
      mean_of_p_moves[i] <- mean(prob_of_better_move(array_of_all_moves, maxmoves), na.rm=TRUE)
      sd_of_p_moves[i] <- sd(prob_of_better_move(array_of_all_moves,maxmoves), na.rm=TRUE)
    }
  }
  ta <- data.frame(mu=mean_of_p_moves,sigma=sd_of_p_moves)
  ta
  
}

probOfBetterMove <- function(pm)
{
  ##pm is power of move
  
  prob_of_zero <- 0.0587628
  prob_of_greater_than_zero <- 0.322546
  prob_of_less_than_zero <- 0.6186912
  
  prob_of_1_to_100 <- 0.9791509 * prob_of_greater_than_zero
  prob_of_101_to_150 <- 0.00492987 * prob_of_greater_than_zero
  prob_of_151_to_300 <- 0.005150656 * prob_of_greater_than_zero
  prob_of_301_to_infinity <- 0.01076859 * prob_of_greater_than_zero
  
  prob_of_n1_to_n100 <- 0.9158791 * prob_of_less_than_zero
  prob_of_n101_to_n150 <- 0.02987015 * prob_of_less_than_zero
  prob_of_n151_to_n300 <- 0.02774861 * prob_of_less_than_zero
  prob_of_n301_to_n550 <- 0.01272839 * prob_of_less_than_zero
  prob_of_n551_to_infinity <- 0.01377379 * prob_of_less_than_zero
  
  lambda_1_to_100 <- 1.0/11.6
  lambda_301_to_infinity <- 1.0/2480.0
  lambda_n1_to_n100 <- 1.0/21.0
  lambda_n551_to_infinity <- 1.0/2605.0
  
  slope_101_to_150 <- -1.077551
  ymax_101_to_150 <- 93.4
  ymin_101_to_150 <- 40.6
  
  slope_151_to_300 <- -0.1932886
  ymax_151_to_300 <- 42.8
  ymin_151_to_300 <- 14
  
  
  slope_n101_to_n150 <- -12.39184
  ymax_n101_to_n150 <- 1099.4
  ymin_n101_to_n150 <- 492.2
  
  slope_n151_to_n300 <- -2.379866
  ymax_n151_to_n300 <- 473.4
  ymin_n151_to_n300 <- 118.8
  
  slope_n301_to_n550 <- -0.4
  ymax_n301_to_n550 <- 122.8
  ymin_n301_to_n550 <- 23.2
  
  
  
  
  return_value <- 0.0
  
  if (pm == 0)
  {
     return_value <- 0.322546
  }
  else if (pm > 0)
  {
    if (pm <= 100)
    {
      if (pm == 100)
      {
        return_value <- prob_of_101_to_150 + prob_of_151_to_300 + prob_of_301_to_infinity
      }
      else
      {
        return_value <- (((pexp(pm, lambda_1_to_100, lower.tail = TRUE) - 
                           pexp(100, lambda_1_to_100, lower.tail = TRUE))/
                          pexp(100, lambda_1_to_100, lower.tail = TRUE)) *
                         prob_of_1_to_100) + 
          prob_of_101_to_150 + prob_of_151_to_300 + prob_of_301_to_infinity
      }
    } ## <= 100
    else if (pm <= 150)
    {
      if (pm == 150)
      {
        return_value <- prob_of_151_to_300 + prob_of_301_to_infinity
      }
      else
      {
        tarea <- ((150 - 101) * ymin_101_to_150) + 
                 (0.5 * (150 - 101) * (ymax_101_to_150 - ymin_101_to_150))
        barea <- ((150 - pm) * ymin_101_to_150)
                
      }
    }
  }
  
}
allmoves <- list()
tabmoves <- list()
cummoves <- list()
mean_p_moves <- list()
sd_p_moves <- list()

elos_moves <- list()

mb <- 0

cumulating <- function()
{
print("now cumulating")

maxindex <- as.integer(30/mb + 1)
for (i in 1:maxindex)
{
  print(i)
  cummoves[[i]] <<- numeric(length(tabmoves[[i]]))
  if (length(tabmoves[[i]]) > 0)
  for (j in 1:length(tabmoves[[i]]))
  {
    cummoves[[i]][j] <<- 0
    
    if (j == 1)
    {
      for (k in (j+1):length(tabmoves[[i]]))
      {
        cummoves[[i]][j] <<- cummoves[[i]][j] + tabmoves[[i]][k]
      }
    }
    else if (j < length(tabmoves[[i]]))
    {
       cummoves[[i]][j] <<- cummoves[[i]][j - 1] - tabmoves[[i]][j]
    }
  }
}
print("its done")
}

support_data <- function(df, moves, uElo,moves_per_block)
{
  mb <<- as.integer(moves_per_block)
  
  if (mb >= 15)
  {
    mb <<- 15
  }
  else if (mb >= 10)
  {
    mb <<- 10
  }
  else if (mb >= 6)
  {
    mb <- 6
  }
  else if (mb >= 5)
  {
    mb <<- 5
  }
  else if (mb >= 3)
  {
    mb <<- 3
  }
  else if (mb >= 2)
  {
    mb <<- 2
  }
  else
  {
    mb <<- 1
  }
  for (i in 1001:3000)
  {
    elos_moves[[i]] <<- list()
  }
  for (i in 1:31)
  {
    allmoves[[i]] <<- numeric(0)
    tabmoves[[i]] <<- numeric(0)
    cummoves[[i]] <<- numeric(0)
    for (j in 1001:3000)
    {
      elos_moves[[j]][[i]] <<- numeric(0)
    }
    mean_p_moves[[i]] <<- numeric(length(uElo))
    sd_p_moves[[i]] <<- numeric(length(uElo))
  }
  for ( i in 1 : length(df$cleanEvents)) 
  {
    print ("now its game")
    print (i)
    black <- getPowerOfBlackMoves(moves$MoveScores[df$cleanEvents[i]])
    if(length(black) > 0)
      for (j in 1: length(black))
      {
        if (j <= 30)
        {
          index <- ceiling(j/mb)
          allmoves[[index]] <<- c(allmoves[[index]], black[j])
          elos_moves[[df$cleanBlackElo[i]]][[index]] <<- 
            c(elos_moves[[df$cleanBlackElo[i]]][[index]], black[j])
        }
        else
        {
          index <- as.integer(30/mb + 1)
          allmoves[[index]] <<- c(allmoves[[index]], black[j])
          elos_moves[[df$cleanBlackElo[i]]][[index]] <<- 
            c(elos_moves[[df$cleanBlackElo[i]]][[index]], black[j])
        }
      }
    white <- getPowerOfWhiteMoves(moves$MoveScores[df$cleanEvents[i]])
    if (length(white) > 0)
      for (j in 1: length(white))
      {
        if (j <= 30)
        {
          index <- ceiling(j/mb)
          allmoves[[index]] <<- c(allmoves[[index]], white[j])
          elos_moves[[df$cleanWhiteElo[i]]][[index]] <<- 
            c(elos_moves[[df$cleanWhiteElo[i]]][[index]], white[j])
        }
        else
        {
          index <- as.integer(30/mb + 1)
          allmoves[[index]] <<- c(allmoves[[index]], white[j])
          elos_moves[[df$cleanWhiteElo[i]]][[index]] <<- 
            c(elos_moves[[df$cleanWhiteElo[i]]][[index]], white[j])
        }
      }
    
  }
  
  print("now tabulating")
  maxindex <- as.integer(30/mb + 1)
  
  for (i in 1:maxindex)
  {
    print("tab index")
    print(i)
    if (length(allmoves[[i]]) > 0)
    {
      min_move <- min(allmoves[[i]])
      if (min_move > 0)
      {
        tabmoves[[i]] <<- tabulate(allmoves[[i]])
      }
      else
      {
        tabmoves[[i]] <<- tabulate(allmoves[[i]] + 1 + abs(min_move))
      }
    }
  }
  
}
buildpTableuElo <- function(df, moves, uElo,moves_per_block) {
  
  maxindex <- as.integer(30/mb + 1)
  for (i in 1:length(uElo))
  { 
    for (j in 1:maxindex)
    {
     ## mean_p_moves[[j]][i] <<- mean(prob_of_bm(elos_moves[[uElo[i]]][[j]], j), na.rm=TRUE)
      ##sd_p_moves[[j]][i] <<- sd(prob_of_bm(elos_moves[[uElo[i]]][[j]], j), na.rm=TRUE)
      
      
      mean_p_moves[[j]][i] <<- mean(prob_of_bm(preprocessmoves(elos_moves[[uElo[i]]][[j]]), j), na.rm=TRUE)
      sd_p_moves[[j]][i] <<- sd(prob_of_bm(preprocessmoves(elos_moves[[uElo[i]]][[j]]), j), na.rm=TRUE)
    }
  }
    
   
  ##ta <- data.frame(mu=mean_of_p_moves,sigma=sd_of_p_moves,elo=uElo)
  ##ta
  
}

prob_of_bm <- function(moves, index)
{
  result <- numeric(length(moves))
  
  if (length(moves) > 0)
  {
    tw <- sum(tabmoves[[index]])
    minm <- min(allmoves[[index]])
    add_to_move <- 0
    if (minm <= 0)
    {
      add_to_move <- abs(minm) + 1
    }
      
    for (i in 1:length(moves))
    {
      cmove <- moves[i] + add_to_move
      if (cmove >= length(cummoves[[index]]))
      {
        result[i] <- 0
      }
      else if (cmove > 0)
      {
        result[i] <- cummoves[[index]][cmove] / tw
      }
      else
      {
          result[i] <- 1
      }
    }
  }
  result
}
