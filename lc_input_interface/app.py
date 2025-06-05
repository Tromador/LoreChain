# app.py

import argparse
import time
from flask import Flask, render_template, request
from input_providers.manual import ManualInputProvider
from input_providers.live import LiveInputProvider
from langchain_relay import process_input
from lc_core import save_memory  # Assumes lc_core exists

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ''
    error_message = ''
    if request.method == 'POST':
        text_input = request.form.get('text_input', '')
        file = request.files.get('file_input', None)
        input_provider = ManualInputProvider(text_input, file)
        chunk = input_provider.get_next_chunk()
        if chunk.startswith("Error:"):
            error_message = chunk
        else:
            result = process_input(chunk)
    return render_template('input_form.html', result=result, error=error_message)

@app.route('/save', methods=['POST'])
def trigger_save():
    try:
        save_memory()
        return render_template('input_form.html', result='✅ Memory saved to disk.', error='')
    except Exception as e:
        return render_template('input_form.html', result='', error=f'Error during save: {e}')

def run_flask_app(host, port):
    print(f"Starting Flask app on {host}:{port}")
    app.run(debug=True, host=host, port=port)

def run_live_mode(log_file_path):
    print(f"Starting LiveInputProvider for {log_file_path}")
    input_provider = LiveInputProvider(log_file_path)
    while True:
        try:
            chunk = input_provider.get_next_chunk()
            output = process_input(chunk)
            print(f"LangChain Output:\n{output}")
            time.sleep(1)
        except NotImplementedError:
            print("LiveInputProvider not yet implemented. Exiting.")
            break

def main():
    parser = argparse.ArgumentParser(description="LC Input Interface Module")
    parser.add_argument('--mode', choices=['text', 'live'], default='text', help="Input mode: 'text' or 'live'")
    parser.add_argument('--host', default='127.0.0.1', help="Host IP (default: 127.0.0.1)")
    parser.add_argument('--port', default=5000, type=int, help="Port (default: 5000)")
    parser.add_argument('--logfile', default='/path/to/logfile.jsonl', help="Path to log file for live mode")
    args = parser.parse_args()

    if args.mode == 'text':
        run_flask_app(args.host, args.port)
    elif args.mode == 'live':
        run_live_mode(args.logfile)
    else:
        print("Invalid mode. Use --mode text or --mode live.")

if __name__ == '__main__':
    main()
