import os
import re
from flask import Flask, request, render_template_string

app = Flask(__name__)


def parse_log_lib(Log_Name: str, HTML_Name: str, regex_pattern: str = r'\[(.*?)\] > (\w+):.*?\| (.*)',
                  css_template: str = 'log.styles.css'):
    with open(Log_Name, 'r') as file:
        log_output = file.read()

    matches = re.findall(regex_pattern, log_output)

    html_table = f"""<style>
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
    html_table += "</table>\n"

    open(HTML_Name, 'w').write(html_table)


def err_400(special_message: str = "The server cannot process the request due to invalid syntax.") -> tuple[str, int]:
    return f'''
<style>
    {open("err.styles.css", 'r').read()}
</style>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->

    <title>404 HTML Template by Colorlib</title>

    <!-- Google font -->
    <link href="https://fonts.googleapis.com/css?family=Montserrat:200,400,700" rel="stylesheet">

    <!-- Custom stylesheet -->
    <link type="text/css" rel="stylesheet" href="err.styles.css"/>

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
    <script src="https://oss.maxcdn.com/html5shiv/3.7.3/html5shiv.min.js"></script>
    <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->

</head>
<body>
<div id="notfound">
    <div class="notfound">
        <div class="notfound-404">
            <h1>Oops!</h1>
            <h2>400 - {special_message}</h2>
        </div>
        <a href="/">Go To Homepage</a>
    </div>
</div>
</body>
<!-- These templates were made by Colorlib (https://colorlib.com) -->
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
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
