library(tidyr)
library(dplyr)
library(ggplot2)

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
#Calculate volume differences between each pair of methods
dane$`Δ(Vv-Va)` <- dane$VevoLab - dane$Algorytm
dane$`Δ(Vs-Va)` <- dane$Suwmiarka - dane$Algorytm
dane$`Δ(Vv-Vs)` <- dane$VevoLab - dane$Suwmiarka

#Convert to long format data (ggplot2)
dane_long <- dane %>%
  select(Mysz, `Δ(Vv-Va)`, `Δ(Vs-Va)`, `Δ(Vv-Vs)`) %>%
  pivot_longer(cols = -Mysz, names_to = "Różnica", values_to = "Wartość")

#Create bar plot showing pairwise differences between methods
ggplot(dane_long, aes(x = Różnica, y = Wartość, fill = Mysz)) +
  geom_bar(stat = "identity", position = position_dodge(width = 0.52), width = 0.5) +
  geom_hline(yintercept = 0, linetype = "dashed", color = "gray40") +
  geom_text(
    aes(label = round(Wartość, 1)),
    position = position_dodge(width = 0.52),
    vjust = ifelse(dane_long$Wartość >= 0, -0.3, 1.2),
    size = 3.5
  )+
  labs(
    title ="Odchylenie różnicowe między parami metod pomiaru objętości dla 
    płaszczyzny koronalnej",                      #title = "Differential deviation between volume measurement methods(coronal) plane"
    y = "Różnica objętości [mm³]",                # y = "Volume difference "[mm³]"
    x = "Różnica"                                 # x = "Difference"
  ) +
  scale_y_continuous(breaks = seq(-10, 20, by = 5), limits = c(-10, 20))+
  theme_classic() +
  theme(
    axis.text.x = element_text(angle = 15, size=11,hjust = 1, color="black", face="bold"),
    legend.position = "right",
    legend.text = element_text(face="bold"),
    legend.title = element_blank(),
    axis.text.y = element_text(color="black"),
    plot.title = element_text(size=15)
  )

