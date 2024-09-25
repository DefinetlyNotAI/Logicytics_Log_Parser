from flask import Flask, request
import re
app = Flask(__name__)


def parse_log_lib(Log_Name: str, HTML_Name: str, regex_pattern: str = r'\[(.*?)\] > (\w+):.*?\| (.*)', css_template: str = 'styles.css'):
    with open(Log_Name, 'r') as file:
        log_output = file.read()

    matches = re.findall(regex_pattern, log_output)

    html_table = f"""<link rel="stylesheet" href="{css_template}">
    <table>
        <tr>
            <th>Time</th>
            <th>Severity</th>
            <th>Data</th>
        </tr>
    """
    for match in matches:
        text = match[2].strip().removesuffix('|')
        cleaned_text = text.rstrip()
        html_table += f"""    <tr>
            <td>{match[0]}</td>
            <td class="{match[1].lower()}">{match[1]}</td>
            <td>{cleaned_text}</td>
        </tr>\n"""
    html_table += "</table>"

    open(HTML_Name, 'w').write(html_table)


@app.route('/parse', methods=['POST'])
def parse_log():
    file = request.files['file']
    name = file.filename.split('.')[0]

    if name == 'DEBUG':
        return parse_log_lib('DEBUG.log', 'debug.html')
    elif name == 'Logicytics':
        return parse_log_lib('Logicytics.log', 'Logs.html')
    else:
        return 'Error: Invalid file'


if __name__ == '__main__':
    app.run()
