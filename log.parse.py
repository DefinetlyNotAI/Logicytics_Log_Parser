import re
from flask import Flask, request, render_template_string

app = Flask(__name__)


def parse_log_lib(Log_Name: str, HTML_Name: str, regex_pattern: str = r'\[(.*?)\] > (\w+):.*?\| (.*)',
                  css_template: str = 'log.styles.css'):
    with open(Log_Name, 'r') as file:
        log_output = file.read()

    matches = re.findall(regex_pattern, log_output)

    html_table = f"""
    <style>
{open(css_template, 'r').read()}
    </style>
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


def err_400(special_message: str = "The server cannot process the request due to invalid syntax.") -> tuple[str, int]:
    body = "{ font-family: Arial, sans-serif; text-align: center; background-color: #f0f0f0; }"
    color = "{color: #ff0000; }"
    p_color = "{ color: #666; }"
    return rf'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Error 400</title>
    <style>
        body {body}
        h1 {color}
        p {p_color}
    </style>
</head>
<body>
    <h1>Error 400: Bad Request</h1>
    <p>{special_message}</p>
    <a href="/">Back to Home</a>
</body>
</html>
    ''', 400


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        uploaded_file = request.files.get('file')
        if not uploaded_file:
            return err_400("No file uploaded.")

        if not uploaded_file.filename.endswith('.log'):
            return err_400("Please upload a .log file only.")

        log_content = uploaded_file.read().decode('utf-8')
        open('Log.log', 'w').write(log_content)
        parse_log_lib("Log.log", 'Log.html')
        return render_template_string(open('Log.html').read())

    return '''
    <form action="" method="post" enctype="multipart/form-data">
        <input type="file" name="file" accept=".log">
        <input type="submit" value="Upload">
    </form>
    '''


if __name__ == '__main__':
    app.run(debug=True)
