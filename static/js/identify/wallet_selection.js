document.getElementById('runButton').addEventListener('click', function (event) {
    const loadingBar = document.getElementById('loading-bar');
    loadingBar.style.display = 'block';  // show loading bar when run starts

    // Disable all inputs immediately
    setInputsDisabled(true);

    const selectedWallets = [];
    const selectedBrowsers = {};

    // Get all wallet rows from the table
    const walletRows = document.querySelectorAll('#walletTable tbody tr');

    for (const row of walletRows) {
        const walletCheckbox = row.querySelector('input[name="wallet"]');
        const walletName = walletCheckbox.value;
        const browserCheckboxes = row.querySelectorAll(`input[name^="${walletName.replaceAll(' ', '_')}_browser"]`);

        if (walletCheckbox.checked) {
            selectedWallets.push(walletName);

            if (browserCheckboxes.length > 0) {
                const anyBrowserChecked = Array.from(browserCheckboxes).some(cb => cb.checked);

                if (!anyBrowserChecked) {
                    alert(`Please select at least one browser option for the wallet: "${walletName}"`);
                    event.preventDefault();
                    loadingBar.style.display = 'none';

                    // Re-enable inputs on validation failure
                    setInputsDisabled(false);
                    return;
                }

                selectedBrowsers[walletName] = Array.from(browserCheckboxes)
                    .filter(cb => cb.checked)
                    .map(cb => cb.value);
            } else {
                selectedBrowsers[walletName] = [];
            }
        }
    }

    // Send data to Flask
    fetch('/process_selection', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ wallets: selectedWallets, browsers: selectedBrowsers })
    }).then(() => {
        // Begin polling
        pollForCsvReady();
        pollForLogReady();
    }).catch(err => {
        console.error("Error sending selection:", err);
        loadingBar.style.display = 'none';

        // Re-enable inputs on error
        setInputsDisabled(false);
    });
});

let pollInterval = null;
let logPollInterval = null;

// Utility to disable/enable all inputs
function setInputsDisabled(state) {
    // OS selection radios
    document.querySelectorAll('input[name="choice"]').forEach(el => el.disabled = state);

    // Directory inputs
    document.getElementById('directoryPath').disabled = state;
    document.getElementById('outputPath').disabled = state;

    // Wallet & browser checkboxes
    document.querySelectorAll('#walletCheckboxes input[type="checkbox"]').forEach(el => el.disabled = state);

    // Run button
    document.getElementById('runButton').disabled = state;
}

// Poll CSV readiness and reload DataTable
function pollForCsvReady() {
    const outputDir = document.getElementById('outputPath')?.value;

    if (!outputDir) {
        console.warn("No output path provided.");
        const loadingBar = document.getElementById('loading-bar');
        loadingBar.style.display = 'none';
        setInputsDisabled(false);
        return;
    }

    if (pollInterval) clearInterval(pollInterval);

    pollInterval = setInterval(() => {
        fetch(`/csv_ready?output_dir=${encodeURIComponent(outputDir)}`)
            .then(response => response.json())
            .then(data => {
                if (data.ready) {
                    clearInterval(pollInterval);
                    pollInterval = null;

                    const loadingBar = document.getElementById('loading-bar');
                    loadingBar.style.display = 'none';

                    alert('Wallet Sleuth - Search Complete!');

                    // Re-enable all inputs after alert
                    setInputsDisabled(false);

                    // Reload DataTable
                    $('#outputTable').DataTable().ajax.reload(null, false);
                } else {
                    console.log("CSV not ready yet...");
                }
            })
            .catch(err => {
                console.error("Error checking CSV readiness:", err);
                const loadingBar = document.getElementById('loading-bar');
                loadingBar.style.display = 'none';
                setInputsDisabled(false);
            });
    }, 2000); // Check every 2 seconds
}

