from MachineLearningModel import MachineLearningModel
from DataLoader import DataLoader
import ModelGlobals
import json
import argparse
import os
import glob


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", default=ModelGlobals.SERIALIZED_MODEL_PATH, help="Directory for serialized model.")
    parser.add_argument("-f", "--file", default=ModelGlobals.SERIALIZED_MODEL_FILE, help="Filename of serialized model.")
    parser.add_argument("-g", "--generateModel", action='store_true', default=False, help="Generate model instead of loading one.")
    parser.add_argument("-o", "--forceOverwrite", action='store_true', default=False, help="Force overwriting of existing serialized model.")
    parser.add_argument("-s", "--stopIterations", type=int, default=0, help="Stop loading data at this many matches.")
    parser.add_argument("-l", "--load", default="lcs_match_data", help="Load matches to predict from this directory.")
    parser.add_argument("-t", "--test", action='store_true', default=False, help="Run testing data.")
    args = parser.parse_args()

    m = MachineLearningModel("linear")

    if args.generateModel:
        m.loadData(args.stopIterations)
        m.trainModel()
        m.serializeModel(args.path, args.file, args.forceOverwrite)

    else:
        m.loadModel(args.path, args.file)
        for json_file in glob.glob(args.load + "/*.json"):
            with open(json_file, 'r') as fp:
                match_data = json.load(fp)
            print "Results[{}], Match[{}]".format(m.predict(match_data), json_file.replace(args.load, "").replace("/", "").replace("\\", ""))


    if args.test:
        m.loadData()
        m.testModel(40000)



if __name__ == "__main__":
    main()
