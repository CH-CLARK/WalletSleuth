document.getElementById('directoryPath').addEventListener('input', function () {
    const directoryPath = this.value;

    fetch('/print_directory_path', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ directoryPath: directoryPath })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Server response:', data);
    })
    .catch(err => {
        console.error('Error sending directory path:', err);
    });
});

// 100% vibe coded Javacript ✅
// i went through the code, tested it and removed what wasn't needed, but i don't know JavaScript. I had an AI assist me with this. 🤖