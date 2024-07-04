from flask import Flask, render_template, request, redirect, url_for
import os
import pickle
from feature_extraction import extract_features
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
#app.secret_key = 'your_secret_key_here'

# Ensure upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Load your model
model = None  # Initialize model variable
model_name = 'Decision Tree'  # Default model

# Function to load model
def load_model(model_name):
    global model
    models = {
        'Decision Tree': 'decisiontree_model.sav',
        'KNN': 'knn_model.sav',
        'Random Forest': 'random_forest_model.sav'
    }
    model_path = models.get(model_name, 'decisiontree_model.sav')  # Default to Decision Tree
    if os.path.exists(model_path):
        model = pickle.load(open(model_path, 'rb'))
    else:
        raise FileNotFoundError(f"Model file {model_path} not found")

# Function to process predictions
def process_predictions(features):
    class_labels = ['OAM', 'VoIP', 'Bulk', 'Control', 'Critical', 'Default', 'P2P', 'Signaling', 'Transaction', 'Video']
    results = {}
    for feature in features:
        # Use the model to make a prediction
        prediction = model.predict([feature])[0]
        # Convert prediction to its corresponding class label
        class_label = class_labels[prediction]
        # Key as tuple of relevant flow features
        flow_key = (feature[3], feature[1], feature[4], feature[2], feature[0])  # (src_ip, src_port, dst_ip, dst_port, protocol)
        results[flow_key] = class_label
    return results


# Route for home page
@app.route('/')
def home():
    return render_template('home.html')

# Route for setting up index.html
@app.route('/index', methods=['GET', 'POST'])
def index():
    global model_name  # Ensure you're using the global model_name defined earlier

    # Determine paths for classification report and confusion matrix based on model_name
    if model_name == 'Decision Tree':
        confusion_matrix_src = "/static/7_cm_dt.png"
        classification_report_src = "/static/DT_ClassifyReport.png"
    elif model_name == 'KNN':
        confusion_matrix_src = "/static/7_cm_knn.png"
        classification_report_src = "/static/KNN_ClassifyReport.png"
    elif model_name == "Random Forest":
        confusion_matrix_src = "/static/7_cm_rf.png"
        classification_report_src = "/static/Random_ClassifyReport.png"
    else:
        # Handle default case
        confusion_matrix_src = ""
        classification_report_src = ""

    return render_template('index.html', model_name=model_name, classification_report_src=classification_report_src, confusion_matrix_src=confusion_matrix_src)


# Route for uploading PCAP file
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('index'))

    file = request.files['file']

    if file.filename == '':
        return redirect(url_for('index'))

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Extract features from the uploaded file
        features = extract_features(filepath)  # Pass the file path to extract_features function
        results = process_predictions(features)

        # Remove the uploaded file after processing
        os.remove(filepath)

        return render_template('results.html', results=results)

    return redirect(url_for('index'))
    
# Route for changing the model
@app.route('/change_model', methods=['POST'])
def change_model():
    global model_name
    model_name = request.form.get('model')
    load_model(model_name)
    return redirect(url_for('index'))

if __name__ == '__main__':
    load_model(model_name)  # Load the default model
    app.run(debug=True)
