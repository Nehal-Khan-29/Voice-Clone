from flask import Flask, render_template, redirect, url_for, request, flash, session
import os
import secrets

# Pre-Req ====================================================================================================

UPLOAD_FOLDER = os.path.join('static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Start Flask ====================================================================================================

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Main ===========================================================================================================

@app.route('/', methods=['GET', 'POST'])
def home():
    return redirect(url_for('collect_data'))

@app.route('/training', methods=['GET', 'POST'])
def collect_data():
    if request.method == 'POST':
        files = request.files
        if files:
            for key in files:
                audio = files[key]
                if audio:
                    save_path = os.path.join(app.config['UPLOAD_FOLDER'], audio.filename)
                    audio.save(save_path)
            session['just_uploaded'] = True
            return redirect(url_for('test_model'))
        
    return render_template('collect_data.html')

@app.route('/testing', methods=['GET', 'POST'])
def test_model():
    if session.get('just_uploaded'):
        flash("Please wait, Model is being created.", "success")
            # ML logic here
    return render_template('test_model.html')

# initialize =====================================================================================================

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)