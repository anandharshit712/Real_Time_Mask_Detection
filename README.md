
# Real-Time Face Mask Detection

This project implements a real-time face mask detection system using deep learning techniques. 
It utilizes a Convolutional Neural Network (CNN) to classify individuals as wearing a mask or not, processing live video streams to ensure compliance with health guidelines.

## Features

- **Real-Time Detection**: Processes live video feeds to detect face masks instantaneously.
- **High Accuracy**: Employs a trained CNN model to achieve reliable detection results.
- **User-Friendly Interface**: Simple setup and execution for immediate use.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/anandharshit712/Real_Time_Mask_Detection.git
   cd Real_Time_Mask_Detection
   ```
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the Detection Script**:
   ```bash
   python detect_mask_video.py
   ```
2. **Operation**:
   - Ensure your webcam is connected.
   - The system will display a live video feed with bounding boxes around detected faces, indicating "Mask" or "No Mask".
   - Press 'q' to exit the application.

## Dataset

The model is trained on a dataset comprising images of individuals with and without face masks. 
The dataset includes both real and augmented images to enhance model robustness. 
For more information, refer to the [Masked Face Recognition Dataset and Application](https://arxiv.org/abs/2003.09093).

## Model Architecture

The face mask detector is built using a Convolutional Neural Network (CNN) architecture. 
The model was trained using TensorFlow and Keras, achieving high accuracy in distinguishing between masked and unmasked faces.

## References

This project is inspired by and adapted from various open-source face mask detection projects, including:

- [Real-Time Face Mask Detection by naemazam](https://github.com/naemazam/Real-Time-Face-Mask-Detection)
- [Real-Time Face Mask Detection by AliElneklawy](https://github.com/AliElneklawy/real-time-face-mask-detection)
- [Face Mask Detector by Karan-Malik](https://github.com/Karan-Malik/FaceMaskDetector)

## License

This project is licensed under the MIT License.

## Acknowledgements

Special thanks to the contributors of the datasets and open-source projects that made this work possible.

---

*Note: This README provides an overview of the Real-Time Face Mask Detection project. For detailed information, please refer to the project's documentation and source code.*
