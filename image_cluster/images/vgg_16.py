import os
import numpy as np
from random import randint
import tensorflow as tf

from tensorflow.keras.preprocessing.image import load_img 
from tensorflow.keras.preprocessing.image import img_to_array 
from tensorflow.keras.applications.vgg16 import preprocess_input 

from tensorflow.keras.applications.vgg16 import VGG16 
from tensorflow.keras.models import Model

from sklearn.metrics.pairwise import cosine_similarity


# enagle GPU usadge (CUDA and cuDNN needs to be set up beforehand)
physical_device = tf.config.experimental.list_physical_devices('GPU')
print('GPU number', len(physical_device))
tf.config.experimental.set_memory_growth(physical_device[0], True)

locating_img_dir = os.path.abspath('./'+'media/images/user_uploaded_images')
change_dir_to_img = os.chdir(locating_img_dir)

print(change_dir_to_img)
pictures = []

with os.scandir(change_dir_to_img) as files:
    for file in files:
        if file.name.endswith('.png') | file.name.endswith('.jpeg') | file.name.endswith ('.jpg'):
            pictures.append(file.name)
                            
# model used without the 'output layer'
model = VGG16()
model = Model(inputs = model.inputs, outputs = model.layers[-2].output)

def extract_features(file, model):
    img = load_img(file, target_size=(224,224))
    img = np.array(img) 
    reshaped_img = img.reshape(1,224,224,3) 
    imgx = preprocess_input(reshaped_img)
    features = model.predict(imgx, use_multiprocessing=True)
    return features

# feture data + picture title
data = {}
print(data)

for picture in pictures:
    try:
        feat = extract_features(picture,model)
        data[picture] = feat
        
    except:
    #    error needs to be raised!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        pass

# list of the filenames
filenames = np.array(list(data.keys()))

# list of the features
feat = np.array(list(data.values()))

# clustering
def cluster(filePaths, features, threshold=0.7):
    features = features.reshape(-1,4096)
    simMatrix = cosine_similarity(features)
    clusters = {}
    for i in range(len(features)):
        dupIdx = list(np.where(simMatrix[i] > threshold)[0])
        if len(dupIdx) > 1:
            curCluster, clusterMatch = list(dupIdx), None
            for cIdx in clusters:
                if curCluster[0] in clusters[cIdx]:
                    clusterMatch = cIdx
                    break
            if clusterMatch == None: clusters[len(clusters)] = curCluster
    for cIdx in clusters: clusters[cIdx] = [filePaths[x] for x in clusters[cIdx]]
    return clusters

# grouped images presented by theyre title (NOTE! if the file is unique the groupe will not be created therfore it will not be in the list)
img_clusters = cluster(filenames, feat)

print(img_clusters)