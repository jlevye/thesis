setwd("~/Documents/School/GradSchool/Thesis/Dimensions")
monoculture <- read.csv("MonocultureBigBio.csv")
names(monoculture)
newnames <- c("Date","SiteID","Species","PlantID","LeafID","Thick1","Thick2","Thick3","ThickMean","ThickSD","File","AreaPx","Area","DryMass","SLA")
names(monoculture) <- newnames

species <- unique(monoculture$Species)
class <- c("Legume","C4","Forb","Forb","Legume","C4","Forb","C3","Legume","Legume","Forb")
spClass <- data.frame(Species = species, Type = class)
monoculture <- merge(monoculture, spClass, by = "Species")

theme <- list(theme(axis.title = element_text(size = 20), axis.text = element_text(size=18), legend.title = element_text(size=20), legend.text = element_text(size=18)))

SLA <- ggplot(monoculture, aes(x = Species, y = SLA, fill = Type)) + geom_boxplot() + labs(y = bquote("SLA ("*~cm^2~g^-1*")")) + theme
Thick <- ggplot(monoculture, aes(x = Species, y = ThickMean, fill = Type)) + geom_boxplot() + labs(y = "Leaf Thickness (mm)") + theme


ggsave("../sla.png",SLA)
ggsave("../thick.png", Thick)
