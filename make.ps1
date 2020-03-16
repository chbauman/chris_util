# Parameter definition
param(
[switch]$docs = $false,
[switch]$no_rebuild = $false)


# Aborts script if previous command failed
Function make_docs ($rebuild = $true) {
    Set-Location docs
    if ($rebuild) {
        Remove-Item sphinx -Force -Recurse
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

if ($docs){
    make_docs(-Not $no_rebuild)
}