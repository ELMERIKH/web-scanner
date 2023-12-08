import subprocess
from flask import Flask, render_template, request
from urllib.parse import urlparse 

app = Flask(__name__)

# Define a function to call the web vulnerability scanner
def web_vulnerability_scan(website_url):
    domain_name = urlparse(website_url).netloc
    report_file_name = f"{domain_name}_report.txt"
    scanner_output = subprocess.check_output(['python', 'web-vulnerability-scanner.py', 'full', website_url])
    with open(report_file_name, 'w') as report_file:
        report_file.write(scanner_output.decode('utf-8'))
    return report_file_name

@app.route('/test_website', methods=['POST'])
def test_website():
    website_url = request.form['website_url']

    # Call the web vulnerability scanner function
    report_file_name = web_vulnerability_scan(website_url)

    # Read the content of the report file
    with open(report_file_name, 'r') as report_file:
        tool_output = report_file.read()

    # Split the content by newlines for organized display
    tool_output_lines = tool_output.split('\n')

    return render_template('result.html', tool_output_lines=tool_output_lines)
@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)