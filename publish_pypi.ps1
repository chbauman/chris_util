
# Aborts script if previous command failed
Function abort_failure {
    if (-Not $?) {
        Write-Host("ERROR: Publishing failed!")
        Break
    }
}

# Check formatting and style
black --check .
abort_failure
flake8 emeki --max-line-length=90
abort_failure
flake8 tests --max-line-length=90
abort_failure

# Run tests
venv/Scripts/activate.ps1
pip install pytest
pytest ./tests
abort_failure
deactivate

# Handle version
$version = ((Get-Content -Path version.txt) | Out-String).Trim()
Write-Host("Previous version is: $version")
$new_vers = Read-Host -Prompt 'New version'
$new_vers | Set-Content 'version.txt'

# Upload to PyPI
python setup.py sdist bdist_wheel
$username = "chbauman"
$pw = (keyring get https://upload.pypi.org/legacy/ $username) | Out-String
twine upload dist/* -u $username -p $pw.Trim()

