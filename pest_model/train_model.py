from fastai.vision.all import *

# Download and prepare dataset (IP102 dataset for pest detection)
path = untar_data(URLs.IP102)
dls = ImageDataLoaders.from_folder(path, valid_pct=0.2, item_tfms=Resize(224))

# Load a pre-trained model (ResNet34)
learn = vision_learner(dls, resnet34, metrics=error_rate)
learn.fine_tune(4)

# Save the trained model
learn.export('pest_detector.pkl')

print("✅ Pest detection model trained and saved as pest_detector.pkl")
