# Parameter definition
param(
[switch]$docs = $false,
[switch]$run = $false,
[switch]$act = $false,
[switch]$no_rebuild = $false,
[switch]$format = $false,
[switch]$clean = $false,
[switch]$test = $false,
[switch]$pub = $false,
[switch]$to_pypi = $false,
[switch]$h = $false)


# Builds the documentation. Use `rebuild` = true, if a module has been
# added, or conf.py changed.
function make_docs ($rebuild = $true) {
    Set-Location docs
    if ($rebuild) {
        Remove-Item sphinx -Force -Recurse -ErrorAction Ignore
        mkdir sphinx
        Set-Location sphinx
        sphinx-apidoc -F -H 'PROJECT_NAME' -A 'AUTHOR' -o . '../../' "../../setup.py"
        Copy-Item ../conf.py .
        Set-Location ..
        python doc_helper.py
    }
    Set-Location sphinx
    ./make html SPHINXBUILD='python $(shell which sphinx-build)'
    Set-Location ../..
}

# Aborts script if previous command failed
function abort_failure {
    if (-Not $?) {
        Write-Host("ERROR: Publishing failed!")
        Break
    }
}

# Runs the main function
function run{
    activate_env
    python .\PROJECT_NAME_UNS\main.py
}

# Runs the tests using pytest
function activate_env {
    venv/Scripts/activate.ps1
}


# Runs the tests using pytest
function run_tests ($abort = $false) {
    activate_env
    pytest tests --cov=PROJECT_NAME_UNS --cov-report html -v
    if ($abort){
        abort_failure
    }
    deactivate
}

# Publish changes to PyPI. Checks if the tests are run successfully
# and if the code formatting is fine.
function publish_to_pypi {
    # Remove old stuff
    Remove-Item dist -Recurse -ErrorAction Ignore
    Remove-Item build -Recurse -ErrorAction Ignore
    Remove-Item *.egg-info -Recurse -ErrorAction Ignore

    # Check formatting and style
    black --check .
    abort_failure
    flake8 tests --max-line-length=90
    abort_failure
    flake8 PROJECT_NAME_UNS --max-line-length=90
    abort_failure

    # Run tests
    venv/Scripts/activate.ps1
    run_tests($true)

    # Handle version
    $version = ((Get-Content -Path version.txt) | Out-String).Trim()
    Write-Host("Previous version is: $version")
    $new_vers = Read-Host -Prompt 'New version'
    $new_vers | Set-Content 'version.txt'

    # Upload to PyPI
    python setup.py sdist bdist_wheel
    $username = "pypi_username"
    $pw = (keyring get https://upload.pypi.org/legacy/ $username) | Out-String
    if($to_pypi){
        twine upload dist/* -u $username -p $pw.Trim()
    } else {
        twine upload dist/* --repository-url https://test.pypi.org/legacy/ -u $username -p $pw.Trim()
    }
}

# Cleans up some files
function clean {
    Remove-Item docs/sphinx -Force -Recurse -ErrorAction Ignore
    Remove-Item htmlcov -Force -Recurse -ErrorAction Ignore
    Remove-Item .coverage -Force -Recurse -ErrorAction Ignore
    Remove-Item Info.txt -Recurse -ErrorAction Ignore
    Remove-Item .pytest_cache -Force -Recurse -ErrorAction Ignore
    get-childitem -Include *__pycache__* -Recurse -force | Remove-Item -Force -Recurse
    Remove-Item dist -Recurse -ErrorAction Ignore
    Remove-Item build -Recurse -ErrorAction Ignore
    Remove-Item *.egg-info -Recurse -ErrorAction Ignore
}

# Do the actual stuff
if ($h) {
    Get-Help .\make.ps1
}
if ($docs) {
    make_docs(-Not $no_rebuild)
}
if ($run) {
    run
}
if ($pub) {
    publish_to_pypi
}
if ($format) {
    black .
    flake8 tests --max-line-length=90
    flake8 PROJECT_NAME_UNS --max-line-length=90
}
if ($clean) {
    clean
}
if ($act) {
    activate_env
}
if ($test) {
    run_tests
}
