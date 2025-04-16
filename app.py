from flask import Flask, request, render_template, Response
from flask_wtf.csrf import CSRFProtect
import subprocess
import os, secrets, sys

# Disable buffering for stdout and stderr for monitoring team to check results in real time
sys.stdout.reconfigure(line_buffering=True)

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF protection for testing
csrf = CSRFProtect(app)

@app.route('/')
def index():
    return render_template('index.html')

def stream_process_output(command):
    '''
        Stream the output of a subprocess command for monitoring team of Entec.
    '''
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)
    try:
        for line in iter(process.stdout.readline, ''):
            # Stream stdout to the browser
            yield f"{line}<br>\n"
        for line in iter(process.stderr.readline, ''):
            # Stream stderr to the browser
            yield f"{line}<br>\n"
    finally:
        process.stdout.close()
        process.stderr.close()
        process.wait()  

@app.route('/run', methods=['POST'])
def run_script():
    script = request.form.get('script')  
    category = request.form.get('category')  

    if script == "logger":
        script_path = os.path.join(os.getcwd(), "logger_reader.py")
        if category:
            return Response(stream_process_output(["python3", script_path, category]), mimetype='text/html')
        else:
            return render_template('output.html', output=None, error="Category is required for logger reader.")

    elif script == "control":
        action = request.form.get('action', 'start')
        script_path = os.path.join(os.getcwd(), "logger_control.py")
        if category:
            return Response(stream_process_output(["python3", script_path, action, category]), mimetype='text/html')
        else:
            return render_template('output.html', output=None, error="Category is required for control scripts.")

    else:
        return render_template('output.html', output=None, error="Invalid script name")

if __name__ == '__main__':
    app.run(debug=True)