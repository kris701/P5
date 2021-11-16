from ProjectTools import AutoPackageInstaller as ap

ap.CheckAndInstall("tensorflow")
ap.CheckAndInstall("pathlib")
ap.CheckAndInstall("tensorflow")
ap.CheckAndInstall("multipledispatch")
ap.CheckAndInstall("tensorflow")

import os
from pathlib import Path
import numpy
import tensorflow
from tensorflow.keras.callbacks import ModelCheckpoint
from multipledispatch import dispatch
from tensorflow.keras import Model
from Classifier import FitData
from Classifier import LayerConfigObject
from Classifier import CompilerConfigObject
from Classifier import LetterModel
from Classifier import DataLoader
from tensorflow.keras.models import load_model


class Classifier():
    def __init__(self, epochs, retrain, modelname, model_path):
        self.save_dir =  Path(model_path)
        self.model: Model

        #Metrics
        self.fit_history: tensorflow.keras.callbacks.History
        self.accuracy = []
        self.loss = []

        #Training variables
        self.epochs = epochs
        self.retrain = retrain
        self.modelname = modelname

    def TrainClassifier(self, data_path: str):
        #Sets up the model for training
        self.model = self.__CreateModel(LayerConfigObject.LayerConfigObject(), CompilerConfigObject.CompilerConfigObject())
        
        #Mount data from GAN
        dataLoader = DataLoader.DataLoader()
        data = dataLoader.LoadFittingData(data_path)
        
        #Train the model with the mounted data
        self.model = self.__TrainModelCallback_(self.model, data, self.epochs, self.retrain, self.modelname)
        return self.model

    def __EvaluateOnRealData(self, data_path: str, validation_split = 0.2, subset = "validaton", seed = 123):
        dataLoader = DataLoader.DataLoader()
        data = dataLoader.LoadDataSet(data_path, validation_split, subset, seed)
        score = self.model.evaluate(x = data, verbose = 1)
        self.loss = score[0]
        self.accuracy = score[1]

    def ProduceStatistics(self, input_path: str, validation_split = 0.2, subset = "validation", seed = 123):
        self.__EvaluateOnRealData(input_path, validation_split, subset, seed)
        return self.accuracy
    
    def __CreateModel(self, layers: LayerConfigObject.LayerConfigObject, compile_config: CompilerConfigObject.CompilerConfigObject):
        model = LetterModel.LetterModel(layers)
        model.compile(compile_config)
        return model.sequential

    def __TestModel(self, model: Model, test_data: tensorflow.data.Dataset):
        return model.evaluate(test_data)

    def __TrainModelCallback_(self, model: Model, fd: FitData.FitData, epochs: int, retrain = False, model_name = "my_model"):
        cm = model
        save_path = self.save_dir / (model_name + '.h5')
        self.save_dir.mkdir(parents = True, exist_ok = True)

        if(retrain):
            self.fit_history = cm.fit(fd.GetTrainData(), epochs=epochs)
            cm.save(save_path)
            return cm

        if(not (save_path.exists())):
            self.fit_history = cm.fit(fd.GetTrainData(), epochs=epochs)
            cm.save(save_path)
            return cm

        else:
            cm = load_model(save_path)
            return cm

    def __PredictData(self, model: Model, data: tensorflow.data.Dataset):
        try: 
            return model.predict(data)
        except:
            print("Exception thrown. Tried to predict over untrained model.")


