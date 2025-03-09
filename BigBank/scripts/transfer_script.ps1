# run_transfers.ps1

# Directories
$INPUT_DIR = ".\transfer\transaction_terminal_input"
$OUTPUT_DIR = ".\transfer\transaction_terminal_output"

# Create the output directory if it doesn't exist
if (!(Test-Path $OUTPUT_DIR)) {
    New-Item -ItemType Directory -Path $OUTPUT_DIR | Out-Null
} else {
    Remove-Item "$OUTPUT_DIR\*" -Force -Recurse
}

# Loop through transfer test files transfer01.txt through transfer12.txt
for ($i = 1; $i -le 11; $i++) {
    $num = "{0:D2}" -f $i
    $INPUT_FILE = Join-Path $INPUT_DIR "transfer$num.inp"
    $OUTPUT_FILE = Join-Path $OUTPUT_DIR "transfer$num.bto"
    
    Write-Host "Running test transfer$num..."
    
    Get-Content $INPUT_FILE | python .\BigBank\main.py > $OUTPUT_FILE
}

Write-Host "All transfer tests completed. Check '$OUTPUT_DIR' for results."
