# run_delete.ps1

# Directories
$INPUT_DIR = ".\delete\transaction_terminal_input"
$OUTPUT_DIR = ".\delete\transaction_terminal_output"

# delete the output directory if it doesn't exist
if (!(Test-Path $OUTPUT_DIR)) {
    New-Item -ItemType Directory -Path $OUTPUT_DIR | Out-Null
} else {
    Remove-Item "$OUTPUT_DIR\*" -Force -Recurse
}

# Loop through delete test files delete01.txt through delete11.txt
for ($i = 1; $i -le 11; $i++) {
    $num = "{0:D2}" -f $i
    $INPUT_FILE = Join-Path $INPUT_DIR "delete$num.inp"
    $OUTPUT_FILE = Join-Path $OUTPUT_DIR "delete$num.bto"
    
    Write-Host "Running test delete$num..."
    
    Get-Content $INPUT_FILE | python .\BigBank\main.py > $OUTPUT_FILE
}

Write-Host "All delete tests completed. Check '$OUTPUT_DIR' for results."
