install.packages("plotrix")
setwd("//Users/macbook/workspace/20211/introToDS/DataScience_AQI_explorer/data")
library(ggplot2)
library(RColorBrewer)
library(plotly)
library(plyr)
library(plotrix)
aqi_data <- read.csv("Merged_All.csv")
aqi_data$Area <- as.numeric(as.character(aqi_data$Area))
#sapply(aqi_data, class)

scl = list( c(0, "rgb(0, 255, 0)"),  # green
            c(0.2, "rgb((255, 255, 0)"), # yellow
            c(0.4, "rgb(255, 127, 0)"), # orange
            c(0.6, "rgb(255, 0, 0)"), # red
            c(0.8, "rgb(120, 43, 125,)"), # purple
            c(1, "rgb(103, 0, 27)")) # maroon


# Country GDP Per Capita and City AQI Index relationship:
########################### 2D
nonNa <- aqi_data[!is.na(aqi_data$AQI_Avg),]
nonNa <- nonNa[!is.na(nonNa$AQI_Max),]
nonNa <- nonNa[!is.na(nonNa$AQI_Min),]
range(nonNa$AQI_Max)
range(nonNa$AQI_Min)
range(nonNa$AQI_Avg)
r_range <- c(0, 50, 100, 150, 200, 250, 10000)
label <- c("Good", "Moderate","Unhealthy for Sensitive Groups", "Unhealthy", "Very Unhealthy", "Hazardous")
colors <- c("#00FF00", "#FFFF00", "#FF8800", "#FF0000", "#782B7D", "#67011B")
nonNa$groups <- cut(nonNa$AQI_Min,               # Add group column
                    breaks = r_range)
ggplot(nonNa, aes(x=GDP_Per_Capita, y=AQI_Min, color=groups)) + 
  geom_point(size=2) + 
  scale_color_manual(breaks = levels(nonNa$groups), values = colors, labels = label)

nonNa$groups <- cut(nonNa$AQI_Avg,               # Add group column
                    breaks = r_range)
ggplot(nonNa, aes(x=GDP_Per_Capita, y=AQI_Avg, color=groups)) + 
  geom_point(size=2) + 
  scale_color_manual(breaks = levels(nonNa$groups), values = colors, labels = label)

nonNa$groups <- cut(nonNa$AQI_Max,               # Add group column
                    breaks = r_range)
ggplot(nonNa, aes(x=GDP_Per_Capita, y=AQI_Max, color=groups)) + 
  geom_point(size=2) + 
  scale_color_manual(breaks = levels(nonNa$groups), values = colors, labels = label)


########################### 3D 

nonNa <- aqi_data[!is.na(aqi_data$AQI_Max),]
nonNa <- nonNa[!is.na(nonNa$AQI_Avg),]
nonNa <- nonNa[!is.na(nonNa$AQI_Min),]
nonNa <- nonNa[!is.na(nonNa$GDP_Per_Capita),]
nonNa <- nonNa[!is.na(nonNa$GDP),]
nonNa <- nonNa[!is.na(nonNa$Growth),]

scl = list( c(0, "rgb(0, 255, 0)"),  # green
            c(0.2, "rgb((255, 255, 0)"), # yellow
            c(0.4, "rgb(255, 127, 0)"), # orange
            c(0.6, "rgb(255, 0, 0)"), # red
            c(0.8, "rgb(120, 43, 125,)"), # purple
            c(1, "rgb(103, 0, 27)")) # maroon
#max(nonNa$AQI_Min) / 500 # => "rgb(255, 200, 0)"
#max(nonNa$AQI_Min) / 500
#min(nonNa$AQI_Min) / 500 # => "rgb(5, 255, 0)"
scl_Min = list(c(0, "rgb(5, 255, 0)"), 
               c(0.2/0.268, "rgb((255, 255, 0)"), 
               c(1, "rgb(255, 200, 0)"))
fig <- plot_ly(nonNa, x = ~GDP_Per_Capita, y = ~Growth, z = ~GDP, marker = list(color=~AQI_Min, colorscale=scl_Min, type = "heatmap", showscale = TRUE))#, color = ~am, colors = c('#BF382A', '#0C4B8E'))
fig <- fig %>% add_markers()
fig <- fig %>% layout(scene = list(xaxis = list(title = 'GDP_Per_Capita'),
                                   yaxis = list(title = 'Growth'),
                                   zaxis = list(title = 'GDP')))
