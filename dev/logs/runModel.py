import pandas as pd
import sys
import pickle
sys.path.append('../')
from loglizer import dataloader, preprocessing, PCA
if __name__ == '__main__':
    struct_log_test = 'data/syslog1.csv' # The structured log file
    # Load another new log file. Here we use struct_log for demo only
    (_, _), (x_test, _) = dataloader.load_HDFS(struct_log_test, window='session', split_type='sequential', train_ratio=0)
    # Go through the same feature extraction process with training, using transform() instead
    pickle_file = open('feature_extractor.pickle', 'rb')
    feature_extractor = pickle.load(pickle_file)
    x_test = feature_extractor.transform(x_test)

    # Finally make predictions and alter on anomaly cases
    pickle_file = open('modelo.pickle', 'rb')
    model = pickle.load(pickle_file)
    y_test = model.predict(x_test)
    t=0
    p = []
    for i in range(len(y_test)):
        if y_test[i] == 1:
            t+=1
            p.append(True)
        else:
            p.append(False)
    output = pd.read_csv(struct_log_test)
    output = output[p]
    output.to_csv('output.csv', index=False)
    print(t)