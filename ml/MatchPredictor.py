from MachineLearningModel import MachineLearningModel
from DataLoader import DataLoader
import ModelGlobals
import json
import argparse
import os



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", default=ModelGlobals.SERIALIZED_MODEL_PATH, help="Directory for serialized model.")
    parser.add_argument("-f", "--file", default=ModelGlobals.SERIALIZED_MODEL_FILE, help="Filename of serialized model.")
    parser.add_argument("-g", "--generateModel", action='store_true', default=True, help="Generate model instead of loading one.")
    parser.add_argument("-o", "--forceOverwrite", action='store_true', default=True, help="Force overwriting of existing serialized model.")
    parser.add_argument("-s", "--stopIterations", type=int, default=0, help="Stop loading data at this many matches.")
    args = parser.parse_args()

    m = MachineLearningModel()

    if args.generateModel:
        m.loadData(args.stopIterations)
        m.trainModel()
        m.serializeModel(args.path, args.file, args.forceOverwrite)

    else:
        m.loadModel(args.path, args.file)

    # dl = DataLoader()
    # formatted_data = dl.filterMatchFields(match_data)

    # m.predict(formatted_data)



if __name__ == "__main__":
    main()
