.PHONY: env
env:
	mamba env create -f environment.yml -p ~/envs/ligo2
	bash -ic 'conda activate ligo;python -m ipykernel install --user --name ligo2 --display-name "IPython - ligo2"'

.PHONY: html
html:
	jupyter-book build ~/hw/hw06-isaacdsloan/

.PHONY: html-hub
html-hub:
	jupyter-book config sphinx ~/hw/hw06-isaacdsloan/
	sphinx-build  ~/hw/hw06-isaacdsloan/ _build/html -D html_baseurl=${JUPYTERHUB_SERVICE_PREFIX}/proxy/absolute/8000
	cd ~/hw/hw06-isaacdsloan/_build/html


.PHONY : clean
clean :
	rm -f figures/*.png
	rm -f data/*.csv
	rm -f audio/*.wav