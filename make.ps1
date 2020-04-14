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
[switch]$install = $false,
[switch]$h = $false)


# Builds the documentation. Use `rebuild` = true, if a module has been
# added, or conf.py changed.
function make_docs ($rebuild = $true) {
    Set-Location docs
    if ($rebuild) {
        Remove-Item sphinx -Force -Recurse -ErrorAction Ignore
        mkdir sphinx
        Set-Location sphinx
        sphinx-apidoc -F -H 'Emeki' -A 'Chris' -o . '../../' "../../setup.py"
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

# Runs the tests using pytest
function run{
    activate_env
    python .\emeki\main.py
}

# Sets up the virtual env and installs required libraries
function setup_venv{
    python -m venv venv
    activate_env
    pip install black flake8 pytest-cov sphinx sphinx-rtd-theme sphinx_autodoc_typehints sphinx-argparse setuptools wheel keyring
    pip install -r requirements.txt
}

# Activates the environment
function activate_env {
    venv/Scripts/activate.ps1
}


# Runs the tests using pytest
function run_tests ($abort = $false) {
    activate_env
    pytest tests --cov=emeki --cov-report html -v
    if ($abort){
        abort_failure
    }
}

# Publish changes to PyPI. Checks if the tests are run successfully
# and if the code formatting is fine.
function publish_to_pypi {
    # Remove old stuff
    Remove-Item dist -Recurse -ErrorAction Ignore
    Remove-Item build -Recurse -ErrorAction Ignore
    Remove-Item *.egg-info -Recurse -ErrorAction Ignore

    # Check formatting and style
    black --check . --exclude venv
    abort_failure
    flake8 tests --max-line-length=90
    abort_failure
    flake8 emeki --max-line-length=90 --exclude emeki/template
    abort_failure

    # Run tests
    venv/Scripts/activate.ps1
    run_tests($true)
    venv/Scripts/activate.ps1

    # Handle version
    $version = ((Get-Content -Path version.txt) | Out-String).Trim()
    Write-Host("Previous version is: $version")
    $new_vers = Read-Host -Prompt 'New version'
    $new_vers | Set-Content 'version.txt'

    # Upload to PyPI
    python setup.py sdist bdist_wheel
    $username = "chbauman"
    $pw = (keyring get https://upload.pypi.org/legacy/ $username) | Out-String
    if($to_pypi){
        twine upload dist/* -u $username -p $pw.Trim()
    } else {
        twine upload dist/* --repository-url https://test.pypi.org/legacy/ -u $username -p $pw.Trim()
    }
}

# Cleans up some files
function clean {
    Remove-Item build -Force -Recurse -ErrorAction Ignore
    Remove-Item dist -Force -Recurse -ErrorAction Ignore
    Remove-Item emeki.egg-info -Force -Recurse -ErrorAction Ignore
    Remove-Item *__pycache__* -Force -Recurse -ErrorAction Ignore
    Remove-Item docs/sphinx -Force -Recurse -ErrorAction Ignore
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
    black .  --exclude venv
    flake8 tests --max-line-length=90
    flake8 emeki --max-line-length=90
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
if ($install) {
    setup_venv
}
