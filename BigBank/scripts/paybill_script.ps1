# run_paybill.ps1
# Directories for Paybill test inputs and outputs
$INPUT_DIR = ".\paybill\transaction_terminal_input"
$OUTPUT_DIR = ".\paybill\transaction_terminal_output"

# Create the output directory if it doesn't exist, or clean it if it does.
if (!(Test-Path $OUTPUT_DIR)) {
    New-Item -ItemType Directory -Path $OUTPUT_DIR | Out-Null
} else {
    Remove-Item "$OUTPUT_DIR\*" -Force -Recurse
}

# Loop through the 10 test files: paybill01.inp to paybill10.inp
for ($i = 1; $i -le 10; $i++) {
    $num = "{0:D2}" -f $i
    $INPUT_FILE = Join-Path $INPUT_DIR "paybill$num.inp"
    $OUTPUT_FILE = Join-Path $OUTPUT_DIR "paybill$num.bto"

    Write-Output "Running test paybill$num..."

    # Run main.py with input redirection from the current test file and capture output.
    # This pipes the content of the input file to the Python program.
    Get-Content $INPUT_FILE | python BigBank/main.py > $OUTPUT_FILE
}

Write-Output "All tests completed. Check '$OUTPUT_DIR' for the console output of each test."
