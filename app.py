from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import tensorflow as tf
import numpy as np
from werkzeug.utils import secure_filename
import os
from PIL import Image
import io

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:3000", "http://127.0.0.1:3000"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"],
        "supports_credentials": True
    }
})

# Configure model paths - use absolute paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SPIRAL_MODEL_PATH = os.path.join(BASE_DIR, 'spiral_model.keras')
MRI_MODEL_PATH = os.path.join(BASE_DIR, 'mri_classifier.keras')

# Load both models
try:
    # Disable GPU warnings if you're not using GPU
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    
    print(f"Current working directory: {os.getcwd()}")
    print(f"Looking for spiral model at: {SPIRAL_MODEL_PATH}")
    print(f"Looking for MRI model at: {MRI_MODEL_PATH}")
    
    # Check if model files exist
    if not os.path.exists(SPIRAL_MODEL_PATH):
        raise FileNotFoundError(f"Spiral model not found at: {SPIRAL_MODEL_PATH}")
    if not os.path.exists(MRI_MODEL_PATH):
        raise FileNotFoundError(f"MRI model not found at: {MRI_MODEL_PATH}")

    # Load models with error handling
    try:
        print("Loading spiral model...")
        spiral_model = tf.keras.models.load_model(SPIRAL_MODEL_PATH)
        print("Spiral model loaded successfully!")
    except Exception as e:
        print(f"Error loading spiral model: {str(e)}")
        raise

    try:
        print("Loading MRI model...")
        mri_model = tf.keras.models.load_model(MRI_MODEL_PATH)
        print("MRI model loaded successfully!")
    except Exception as e:
        print(f"Error loading MRI model: {str(e)}")
        raise

except Exception as e:
    print(f"Error during initialization: {str(e)}")
    raise

# Configure upload folder
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Create necessary directories
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, 'static'), exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def preprocess_image(image_path):
    """Preprocess image for spiral model"""
    try:
        print(f"Starting preprocessing for {image_path}")
        

        img = Image.open(image_path).convert('L')
        print(f"Original image size: {img.size}")
        
        input_shape = spiral_model.input_shape[1:3]
        print(f"Target shape from model: {input_shape}")
        
        img = img.resize(input_shape)
        print(f"Resized image size: {img.size}")
        
        img_array = np.array(img)
        print(f"Array shape after conversion: {img_array.shape}")
        
       
        img_array = img_array.astype(np.float32) / 255.0
        img_array = np.expand_dims(img_array, axis=-1) 
        img_array = np.expand_dims(img_array, axis=0)   
        print(f"Final preprocessed shape: {img_array.shape}")
        
        return img_array
        
    except Exception as e:
        print(f"Error in spiral preprocessing: {str(e)}")
        print(f"Stack trace: ", exc_info=True)
        raise

