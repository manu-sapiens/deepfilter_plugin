if exist ".\venv" (

	call .\venv\Scripts\activate
	python -m ensurepip --upgrade
	python -m pip install --upgrade "pip>=22.3.1,<23.1.*"


	python -m pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu116
	python -m pip install soundfile
	python -m pip install -r requirements.txt

	git clone https://github.com/Rikorose/DeepFilterNet.git

	pushd DeepFilterNet
	cd DeepFilterNet
	python -m pip install .
	popd
)
pause