#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' This is a demo file for the PCA model.
    API usage:
        dataloader.load_HDFS(): load HDFS dataset
        feature_extractor.fit_transform(): fit and transform features
        feature_extractor.transform(): feature transform after fitting
        model.fit(): fit the model
        model.predict(): predict anomalies on given data
        model.evaluate(): evaluate model accuracy with labeled data
'''
import pandas as pd
import sys
sys.path.append('../')

from loglizer import dataloader, preprocessing, PCA
struct_log_test = 'data/syslog1.csv' # The structured log file
struct_log_entreno = 'data/syslog2.csv' # The structured log file
#struct_log = '../data/HDFS/HDFS_100k.log_structured.csv' # The structured log file

if __name__ == '__main__':
    ## 1. Load strutured log file and extract feature vectors
    # Save the raw event sequence file by setting save_csv=True
    (x_train, _), (_, _) = dataloader.load_HDFS(struct_log_entreno, train_ratio=1)
    feature_extractor = preprocessing.FeatureExtractor()
    x_train = feature_extractor.fit_transform(x_train, term_weighting='tf-idf',normalization='zero-mean')

    ## 2. Train an unsupervised model
    print('Train phase:')
    
    # Initialize PCA, or other unsupervised models, LogClustering, InvariantsMiner
    model = PCA.pca() 
    
    # Model hyper-parameters may be sensitive to log data, here we use the default for demo
    model.fit(x_train)
    
    # Make predictions and manually check for correctness. Details may need to go into the raw logs
    y_train = model.predict(x_train) 

    ## 3. Use the trained model for online anomaly detection
    print('Test phase:')
    
    # Load another new log file. Here we use struct_log for demo only
    (_, _), (x_test, _) = dataloader.load_HDFS(struct_log_test, window='session', split_type='sequential', train_ratio=0)
    # Go through the same feature extraction process with training, using transform() instead

    x_test = feature_extractor.transform(x_test) 

    # Finally make predictions and alter on anomaly cases
    y_test = model.predict(x_test)
    p = []
    for i in range(len(y_test)):
        if y_test[i] == 1:
            p.append(True)
        else:
            p.append(False)
    output = pd.read_csv(struct_log_test)
    output = output[p]
    output.to_csv('output.csv', index=False)

