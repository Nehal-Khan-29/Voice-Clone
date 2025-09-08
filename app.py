from flask import Flask, render_template, redirect, url_for, request, flash, session, jsonify
import os
from ml import trainingcode
from test import testingcode

# Pre-Req ====================================================================================================

UPLOAD_FOLDER = os.path.join('static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
MODEL_FOLDER = os.path.join('static', 'models')
os.makedirs(MODEL_FOLDER, exist_ok=True)
PROCESSED_FOLDER = os.path.join('static', 'processed')
os.makedirs(PROCESSED_FOLDER, exist_ok=True)
OUTPUT_FOLDER = os.path.join('static', 'output')
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Start Flask ====================================================================================================

app = Flask(__name__)
app.secret_key = 'your-very-secret-key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MODEL_FOLDER'] = MODEL_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Main ===========================================================================================================

@app.route('/', methods=['GET', 'POST'])
def home():
    return redirect(url_for('collect_data'))

@app.route('/training', methods=['GET', 'POST'])
def collect_data():
    if request.method == 'POST':
        user_name = request.form.get("user_name")

        if os.path.exists(UPLOAD_FOLDER):
            for f in os.listdir(UPLOAD_FOLDER):
                os.remove(os.path.join(UPLOAD_FOLDER, f))
        else:
            os.makedirs(UPLOAD_FOLDER)

        files = request.files
        if files:
            for key in files:
                audio = files[key]
                if audio:
                    save_path = os.path.join(UPLOAD_FOLDER, audio.filename)
                    audio.save(save_path)

            session['just_uploaded'] = True
            # ML CODE
            trainingcode(user_name)   
            return jsonify({'redirect': url_for('test_model')})

    return render_template('collect_data.html')

@app.route('/testing', methods=['GET', 'POST'])
def test_model():
    output_file = None

    models = os.listdir(app.config['MODEL_FOLDER'])

    if request.method == 'GET':
        just_uploaded = session.pop('just_uploaded', None)
        if just_uploaded:
            flash("Please wait, Model is being created.", "info")

    if request.method == 'POST':
        
        selected_model = request.form.get('selected_model') 
        text_to_clone = request.form.get('text_to_clone')

        if not selected_model:
            flash("No model selected!", "error")
        elif not text_to_clone:
            flash("Please enter text to clone!", "error")
        else:
            model_path = os.path.join(app.config['MODEL_FOLDER'], selected_model)
            
            try:
                output_file = testingcode(text_to_clone, model_path)
                flash("Voice Cloning Success!", "success")
            except Exception as e:
                print(f"Error during cloning: {str(e)}")
                flash(f"Error during cloning: {str(e)}", "error")

    return render_template('test_model.html', output_file=output_file, models=models)


# initialize =====================================================================================================

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)