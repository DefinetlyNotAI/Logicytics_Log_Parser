import re


with open('DEBUG.log', 'r') as file:
    log_output = file.read()

pattern = r'\[(.*?)\] > (\w+):.*?\| (.*)'
matches = re.findall(pattern, log_output)

html_table = """<link rel="stylesheet" href="styles.css">
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

open('DEBUG.html', 'w').write(html_table)
