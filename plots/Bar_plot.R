library(ggplot2)
library(tidyr)
library(dplyr)

#Create the data frame
dane <- data.frame(
  Mysz = paste0("Mysz ", 1:5),
  #Suwmiarka = c(31.566, 92.317, 149.855, 99.623, 105.794), #axial
  #VevoLab = c(24.049, 109.653, 142.699, 99.968, 105.322),  #axial
  #Algorytm = c(24.54, 98.59, 142.16, 109.01, 109.98)       #axial
  Suwmiarka = c(31.566, 92.317, 149.855, 99.623, 105.794),  #coronal
  VevoLab = c(26.462, 89.453, 141.057, 99.256, 105.748),    #coronal
  Algorytm = c(27.37, 96.28, 144.89, 103.28, 103.78)        #coronal
)

#Convert to long format data (ggplot2)
dane_long <- dane %>%
  pivot_longer(cols = -Mysz, names_to = "Metoda", values_to = "Objętość")
dane_long$Metoda <- factor(dane_long$Metoda, levels = c("Suwmiarka", "VevoLab", "Algorytm"))

#Create grouped bar plot
ggplot(dane_long, aes(x = Mysz, y = Objętość, fill = Metoda)) +
  geom_bar(stat = "identity", position = position_dodge(width = 0.9), width = 0.7) +
  labs(
    title = "Porównanie pomiarów objętości dla płaszczyzny koronalnej", #title = "Comparison of volume measurements in the (coronal) plane"
    y = "Objętość [mm³]",     # y = "Volume [mm³]"
    x= "Model zwierzęcy"      # x = "Animal model"
  ) +
  scale_y_continuous(breaks = seq(0, 150, by = 25), limits = c(0, 150))+
  theme_classic() +
  theme(
    axis.text = element_text(size = 11, color = "black"),
    axis.title = element_text(size = 11),
    plot.title = element_text(size=15,hjust=0.5),
    legend.title = element_blank(),
    legend.text = element_text(face = "bold")
  )
