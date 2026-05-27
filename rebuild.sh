cd package
set PYTHONUTF8=1
python -m pip uninstall cmake-init -y  
python -m pip install -e .
cd ..