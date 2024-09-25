# Script to automatically compile latex files, prune log files, open compiled pdf. 

```ps1
param (
    [string]$fileName = 'main.tex'
)

# Check if the file exists
if (-Not (Test-Path $fileName)) {
    Write-Host "File '$fileName' does not exist."
    exit 1
}

echo $fileName

# Extract the base name (without extension) from the file name
$baseName = [System.IO.Path]::GetFileNameWithoutExtension($fileName)

# Compile the LaTeX file using pdflatex
Write-Host "Compiling LaTeX file..."
& pdflatex -interaction=nonstopmode $fileName > nul

# Run biblatex for references
Write-Host "Running biblatex..."
# & biber $baseName
& bibtex $baseName

# Compile the LaTeX file again (twice) to ensure references are updated
Write-Host "Finalizing compilation..."
& pdflatex -interaction=nonstopmode $fileName > nul
& pdflatex -interaction=nonstopmode -synctex=1 $fileName > nul

# Delete auxiliary files
$auxFiles = @("$baseName.aux", "$baseName.log", "$baseName.out", "$baseName.bbl", "$baseName.blg")
foreach ($file in $auxFiles) {
    if (Test-Path $file) {
        Remove-Item $file
        Write-Host "Deleted $file"
    }
}
# rm *.log

Write-Host "Compilation finished. PDF generated as '$baseName.pdf'."

ii "$baseName.pdf"
```

## Setting up Sumatra for inverse search
```
vim +%l "%f"
```
