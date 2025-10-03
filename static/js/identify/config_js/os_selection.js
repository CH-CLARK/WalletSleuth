// On OS radio button change, POST new OS selection then redirect
document.querySelectorAll('#radioFrame input[name="choice"]').forEach(radio => {
    radio.addEventListener('change', () => {
        const selectedOS = radio.value;

        fetch('/print_os_selection', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ os_choice: selectedOS })
        })
        .then(() => {
            window.location.href = `/identify?os=${selectedOS}`;
        })
        .catch(err => {
            console.error('Error updating OS selection:', err);
        });
    });
});

// On page load, set the OS radio button checked based on URL param
document.addEventListener('DOMContentLoaded', () => {
    const params = new URLSearchParams(window.location.search);
    const os = params.get('os') || 'windows';

    const radioToCheck = document.querySelector(`#radioFrame input[name="choice"][value="${os}"]`);
    if (radioToCheck) radioToCheck.checked = true;

    // Update directory label and placeholders accordingly
    const directoryLabel = document.querySelector('label[for="directoryPath"]');
    const directoryInput = document.getElementById('directoryPath');
    const outputInput = document.getElementById('outputPath');

    if (os === 'mac') {
        directoryLabel.textContent = 'Library Directory:';
        directoryInput.placeholder = '\\Volumes\\Macintosh HD\\Users\\**USERNAME**';
        outputInput.placeholder = '\\Volumes\\**OUTPUT_VOLUME**\\Output\\Path';
    } else if (os === 'windows') {
        directoryLabel.textContent = 'Appdata Directory:';
        directoryInput.placeholder = 'C:\\Users\\**USERNAME**';
        outputInput.placeholder = 'D:\\Output\\Path';
    }
});

// 100% vibe coded Javacript ✅
// i went through the code, tested it and removed what wasn't needed, but i don't know JavaScript. I had an AI assist me with this. 🤖