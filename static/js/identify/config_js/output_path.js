document.getElementById('outputPath').addEventListener('input', function () {
    const outputPath = this.value;

    fetch('/print_output_path', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ outputPath: outputPath })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Server response:', data);
    })
    .catch(err => {
        console.error('Error sending output path:', err);
    });
});

// 100% vibe coded Javacript ✅
// i went through the code, tested it and removed what wasn't needed, but i don't know JavaScript. I had an AI assist me with this. 🤖