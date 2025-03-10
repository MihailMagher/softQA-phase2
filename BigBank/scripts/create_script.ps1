# run_create.ps1

# Directories
$INPUT_DIR = ".\create\transaction_terminal_input"
$OUTPUT_DIR = ".\create\transaction_terminal_output"

# Create the output directory if it doesn't exist
if (!(Test-Path $OUTPUT_DIR)) {
    New-Item -ItemType Directory -Path $OUTPUT_DIR | Out-Null
} else {
    Remove-Item "$OUTPUT_DIR\*" -Force -Recurse
}

# Loop through create test files create01.txt through create11.txt
for ($i = 1; $i -le 11; $i++) {
    $num = "{0:D2}" -f $i
    $INPUT_FILE = Join-Path $INPUT_DIR "create$num.inp"
    $OUTPUT_FILE = Join-Path $OUTPUT_DIR "create$num.bto"
    
    Write-Host "Running test create$num..."
    
    Get-Content $INPUT_FILE | python .\BigBank\main.py > $OUTPUT_FILE
}

Write-Host "All create tests completed. Check '$OUTPUT_DIR' for results."
