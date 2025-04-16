from flask import Flask, request, render_template
from flask_wtf.csrf import CSRFProtect
import subprocess
import os, secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF protection for testing
csrf = CSRFProtect(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def run_script():
    script = request.form.get('script')

    if script == "logger":
        
        script_path = os.path.join(os.getcwd(), "logger_reader.py")
        try:
            process = subprocess.Popen(["python3", script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()
            print(stdout)
            print(stderr)

            # expose both stdout and stderr to the template
            return render_template('output.html', output=stdout, error=stderr)
        except Exception as e:
            return render_template('output.html', output=None, error=str(e))

    elif script == "control":

        action = request.form.get('action', 'start')  # Default to "start" because it doesn't do anything if already started
        try:
            script_path = os.path.join(os.getcwd(), "logger_control.py")
            process = subprocess.Popen(["python3", script_path, action], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()
            print(stdout)
            print(stderr)

            # expose both stdout and stderr to the template
            return render_template('output.html', output=stdout, error=stderr)
        except Exception as e:
            return render_template('output.html', output=None, error=str(e))

    else:
        return render_template('output.html', output=None, error="Invalid script name")

if __name__ == '__main__':
    app.run(debug=True)