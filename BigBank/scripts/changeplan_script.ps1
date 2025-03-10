# run_changeplan.ps1

# Define the input and output directories for Changeplan test cases.
$INPUT_DIR = ".\changeplan\transaction_terminal_input"
$OUTPUT_DIR = ".\changeplan\transaction_terminal_output"

# Create the output directory if it doesn't exist or clear it if it does.
if (!(Test-Path $OUTPUT_DIR)) {
    New-Item -ItemType Directory -Path $OUTPUT_DIR | Out-Null
} else {
    Remove-Item "$OUTPUT_DIR\*" -Force -Recurse
}

# Loop through the 10 test files: changeplan01.inp to changeplan10.inp
for ($i = 1; $i -le 9; $i++) {
    $num = "{0:D2}" -f $i
    $INPUT_FILE = Join-Path $INPUT_DIR "changeplan$num.inp"
    $OUTPUT_FILE = Join-Path $OUTPUT_DIR "changeplan$num.bto"

    Write-Output "Running test changeplan$num..."

    # Run main.py with input redirection from the current test file and capture output.
    Get-Content $INPUT_FILE | python BigBank/main.py > $OUTPUT_FILE
}

Write-Output "All Changeplan tests completed. Check '$OUTPUT_DIR' for the console output of each test."
