### INFO
# project: Project #: Prostate cancer prevalence
# author: Agz Leman
# 17th January 2023
# Plots monthly rates 
###
## library
library(tidyverse)
library(here)
library(MASS)
library(plyr)

start <- "2020-03-01"

for (i in c(
  "measure_self_harmAE_rate.csv",
  "measure_self_harmHo_rate.csv",
  "measure_self_harmDe_rate.csv",
  "measure_emot_distAE_rate.csv",
  "measure_emot_distHo_rate.csv",
  "measure_emot_distDe_rate.csv",
  "measure_eat_disorAE_rate.csv",
  "measure_eat_disorHo_rate.csv",
  "measure_eat_disorDe_rate.csv",
  # "measure_lifestyleAE_rate.csv",
  "measure_lifestyleHo_rate.csv",
  "measure_lifestyleDe_rate.csv",
  # "measure_violence_AE_rate.csv",
  "measure_violence_Ho_rate.csv",
  "measure_violence_De_rate.csv"
)){

  Rates <- read_csv(here::here("output", "measures", i))
  Rates_rounded <- as.data.frame(Rates)
  
  ###
  # Redact and round counts 
  ###
  Rates_rounded[,1] <- redactor(Rates_rounded[,1])
  for (j in 1:2){
    Rates_rounded[,j] <- plyr::round_any(Rates_rounded[,j], 5, f = round)}
  
  Rates_rounded$value <- Rates_rounded[,1]/Rates_rounded$population
  # calc rate per 100,000
  Rates_rounded$value2 <- Rates_rounded$value*100000
  write.table(Rates_rounded, here::here("output", paste0(substr(i, 9, 19),"_rounded",".csv")),
              sep = ",",row.names = FALSE)
  ###### cut date that is after November 
  
  ###
  # Plot 
  ###
  p <- ggplot(data = Rates_rounded,aes(date, value2)) +
    geom_line()+
    geom_point()+
    scale_x_date(date_breaks = "2 month",
                 date_labels = "%Y-%m")+
    labs(title = paste0(colnames(Rates_rounded)[1]), 
         x = "", y = "Rate per 100,000")+
    theme_bw()+
    theme(axis.text.x = element_text(angle = 45, hjust = 1))
  p <- p + geom_vline(xintercept=as.Date(start, format="%Y-%m-%d"), size=0.3, colour="red")
  p <- p +  geom_text(aes(x=as.Date(start, format="%Y-%m-%d")+5, y=min(value2)+(sd(value2)*2)), 
                      color = "red",label="Start of\nrestrictions", angle = 90, size = 3)
  p <- p + labs(caption="OpenSafely-TPP June 2023")
  p <- p + theme(plot.caption = element_text(size=8))
  p <- p + theme(plot.title = element_text(size = 10))
  
  ggsave(
    plot= p, dpi=800,width = 20,height = 10, units = "cm",
    filename=paste0(substr(i, 9, 19),".png"), path=here::here("output"),
  )
}