// Poll for log readiness and fetch log content
function pollForLogReady() {
    const outputDir = document.getElementById('outputPath')?.value;

    if (!outputDir) {
        console.warn("No output path provided.");
        return;
    }

    const logCheckInterval = setInterval(() => {
        fetch(`/log_ready?output_dir=${encodeURIComponent(outputDir)}`)
            .then(res => res.json())
            .then(data => {
                if (data.ready) {
                    clearInterval(logCheckInterval);

                    // Fetch and display the log content
                    fetch('/get_log_data', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' }
                    })
                    .then(res => res.json())
                    .then(data => {
                        document.getElementById('process-log-textarea').value = data.data;
                    })
                    .catch(err => {
                        document.getElementById('process-log-textarea').value = "Failed to load log content.";
                        console.error(err);
                    });
                }
            })
            .catch(err => {
                console.error("Error checking log readiness:", err);
            });
    }, 2000);
}

// Desktop wallets greyed out when "All Desktop Wallets" selected
document.addEventListener("DOMContentLoaded", function () {
    const walletCheckboxes = document.querySelectorAll('#walletCheckboxes input[type="checkbox"][name="wallet"]');

    function toggleLaptopWallets() {
        let allDesktopChecked = false;

        walletCheckboxes.forEach(cb => {
            if (cb.value.trim() === "All Desktop Wallets-desktop_wallets" && cb.checked) {
                allDesktopChecked = true;
            }
        });

        walletCheckboxes.forEach(cb => {
            const labelText = cb.closest("label").textContent;
            const hasLaptopIcon = labelText.includes("💻");

            if (hasLaptopIcon && cb.value !== "All Desktop Wallets-desktop_wallets") {
                cb.disabled = allDesktopChecked;

                const walletRow = cb.closest("tr");
                const browserCheckboxes = walletRow.querySelectorAll('input[type="checkbox"][name$="_browser"]');
                browserCheckboxes.forEach(bcb => bcb.disabled = allDesktopChecked);
            }

            if (!allDesktopChecked && hasLaptopIcon) {
                cb.disabled = false;
                const walletRow = cb.closest("tr");
                const browserCheckboxes = walletRow.querySelectorAll('input[type="checkbox"][name$="_browser"]');
                browserCheckboxes.forEach(bcb => bcb.disabled = false);
            }
        });
    }

    walletCheckboxes.forEach(cb => cb.addEventListener('change', toggleLaptopWallets));
});

// Browser wallets greyed out when "All Browser Wallets" selected
document.addEventListener("DOMContentLoaded", function () {
    const walletCheckboxes = document.querySelectorAll('#walletCheckboxes input[type="checkbox"][name="wallet"]');

    function toggleBrowserWallets() {
        let allBrowsersChecked = false;

        walletCheckboxes.forEach(cb => {
            if (cb.value.trim() === "All Browser Wallets-browser_wallets" && cb.checked) {
                allBrowsersChecked = true;
            }
        });

        walletCheckboxes.forEach(cb => {
            const labelText = cb.closest("label").textContent;
            const hasPuzzleIcon = labelText.includes("🧩");

            if (hasPuzzleIcon && cb.value !== "All Browser Wallets-browser_wallets") {
                cb.disabled = allBrowsersChecked;

                const walletRow = cb.closest("tr");
                const browserCheckboxes = walletRow.querySelectorAll('input[type="checkbox"][name$="_browser"]');
                browserCheckboxes.forEach(bcb => bcb.disabled = allBrowsersChecked);
            }

            if (!allBrowsersChecked && hasPuzzleIcon) {
                cb.disabled = false;
                const walletRow = cb.closest("tr");
                const browserCheckboxes = walletRow.querySelectorAll('input[type="checkbox"][name$="_browser"]');
                browserCheckboxes.forEach(bcb => bcb.disabled = false);
            }
        });
    }

    walletCheckboxes.forEach(cb => cb.addEventListener('change', toggleBrowserWallets));
});

// 100% vibe coded Javacript ✅
// i went through the code, tested it and removed what wasn't needed, but i don't know JavaScript. I had an AI assist me with this. 🤖