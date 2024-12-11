# -*- coding: utf-8 -*-
"""Mask Detecction.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Np_4Jod2geBEM3yIwynHChGjl3C5AbT3

# Importing Libraries
"""

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from keras.models import model_from_json
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from keras.layers import Dense,Flatten,Conv2D,MaxPooling2D,Dropout
from keras.models import Sequential
from keras.optimizers import Adam

"""# Data Collection"""

features = []
target = []

data_dir = "C:/Users/anand/Downloads/Projects/Mask Dtection Model/dataset"

for folder_name in os.listdir(data_dir):
    if os.path.isdir(os.path.join(data_dir, folder_name)):
        label = 0 if folder_name == "without_mask" else 1
        for filename in os.listdir(os.path.join(data_dir, folder_name)):
            image_path = os.path.join(data_dir, folder_name, filename)
            try:
                image = cv2.imread(image_path)
                if image is not None:
                    image = cv2.resize(image, (100, 100))
                    features.append(image)
                    target.append(label)
            except Exception as e:
                print(f"Error reading image {image_path}: {e}")

        print(f"Processed images in folder: {folder_name}")

plt.figure(figsize=(10,10))
plt.subplot(4,5,1)
plt.imshow(features[1950])
plt.show()

target[1950]

os.listdir("C:/Users/anand/Downloads/Projects/Mask Dtection Model/dataset")
features=np.array(features)
target=np.array(target)
features.shape
target.shape

"""# Splitting the data in to Traing and Testing data"""

features_train,features_test,target_train,target_test=train_test_split(features,target,test_size=0.2)
features_train.shape
# target_train.shape
# features_test.shape

plt.figure(figsize=(10,10))
plt.subplot(4,5,1)
plt.imshow(features_train[240])
plt.show()

target_train[240]

"""# Data Preprocessing"""

def preprocessing(image):
    image=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    image=image/255
    return image

features_train=np.array(list(map(preprocessing,features_train)))

features_train=features_train.reshape(3048, 100, 100,1)

dataGen=ImageDataGenerator(rotation_range=10,width_shift_range=0.1,height_shift_range=0.1,zoom_range=0.2,shear_range=0.1)
dataGen.fit(features_train)
batches=dataGen.flow(features_train,target_train,batch_size=20)
images,labels=next(batches)

plt.figure(figsize=(10,10))
for i in range(0,20):
    plt.subplot(4,5,i+1)
    plt.imshow(images[i].reshape(100,100))
plt.show()

target_train=to_categorical(target_train)
target_train.shape

"""# Model Creation"""

model=Sequential()
model.add(Conv2D(100,(3,3),activation="relu",input_shape=(100,100,1)))
model.add(Conv2D(200,(3,3),activation="relu"))
model.add(MaxPooling2D((2,2)))
model.add(Conv2D(100,(3,3),activation="relu"))
model.add(Conv2D(100,(3,3),activation="relu"))
model.add(Conv2D(100,(3,3),activation="relu"))
model.add(MaxPooling2D((2,2)))
model.add(Dropout(0.5))
model.add(Flatten())
model.add(Dense(500,activation="relu"))
model.add(Dense(2,activation="softmax"))

"""# Model Compilation and Model Fitting"""

model.compile(Adam(learning_rate=0.001),loss="categorical_crossentropy",metrics=["accuracy"])

model.fit(dataGen.flow(features_train, target_train, batch_size=20), epochs=20)

"""# Step 4: Saving and Loading Model"""

model_json=model.to_json()
with open("Mask_Detection.json","w") as abc:
    abc.write(model_json)
    abc.close()
model.save_weights("MaskDetection.weights.h5")
print("Save the Model")

from tensorflow.keras.models import model_from_json
from tensorflow.keras.models import Sequential

# Load the JSON model architecture
json_file = open("Mask_Detection.json", "r")
loaded_model_json = json_file.read()
json_file.close()

# Load the model from the JSON file
# Provide the Sequential class to the custom_objects parameter
loaded_model = model_from_json(loaded_model_json, custom_objects={"Sequential": Sequential})

# Load the weights
loaded_model.load_weights("C:/Users/anand/Downloads/Projects/Mask Dtection Model/mask detection/MaskDetection.weights.h5")
print("Loaded Model Successfully")

def getClassName(classNo):
    if   classNo == 1: return 'With Mask'
    elif classNo == 0: return 'Without Mask'

capt=cv2.VideoCapture(0)
capt.set(3,640)
capt.set(4,480)
capt.set(10,180)

"""# Detecting Mask using Integrated Camera

face_cascade = cv2.CascadeClassifier("C:/Users/anand/anaconda3/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml")
while True:
    message, image = capt.read()

    if image is None:
        print("Error reading image!")
        continue

    imagearr = np.asarray(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.05, 3)

    for (x, y, w, h) in faces:
        detectedFace = image[y:y + h, x:x + w]
        detectedFace = cv2.resize(detectedFace, (100, 100))
        detectedFace = preprocessing(detectedFace)
        detectedFace = detectedFace.reshape(1, 100, 100, 1)
        predictions = loaded_model.predict(detectedFace)
        classIndex = np.argmax(predictions, axis=-1)

        probabilityValue = np.amax(predictions)
        print(probabilityValue)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

        if probabilityValue > 0.75:
            class_name = getClassName(classIndex)
            cv2.putText(image, class_name, (x, y - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            cv2.putText(image, str(int(probabilityValue * 100)) + " %", (x + 120  , y - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            print(class_name)

    cv2.imshow("Model Prediction", image)
    returnedValue = cv2.waitKey(1)

    if returnedValue == ord("s") or returnedValue == ord("S"):
        cv2.destroyAllWindows()
        break
"""

import cv2
import numpy as np

# Initialize the video capture object

# Load the Haar cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Verify if the classifier loaded correctly
if face_cascade.empty():
    print("Error loading Haar cascade file")
    exit()

while True:
    # Read frame from the video capture
    ret, image = capt.read()

    if not ret or image is None:
        print("Error reading image!")
        continue

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale image
    faces = face_cascade.detectMultiScale(gray, 1.05, 3)

    for (x, y, w, h) in faces:
        detectedFace = image[y:y + h, x:x + w]
        detectedFace = cv2.resize(detectedFace, (100, 100))
        detectedFace = preprocessing(detectedFace)  # Ensure this function is defined
        detectedFace = detectedFace.reshape(1, 100, 100, 1)
        predictions = loaded_model.predict(detectedFace)  # Ensure 'loaded_model' is defined
        classIndex = np.argmax(predictions, axis=-1)
        probabilityValue = np.amax(predictions)

        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

        if probabilityValue > 0.30:
            class_name = getClassName(classIndex)  # Ensure 'getClassName' is defined
            cv2.putText(image, class_name, (x, y - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            cv2.putText(image, str(int(probabilityValue * 100)) + " %", (x + 120, y - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            print(class_name)

    cv2.imshow("Model Prediction", image)
    returnedValue = cv2.waitKey(1)

    if returnedValue == ord("s") or returnedValue == ord("S"):
        cv2.destroyAllWindows()
        break

# Release the video capture object
capt.release()
