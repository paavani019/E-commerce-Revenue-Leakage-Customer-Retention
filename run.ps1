param(
  [ValidateSet("setup","run")]
  [string]$Task = "run"
)

$ErrorActionPreference = "Stop"

if ($Task -eq "setup") {
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  pip install -r requirements.txt
  python .\scripts\unpack_data.py
  Write-Host "Setup complete. Run: .\run.ps1 -Task run"
  exit 0
}

.\.venv\Scripts\Activate.ps1
python .\main.py

