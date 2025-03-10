# run_disable.ps1
# This PowerShell script tests the "Disable" functionality of the Bigbank program.
# It reads test input files from the designated directory, runs main.py with input redirection,
# and writes the console output to the corresponding output files.

# Define the input and output directories for Disable test cases.
$INPUT_DIR = ".\disable\transaction_terminal_input"
$OUTPUT_DIR = ".\disable\transaction_terminal_output"

# Create the output directory if it doesn't exist, or clear it if it does.
if (!(Test-Path $OUTPUT_DIR)) {
    New-Item -ItemType Directory -Path $OUTPUT_DIR | Out-Null
} else {
    Remove-Item "$OUTPUT_DIR\*" -Force -Recurse
}

# Loop through the 10 test files: disable01.inp to disable10.inp
for ($i = 1; $i -le 10; $i++) {
    $num = "{0:D2}" -f $i
    $INPUT_FILE = Join-Path $INPUT_DIR "disable$num.inp"
    $OUTPUT_FILE = Join-Path $OUTPUT_DIR "disable$num.bto"

    Write-Output "Running test disable$num..."

    # Run main.py with input redirection from the current test file and capture output.
    Get-Content $INPUT_FILE | python BigBank/main.py > $OUTPUT_FILE
}

Write-Output "All Disable tests completed. Check '$OUTPUT_DIR' for the console output of each test."
