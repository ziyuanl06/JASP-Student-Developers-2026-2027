library(dplyr)

d <- read.csv(file.choose(), check.names = FALSE)

#1
nrow(d)

#2
colnames(d)

#3
d[4, "Age"]

#4
mean(d$Age, na.rm = TRUE)

#5
max(d$Age)

#6
sum(d$Age > 100)

#7
d[d$Age == 999, "ID"]

#8
d[d$Age == 999, "Age"] <- NA
mean(d$Age, na.rm = TRUE)

#9
vec_na <- c()
for (col in colnames(d)){
  vec_na <- c(vec_na, sum(is.na(d[col])))
}

#10
lvl_gender <- d$gender
lvl_lower <- tolower(lvl_gender)
lvl_nospace <- gsub(" ", "", lvl_lower)
lvl_name <- levels(as.factor(lvl_nospace))

#11
anx_cols <- grep("anx", names(d), ignore.case = TRUE)

#12
mean_anx <- sapply(d[, anx_cols], mean, na.rm = TRUE)
max_anx_item <- names(mean_anx)[which.max(mean_anx)]

#13
anx_1 <- d[, c("wave", "anxiety_1")]
anx_new <- anx_1 %>%
  group_by(wave) %>%
  summarise(mean_anxiety = mean(anxiety_1, na.rm = TRUE))

#14
sleep <- d$sleep_hrs
sleep_cleaned <- gsub(",", ".", sleep)
mean_sleep <- mean(as.numeric(sleep_cleaned), na.rm = TRUE)

#15
mean_anx <- round(sapply(d[, anx_cols], mean, na.rm = TRUE), 2)
sd_anx <- round(sapply(d[, anx_cols], sd, na.rm = TRUE), 2)
df_anx <- data.frame(variable = names(mean_anx),
                     mean = mean_anx,
                     sd = sd_anx)

#16
pct_missing <- function(x){
  return(mean(is.na(x)) * 100)
}
pct_missing(d$anx.6)


#17
anx_cols_names <- names(d)[anx_cols]

missing_table <- function(df, vars){
  variable <- c()
  n_missing <- c()
  pct_miss <- c()
  for (var in vars){
    dat_vec <- df[, var]
    n_missing <- c(n_missing, sum(is.na(dat_vec)))
    pct_miss <- c(pct_miss, pct_missing(dat_vec))
  }
  return(data.frame(variable = vars,
                    n_missing = n_missing,
                    pct_miss = pct_miss))
}

sum(missing_table(d, anx_cols_names)$n_missing)


#18
missing_table <- function(df, vars, codes = c(999, -99), digits = 1){
  variable <- c()
  n_missing <- c()
  pct_miss <- c()
  for (var in vars){
    dat_vec <- df[, var]
    
    dat_vec[dat_vec %in% codes] <- NA
    
    n_missing <- c(n_missing, sum(is.na(dat_vec)))
    pct_miss <- c(pct_miss, round(pct_missing(dat_vec), digits))
  }
  return(data.frame(variable = vars,
                    n_missing = n_missing,
                    pct_miss = pct_miss))
}

sum(missing_table(d, anx_cols_names)$n_missing)


#19
missing_table <- function(df, vars, codes = c(999, -99), digits = 1){
  variable <- c()
  n_missing <- c()
  pct_miss <- c()
  unknown <- setdiff(vars, names(df))
  if (length(unknown) > 0){
    stop("These columns don't exist: ", paste(unknown, collapse = ", "))
  }
  for (var in vars){
    dat_vec <- df[, var]
    
    dat_vec[dat_vec %in% codes] <- NA
    
    n_missing <- c(n_missing, sum(is.na(dat_vec)))
    pct_miss <- c(pct_miss, round(pct_missing(dat_vec), digits))
  }
  return(data.frame(variable = vars,
                    n_missing = n_missing,
                    pct_miss = pct_miss))
}
sum(missing_table(d, anx_cols_names)$n_missing)

#20
describe <- function(df, vars, split_by = NULL) {
  if (!is.null(split_by)) {
    df <- df %>%
      group_by(across(all_of(split_by)))
  }
  
  results <- list()
  
  for (var in vars) {
    df_sum <- df %>%
      summarise(
        variable = var,
        n = sum(!is.na(.data[[var]])),
        mean = mean(.data[[var]], na.rm = TRUE),
        sd = sd(.data[[var]], na.rm = TRUE),
        .groups = "drop"
      )
    
    results[[var]] <- df_sum
  }
  
  return(bind_rows(results))
}

describe(d, c("anxiety_1", "stroop_RT_ms"), split_by = "wave")