for (i in c(
  "measure_self_harmAEbyRegion_rate.csv",
  "measure_self_harmAEbyIMD_rate.csv",
  "measure_self_harmAEbyEthnicity_rate.csv",
  "measure_self_harmAEbyAge_rate.csv",
  "measure_self_harmHobyRegion_rate.csv",
  "measure_self_harmHobyIMD_rate.csv",
  "measure_self_harmHobyEthnicity_rate.csv",
  "measure_self_harmHobyAge_rate.csv",
  "measure_self_harmDebyRegion_rate.csv",
  "measure_self_harmDebyIMD_rate.csv",
  "measure_self_harmDebyEthnicity_rate.csv",
  "measure_self_harmDebyAge_rate.csv",
  "measure_emot_distAEbyRegion_rate.csv",
  "measure_emot_distAEbyIMD_rate.csv",
  "measure_emot_distAEbyEthnicity_rate.csv",
  "measure_emot_distAEbyAge_rate.csv",
  "measure_emot_distHobyRegion_rate.csv",
  "measure_emot_distHobyIMD_rate.csv",
  "measure_emot_distHobyEthnicity_rate.csv",
  "measure_emot_distHobyAge_rate.csv",
  "measure_emot_distDebyRegion_rate.csv",
  "measure_emot_distDebyIMD_rate.csv",
  "measure_emot_distDebyEthnicity_rate.csv",
  "measure_emot_distDebyAge_rate.csv",
  "measure_eat_disorAEbyRegion_rate.csv",
  "measure_eat_disorAEbyIMD_rate.csv",
  "measure_eat_disorAEbyEthnicity_rate.csv",
  "measure_eat_disorAEbyAge_rate.csv",
  "measure_eat_disorHobyRegion_rate.csv",
  "measure_eat_disorHobyIMD_rate.csv",
  "measure_eat_disorHobyEthnicity_rate.csv",
  "measure_eat_disorHobyAge_rate.csv",
  "measure_eat_disorDebyRegion_rate.csv",
  "measure_eat_disorDebyIMD_rate.csv",
  "measure_eat_disorDebyEthnicity_rate.csv",
  "measure_eat_disorDebyAge_rate.csv",
  # "measure_lifestyleAEbyRegion_rate.csv",
  # "measure_lifestyleAEbyIMD_rate.csv",
  # "measure_lifestyleAEbyEthnicity_rate.csv",
  # "measure_lifestyleAEbyAge_rate.csv",
  "measure_lifestyleHobyRegion_rate.csv",
  "measure_lifestyleHobyIMD_rate.csv",
  "measure_lifestyleHobyEthnicity_rate.csv",
  "measure_lifestyleHobyAge_rate.csv",
  "measure_lifestyleDebyRegion_rate.csv",
  "measure_lifestyleDebyIMD_rate.csv",
  "measure_lifestyleDebyEthnicity_rate.csv",
  "measure_lifestyleDebyAge_rate.csv",
  # "measure_violence_AEbyRegion_rate.csv",
  # "measure_violence_AEbyIMD_rate.csv",
  # "measure_violence_AEbyEthnicity_rate.csv",
  # "measure_violence_AEbyAge_rate.csv",
  "measure_violence_HobyRegion_rate.csv",
  "measure_violence_HobyIMD_rate.csv",
  "measure_violence_HobyEthnicity_rate.csv",
  "measure_violence_HobyAge_rate.csv",
  "measure_violence_DebyRegion_rate.csv",
  "measure_violence_DebyIMD_rate.csv",
  "measure_violence_DebyEthnicity_rate.csv",
  "measure_violence_DebyAge_rate.csv"
  )){
  
  Rates <- read_csv(here::here("output", "measures", i))
  Rates_rounded <- as.data.frame(Rates)
  
  ###
  # Redact and round counts 
  ###
  Rates_rounded[which(is.na(Rates_rounded[,2])),2] <- 1
  Rates_rounded[,2] <- redactor(Rates_rounded[,2])
  for (j in 2:3){
    Rates_rounded[,j] <- plyr::round_any(Rates_rounded[,j], 5, f = round)}
  
  Rates_rounded$value <- Rates_rounded[,2]/Rates_rounded$population
  # calc rate per 100,000
  Rates_rounded$value2 <- Rates_rounded$value*100000
  write.table(Rates_rounded, here::here("output",paste0(substr(i, 9, 24),"_rounded",".csv")),
              sep = ",",row.names = FALSE)
  
  
  p <- ggplot(data = Rates_rounded,aes(date, value2, color = Rates_rounded[,1], lty = Rates_rounded[,1])) +
    geom_line()+
    #geom_point(color = "region")+
    scale_x_date(date_breaks = "2 month",
                 date_labels = "%Y-%m")+
    labs(title = paste0(substr(i, 9, 19)," by ",colnames(Rates_rounded)[1]), 
         x = "", y = "Rate per 100,000")+
    theme_bw()+
    theme(axis.text.x = element_text(angle = 45, hjust = 1), 
          legend.position="bottom",
          legend.title=element_blank())
  
  p <- p + geom_vline(xintercept=as.Date(start, format="%Y-%m-%d"), size=0.3, colour="red")
  p <- p +  geom_text(aes(x=as.Date(start, format="%Y-%m-%d")+5, y=min(value2)+(sd(value2)*2)), 
                      color = "red",label="Start of\nrestrictions", angle = 90, size = 3)
  p <- p + labs(caption="OpenSafely-TPP June 2023")
  p <- p + theme(plot.caption = element_text(size=8))
  p <- p + theme(plot.title = element_text(size = 10))
  
  ggsave(
    plot= p, dpi=800,width = 20,height = 10, units = "cm",
    filename=paste0(substr(i, 9, 24),".png"), path=here::here("output"),
  )
}

# ###
# # Summarise population data from the input.csv
# ###

# #Input <- read_csv(here::here("output", "input.csv"),show_col_types = FALSE)
# Input <- read_csv(here::here("output", "input.csv"),col_types = cols(patient_id = col_integer()))

# Table1 <- as.data.frame(NA)
# xx <- c("total_number","average_age","sd_age","ADTsecond_gener","HCD", "HCDexpanded")
# Table1[xx] <- NA
# Table1[1,"total_number"] <- plyr::round_any(length(which(Input$prostate_ca==1)), 5, f = round)
# Input2 <- Input[Input$prostate_ca==1,]
# Table1[1,"HCD"] <- plyr::round_any(length(which(Input2$HCD==1)), 5, f = round)
# Table1[1,"HCDexpanded"] <- plyr::round_any(length(which(Input2$HCDexpanded==1)), 5, f = round)
# Table1[1,"ADTsecond_gener"] <- plyr::round_any(length(which(Input2$ADTsecond_gener==1)), 5, f = round)

# Table1[1,"average_age"] <- mean(Input2$age_pa_ca)
# Table1[1,"sd_age"] <- sd(Input2$age_pa_ca)
# Table1[names(table(Input2$age_group))] <- NA
# Table1[1,names(table(Input2$age_group))] <- plyr::round_any(as.numeric(table(Input2$age_group)), 5, f = round)
# Table1[names(table(Input2$ethnicity))] <- NA
# Table1[1,names(table(Input2$ethnicity))] <- plyr::round_any(as.numeric(table(Input2$ethnicity)), 5, f = round)
# Table1[names(table(Input2$sex))] <- NA
# Table1[1,names(table(Input2$sex))] <- plyr::round_any(as.numeric(table(Input2$sex)), 5, f = round)

# write.table(Table1, here::here("output", "Table1.csv"),sep = ",",row.names = FALSE)