def preprocess_mri_image(image_path):
    """Preprocess image for MRI model"""
    try:
        img = Image.open(image_path).convert('RGB')
        input_shape = mri_model.input_shape[1:3]
        img = img.resize(input_shape)
        img_array = np.array(img)
        img_array = img_array.astype(np.float32) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        return img_array
    except Exception as e:
        print(f"Error in MRI preprocessing: {str(e)}")
        raise

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            try:
                print("Processing spiral drawing image...")
                processed_image = preprocess_image(filepath)
                print(f"Processed image shape: {processed_image.shape}")
                
                prediction = spiral_model.predict(processed_image, verbose=1)
                print(f"Raw prediction output: {prediction}")
                
                prediction_value = float(prediction[0][0])
                print(f"Raw prediction value: {prediction_value}")
                
                has_parkinsons = bool(prediction_value < 0.5)  
                

                confidence = (1 - prediction_value) * 100 if has_parkinsons else prediction_value * 100
                
                print(f"Final results - Has Parkinsons: {has_parkinsons}, Confidence: {confidence}%")
                
                return jsonify({
                    'prediction': has_parkinsons,
                    'confidence': confidence,
                    'raw_prediction': prediction_value,
                    'message': 'Based on the spiral drawing analysis, ' + 
                              ('indicators of Parkinson\'s disease were detected' if has_parkinsons 
                               else 'no significant indicators of Parkinson\'s disease were found')
                })
                
            except Exception as e:
                print(f"Error during prediction: {str(e)}")
                return jsonify({'error': str(e)}), 500
            finally:
                if os.path.exists(filepath):
                    os.remove(filepath)
        
        return jsonify({'error': 'Invalid file type'}), 400
    
    except Exception as e:
        print(f"Server error in predict: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/predict_mri', methods=['POST'])
def predict_mri():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            try:
                processed_image = preprocess_mri_image(filepath)
                prediction = mri_model.predict(processed_image)
                
                print(f"MRI prediction shape: {prediction.shape}")
                print(f"MRI prediction values: {prediction}")
                
                prediction_value = float(prediction[0][0])
                has_parkinsons = prediction_value > 0.5
                
                # Calculate confidence percentage
                confidence = prediction_value * 100 if has_parkinsons else (1 - prediction_value) * 100
                
                return jsonify({
                    'prediction': has_parkinsons,
                    'confidence': confidence,
                    'raw_prediction': prediction_value,
                    'message': 'Based on the MRI scan analysis, ' + 
                              ('indicators of Parkinson\'s disease were detected' if has_parkinsons 
                               else 'no significant indicators of Parkinson\'s disease were found')
                })
                
            except Exception as e:
                return jsonify({'error': f'MRI Prediction failed: {str(e)}'}), 500
            finally:
                if os.path.exists(filepath):
                    os.remove(filepath)
        
        return jsonify({'error': 'Invalid file type'}), 400
    
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    try:
        # Check if models are loaded
        if spiral_model is None or mri_model is None:
            return jsonify({
                'status': 'unhealthy',
                'message': 'Models not loaded properly'
            }), 500

        # Check if upload directory exists
        if not os.path.exists(UPLOAD_FOLDER):
            return jsonify({
                'status': 'unhealthy',
                'message': 'Upload directory not found'
            }), 500

        # Check if static directory exists
        if not os.path.exists('static'):
            return jsonify({
                'status': 'unhealthy',
                'message': 'Static directory not found'
            }), 500

        return jsonify({
            'status': 'healthy',
            'message': 'All systems operational'
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'message': str(e)
        }), 500

REPORT_MAPPING = {
    "mri": os.path.join(os.path.dirname(__file__), "static/reports/MRI Report.pdf"),
    "spiral": os.path.join(os.path.dirname(__file__), "static/reports/Spiral Drawing Report.pdf")
}

@app.route('/download_report/<scan_type>', methods=['GET'])
def download_report(scan_type):
    try:
        scan_type = scan_type.lower()  # Convert to lowercase to make it case-insensitive
        if scan_type not in REPORT_MAPPING:
            return {"error": f"Invalid report type: {scan_type}"}, 400
            
        file_path = REPORT_MAPPING[scan_type]
        print(f"Attempting to serve file from: {file_path}")  # Debug print
        
        if not os.path.exists(file_path):
            return {"error": f"Report file not found at {file_path}"}, 404
            
        return send_file(
            file_path,
            as_attachment=True,
            download_name=f"parkinsons_{scan_type}_report.pdf",
            mimetype='application/pdf'
        )
    except Exception as e:
        print(f"Error in download_report: {str(e)}")  # Add logging
        return {"error": str(e)}, 500

@app.route('/check_files', methods=['GET'])
def check_files():
    files = {
        "critical": os.path.exists(REPORT_MAPPING["critical"]),
        "mild": os.path.exists(REPORT_MAPPING["mild"]),
        "paths": {
            "critical": REPORT_MAPPING["critical"],
            "mild": REPORT_MAPPING["mild"]
        }
    }
    return jsonify(files)

if __name__ == '__main__':
    print("\nStarting Flask application...")
    print(f"Upload folder: {UPLOAD_FOLDER}")
    print(f"Static folder: {os.path.join(BASE_DIR, 'static')}")
    app.run(host='0.0.0.0', port=5000, debug=True) 