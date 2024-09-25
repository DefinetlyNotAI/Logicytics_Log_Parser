function uploadLogFile() {
    const file = document.getElementById('uploadFile').files[0];
    if (!file || !file.name.endsWith('.log')) {
        alert('Invalid file');
        return;
    }

    const fileName = file.name.split('.')[0];
    fetch('/parse', { method: 'POST', body: file })
        .then(response => response.text())
        .then(() => {
            const htmlFile = fileName === 'DEBUG' ? 'debug.html' : 'Logs.html';
            window.open(htmlFile);
        });
}
