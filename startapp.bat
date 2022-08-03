IF EXIST venv (
echo ""
) else (
python -m venv venv
)
call venv\Scripts\activate.bat
pip install maturin
pip install -r requirements.txt
cd .\rustmaz
maturin develop --release
cd ..
python pysideapp.py