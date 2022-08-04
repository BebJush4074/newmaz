#! /bin/bash
if [ ! -d "./venv" ]
then
	python3 -m venv venv
fi
. ./venv/bin/activate
pip install maturin
pip install -r requirements.txt
cd ./rustmaz
cargo build -r
maturin develop --release
cd ..
python3 pysideapp.py