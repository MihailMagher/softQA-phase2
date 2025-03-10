# run_logout.ps1

# Directories
$INPUT_DIR = ".\logout\transaction_terminal_input"
$OUTPUT_DIR = ".\logout\transaction_terminal_output"

# Create/clean the output directory
if (!(Test-Path $OUTPUT_DIR)) {
    New-Item -ItemType Directory -Path $OUTPUT_DIR | Out-Null
} else {
    Remove-Item "$OUTPUT_DIR\*" -Force -Recurse
}

# Loop through the 12 test files: create01.txt ... create11.txt
for ($i = 1; $i -le 3; $i++) {
    $num = "{0:D2}" -f $i
    $INPUT_FILE = Join-Path $INPUT_DIR "logout$num.inp"
    $OUTPUT_FILE = Join-Path $OUTPUT_DIR "logout$num.bto"

    Write-Output "Running test logout$num..."

    # Run main.py with input redirection and capture output.
    # In PowerShell, we can read the content of the input file and pipe it to Python.
    Get-Content $INPUT_FILE | python BigBank/main.py > $OUTPUT_FILE
}

Write-Output "All tests completed. Check '$OUTPUT_DIR' for the console output of each test."
