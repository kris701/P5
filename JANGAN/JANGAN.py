from ProjectTools import ConfigHelper as cfg

import CGAN as cg
import DataGenerator as dg

print(" --- Generating dataset if not there --- ")

datagen = dg.DataGenerator()
datagen.ConfigureFileImporter(
    cfg.GetStringValue("DATAGENERATOR","TextPath"),
    cfg.GetStringValue("DATAGENERATOR","LetterDownloadURL"),
    cfg.GetJsonValue("DATAGENERATOR","TextDownloadURLS"),
    cfg.GetStringValue("DATAGENERATOR","TempDownloadLetterPath"),
    cfg.GetStringValue("DATAGENERATOR", "TempDownloadLetterFileName"))
datagen.ConfigureTextSequence(
    cfg.GetStringValue("DATAGENERATOR", "TextPath"))
datagen.ConfigureDataExtractor(
    cfg.GetStringValue("DATAGENERATOR", "OutputLettersPath"),
    cfg.GetStringValue("DATAGENERATOR", "TempDownloadLetterPath"),
    cfg.GetStringValue("DATAGENERATOR", "TempDownloadLetterFileName"),
    cfg.GetIntValue("DATAGENERATOR", "MinimumLetterCount"),
    cfg.GetIntValue("DATAGENERATOR", "MaximumLetterCount"),
    cfg.GetStringValue("DATAGENERATOR", "OutputLetterFormat"),
    cfg.GetIntValue("DATAGENERATOR", "IncludeNumbers"),
    cfg.GetIntValue("DATAGENERATOR", "IncludeLetters"))
    

datagen.GenerateData()

print(" --- Done! --- ")
print("")
print(" --- Training CGAN --- ")

cgan = cg.CGAN(
    cfg.GetIntValue("CGAN", "BatchSize"),
    1,
    cfg.GetIntValue("CGAN", "NumberOfClasses"),
    cfg.GetIntValue("CGAN", "ImageSize"),
    cfg.GetIntValue("CGAN", "LatentDimension"),
    cfg.GetIntValue("CGAN", "EpochCount"),
    cfg.GetIntValue("CGAN", "RefreshUIEachXIteration"),
    cfg.GetIntValue("CGAN", "NumberOfFakeImagesToOutput"),
    cfg.GetStringValue("CGAN", "TrainDatasetDir"),
    cfg.GetStringValue("CGAN", "TestDatasetDir"))

cgan.SetupCGAN()
cgan.LoadDataset()
cgan.TrainGAN()
cgan.ProduceLetters()

print(" --- Done! --- ")