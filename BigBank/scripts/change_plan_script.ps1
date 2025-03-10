# run_deposits.ps1

# Directories 
$INPUT_DIR = ".\changeplan\transaction_terminal_input"
$OUTPUT_DIR = ".\changeplan\transaction_terminal_output"

# Create the output directory if it doesn't exist
if (!(Test-Path $OUTPUT_DIR)) {
    New-Item -ItemType Directory -Path $OUTPUT_DIR | Out-Null
} else {
    Remove-Item "$OUTPUT_DIR\*" -Force -Recurse
}

# Loop through deposit test files deposit01.txt through deposit12.txt
for ($i = 1; $i -le 9; $i++) {
    $num = "{0:D2}" -f $i
    $INPUT_FILE = Join-Path $INPUT_DIR "changeplan$num.inp"
    $OUTPUT_FILE = Join-Path $OUTPUT_DIR "changeplan$num.bto"
    
    Write-Host "Running test changeplan$num..."

    Get-Content $INPUT_FILE | python .\BigBank\main.py > $OUTPUT_FILE
}

Write-Host "All changeplan tests completed. Check '$OUTPUT_DIR' for results."