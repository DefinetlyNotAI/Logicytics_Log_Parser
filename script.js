document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];

    if (!file) {
        alert('No file uploaded.');
        return;
    }

    if (!file.name.endsWith('.log')) {
        alert('Please upload a .log file only.');
        return;
    }

    const reader = new FileReader();
    reader.onload = function(e) {
        const logContent = e.target.result;
        parseLog(logContent);
    };
    reader.readAsText(file);
});

function parseLog(logContent) {
    const regexPattern = /\[(.*?)] > (\w+):.*?\| (.*)/g;
    const matches = [...logContent.matchAll(regexPattern)];

    let htmlTable = `
        <table>
            <tr>
                <th>Time</th>
                <th>Severity</th>
                <th>Data</th>
            </tr>
    `;

    matches.forEach(match => {
        const time = match[1];
        const severity = match[2].toLowerCase();
        const data = match[3].trim().replace(/\|$/, '');

        htmlTable += `
            <tr>
                <td>${time}</td>
                <td class="severity-${severity}">${severity}</td>
                <td>${data}</td>
            </tr>
        `;
    });

    htmlTable += '</table>';
    document.getElementById('logOutput').innerHTML = htmlTable;
}