fig

#max(nonNa$AQI_Max) / 500 # => "rgb(103, 0, 27)" = 1
#min(nonNa$AQI_Max) / 500 # => "rgb(127, 255, 0)" = 0.1
scl_Max = list(c(0,"rgb(127, 255, 0)"), 
               c((0.2-0.1)/0.9,"rgb((255, 255, 0)"), 
               c((0.4-0.1)/0.9,"rgb(255, 127, 0)"), 
               c((0.6-0.1)/0.9,"rgb(255, 0, 0)"), 
               c((0.8-0.1)/0.9,"rgb(120, 43, 125,)"), 
               c((1-0.1)/0.9,"rgb(103, 0, 27)" ))
fig <- plot_ly(nonNa, x = ~GDP_Per_Capita, y = ~Growth, z = ~GDP, marker = list(color=~AQI_Max, colorscale=scl_Max, type = "heatmap", showscale = TRUE))#, color = ~am, colors = c('#BF382A', '#0C4B8E'))
fig <- fig %>% add_markers()
fig <- fig %>% layout(scene = list(xaxis = list(title = 'GDP_Per_Capita'),
                                   yaxis = list(title = 'Growth'),
                                   zaxis = list(title = 'GDP')))
fig

#max(nonNa$AQI_Avg)# / 500 # => "rgb(255, 115, 0)" 0.411759
#min(nonNa$AQI_Avg)# / 500 # => "rgb(64, 255, 0)" 0.05661146 

scl_Avg = list(c((0.05661146 - 0.05661146)/(0.411759 - 0.05661146), "rgb(64, 255, 0)"), 
               c((0.2 - 0.05661146)/(0.411759 - 0.05661146), "rgb((255, 255, 0)"), 
               c((0.4 - 0.05661146)/(0.411759 - 0.05661146), "rgb(255, 127, 0)"), 
               c((0.411759 - 0.05661146)/(0.411759 - 0.05661146), "rgb(255, 115, 0)"))


fig <- plot_ly(nonNa, x = ~GDP_Per_Capita, y = ~Growth, z = ~GDP, marker = list(color=~AQI_Avg, colorscale=scl_Avg, type = "heatmap", showscale = TRUE))#, color = ~am, colors = c('#BF382A', '#0C4B8E'))
fig <- fig %>% add_markers()
fig <- fig %>% layout(scene = list(xaxis = list(title = 'GDP_Per_Capita'),
                                   yaxis = list(title = 'Growth'),
                                   zaxis = list(title = 'GDP')))
fig


########################### AQI TIMELY

aqi_time <- read.csv("aqi_all.csv")

# stable: Sydney, Stockholm
# vary by time: Delhi, Hanoi
stockholm <- filter(aqi_time, city=="Stockholm")
cc <- stockholm["AQI"][,]
ci <- 0:(length(cc)-1)
plot(ci, cc, type="l")

hanoi <- filter(aqi_time, city=="Hanoi")
cc <- hanoi["AQI"][,]
ci <- 0:(length(cc)-1)
plot(ci, cc, type="l")



########################################################################


# dominant:
domi_nonna <- aqi_data[!is.na(aqi_data$dominant_pollutant),]
# domi_nonna <- aqi_time[!is.na(aqi_data$dominant_pollutant),]
#group <- as.factor(aqi_data$dominant_pollutant)

tb = table(domi_nonna$dominant_pollutant)
df = as.data.frame(tb)
freq = c(df['Freq'][,][2:5])
var = c(df['Var1'][,][2:5])

#var <- mapvalues(var,from=c(""), to=("NA"))
pie(freq, var, col=rainbow(length(x))) 
legend("topright", as.character(var), cex = 0.3, fill = rainbow(length(x)))

pie3D(c(freq),labels = c(freq), explode = 0.1)
legend("topright", c("O3", "PM10", "PM2.5", "SO2"), cex = 0.4, fill = rainbow(4))


########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
########################################################################
########################################################################



