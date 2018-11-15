# Libraries
library("forecast")


#Load DataSet
Dataset <- read.table("data_analysis.csv", header=TRUE, sep=",", na.strings="NA", dec=".", strip.white=TRUE)
Dataset <- subset(Dataset, PUERTO == "Valparaíso")
Dataset <- aggregate(TONELADAS ~ AÑO , data=Dataset, FUN=sum)

#Offset data
Dataset_1 <- Dataset
names(Dataset_1)[c(2)] <- c("TONELADAS_1")
Dataset_1$AÑO <- with(Dataset_1, AÑO+1)
Dataset_2 <- Dataset
names(Dataset_2)[c(2)] <- c("TONELADAS_2")
Dataset_2$AÑO <- with(Dataset_2, AÑO+2)
Dataset_3 <- Dataset
names(Dataset_3)[c(2)] <- c("TONELADAS_3")
Dataset_3$AÑO <- with(Dataset_3, AÑO+3)
Dataset <- merge(x = Dataset, y = Dataset_1, all.x=TRUE, by="AÑO")
Dataset <- merge(x = Dataset, y = Dataset_2, all.x=TRUE, by="AÑO")
Dataset <- merge(x = Dataset, y = Dataset_3, all.x=TRUE, by="AÑO")

#Pearson correlation
cor(Dataset[,c("TONELADAS","TONELADAS_1","TONELADAS_2","TONELADAS_3")], use="complete")

#Create predictive model
tsData <- ts(Dataset$TONELADAS, frequency = 1)
plot.ts(tsData)
tsModel <-auto.arima(tsData)
summary(tsModel)

#Forecast
tsForecast <- forecast(tsModel, 5)
plot(tsForecast )

#Check residuals
plot.ts(tsForecast$residuals)
qqnorm(tsForecast$residuals)
qqline(tsForecast$residuals)
acf(tsForecast$residuals)
plot(density(tsForecast$residuals), main= "Residual Density Plot")