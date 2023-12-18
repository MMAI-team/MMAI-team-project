# Whale Tail Classification System - MMAI

## Overview

The Whale Tail Classification System is designed to compare whale tail images, determining whether they belong to the same individual. The project is inspired by the [Humpback Whale Identification](https://www.kaggle.com/competitions/humpback-whale-identification) competition on Kaggle.

## Components

1. Data Loading and Preprocessing
   - Implemented functionality for fetching data from the competition website.
   - Processed and prepared data for training both the Convolutional Neural Network (CNN) model and feature point extraction.
     For additional information you can check [Data loading README](data_load/README.md).

2. CNN Model
   - Trained a convolutional neural network model capable of high-precision classification when provided with two whale tail images.
     To see model training process in detail you can check the [narrated CNN notebook](research/cnn/CNN_Siamese_97_mk2.ipynb)

3. Feature Points
   - Identified the optimal parameters for a feature point-based solution using the Scale-Invariant Feature Transform (SIFT) methodology.
     You can see the example of feature points application in the [Feature points notebook](research/feature_points/sift_matching.ipynb)

4. API
   - Developed an API for image classification, serving as a crucial tool for the Telegram bot and website components.
   - Enables requests from the Telegram bot and website to access the classification functionality without the need to individually deploy and manage the CNN model.

5. Telegram Bot
   - Implemented a Telegram bot that accepts two whale tail images and performs classification.
   - Users can choose between feature points or the CNN model for classification.
   - Deployed the Telegram bot on the Heroku platform, ensuring continuous access to its functionality.
   - User requests are forwarded to the API, and the classification results are returned.

6. iOS App
   - Developed an iOS application for convenient use of the system on iPhones.
   - Features an intuitive interface and aesthetically pleasing design for user-friendly interaction.
   - The model is stored locally on the user's device, allowing system usage even without an internet connection.

7. Website
   - Created a website for image classification, with user requests forwarded to the API.
   - Provides an accessible and user-friendly interface for interaction with the system.
   For additional information you can check [Website README](website_root/README.md).

## Conclusion

The Whale Tail Classification System offers a comprehensive solution for comparing whale tail images. Its modular design allows for flexibility in choosing classification methods, and the user-friendly interfaces provided by the Telegram bot, iOS app, and website enhance the overall accessibility of the system.
