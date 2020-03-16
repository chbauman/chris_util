
Set-Location docs
Remove-Item sphinx -Force -Recurse
mkdir sphinx
Set-Location sphinx
sphinx-apidoc -F -H 'Emeki' -A 'Chris' -o . '../../' "../../setup.py"
Copy-Item ../conf.py .
Set-Location ..
python doc_helper.py
Set-Location sphinx
./make html SPHINXBUILD='python $(shell which sphinx-build)'
Set-Location ../..