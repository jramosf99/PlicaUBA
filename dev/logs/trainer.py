import pickle
import pandas as pd
import sys
sys.path.append('../')

from loglizer import dataloader, preprocessing, PCA

struct_log_entreno = 'data/syslog2.csv' # The structured log file
#struct_log = '../data/HDFS/HDFS_100k.log_structured.csv' # The structured log file

if __name__ == '__main__':
    ## 1. Load strutured log file and extract feature vectors
    # Save the raw event sequence file by setting save_csv=True
    (x_train, _), (_, _) = dataloader.load_HDFS(struct_log_entreno, train_ratio=1)
    feature_extractor = preprocessing.FeatureExtractor()
    x_train = feature_extractor.fit_transform(x_train, term_weighting='tf-idf',normalization='zero-mean')
    pickle_file = open('feature_extractor.pickle', 'wb')
    pickle.dump(feature_extractor, pickle_file)
    pickle_file.close()
    ## 2. Train an unsupervised model
    print('Train phase:')
    
    # Initialize PCA, or other unsupervised models, LogClustering, InvariantsMiner
    model = PCA.pca() 
    
    # Model hyper-parameters may be sensitive to log data, here we use the default for demo
    model.fit(x_train)

    pickle_file = open('modelo.pickle', 'wb')
    pickle.dump(model, pickle_file)
    pickle_file.close()