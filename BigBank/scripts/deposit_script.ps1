# run_deposits.ps1

# Directories 
$INPUT_DIR = ".\transaction terminal (input)\deposit"
$OUTPUT_DIR = ".\transaction terminal (output)\deposit"

# Create the output directory if it doesn't exist
if (!(Test-Path $OUTPUT_DIR)) {
    New-Item -ItemType Directory -Path $OUTPUT_DIR | Out-Null
} else {
    Remove-Item "$OUTPUT_DIR\*" -Force -Recurse
}

# Loop through deposit test files deposit01.txt through deposit12.txt
for ($i = 1; $i -le 11; $i++) {
    $num = "{0:D2}" -f $i
    $INPUT_FILE = Join-Path $INPUT_DIR "deposit$num.inp"
    $OUTPUT_FILE = Join-Path $OUTPUT_DIR "deposit$num.out"
    
    Write-Host "Running test deposit$num..."

    Get-Content $INPUT_FILE | python ./main.py > $OUTPUT_FILE
}

Write-Host "All deposit tests completed. Check '$OUTPUT_DIR' for results."
