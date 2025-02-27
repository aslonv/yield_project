import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, UpSampling2D, Concatenate

def unsupervised_change_detection(pre_features, post_features):
    """Unsupervised change detection using PCA and K-Means."""
    diff = post_features - pre_features
    pca = PCA(n_components=2).fit_transform(diff.reshape(-1, diff.shape[0]))
    clusters = KMeans(n_clusters=2).fit_predict(pca)  # Standing (0) vs. damaged (1)
    damage_map = clusters.reshape(diff.shape[1], diff.shape[2])
    return damage_map

def build_unet(input_shape):
    """Build a simple U-Net for semantic segmentation."""
    inputs = Input(input_shape)
    # Encoder
    conv1 = Conv2D(64, 3, activation='relu', padding='same')(inputs)
    pool1 = MaxPooling2D(pool_size=(2, 2))(conv1)
    # Decoder
    up1 = UpSampling2D(size=(2, 2))(pool1)
    conv2 = Conv2D(64, 3, activation='relu', padding='same')(up1)
    outputs = Conv2D(1, 1, activation='sigmoid')(conv2)  # Binary classification (standing/damaged)
    model = Model(inputs, outputs)
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

def supervised_classification(features, labels):
    """Train a Random Forest classifier on labeled features."""
    rf = RandomForestClassifier(n_estimators=100)
    rf.fit(features, labels)
    return rf

if __name__ == "__main__":
    # Replace with actual data paths and labels)
    pre_ndvi, pre_texture = np.random.rand(100, 100), np.random.rand(100, 100)  # Placeholder
    post_ndvi, post_texture = np.random.rand(100, 100), np.random.rand(100, 100)  # Placeholder
    features = np.stack([pre_ndvi, post_ndvi, pre_texture, post_texture], axis=-1)
    
    # Unsupervised detection
    damage_map = unsupervised_change_detection(pre_ndvi, post_ndvi)
    print("Damage map shape:", damage_map.shape)

    # Supervised classification (assuming labeled samples in data/labels/)
    # Load labels (e.g., CSV with 0=standing, 1=damaged)
    labels = np.random.randint(0, 2, (10000,))  # Placeholder
    flat_features = features.reshape(-1, features.shape[-1])
    rf_model = supervised_classification(flat_features, labels)
    print("Random Forest trained successfully")

    # U-Net for segmentation (example with dummy data)
    unet = build_unet((100, 100, 4))  # Example shape
    unet.fit(features, damage_map, epochs=1, batch_size=32, verbose=1)  # Placeholder training
    print("U-Net trained successfully")