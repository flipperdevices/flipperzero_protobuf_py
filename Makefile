

# E201 whitespace after '['
# E202 whitespace before ']'
# E302 expected 2 blank lines, found 1
# E303 too many blank lines
# E501 line too long
# E741 ambiguous variable name

# PEP8=pep8
PYCODESTYLE=pycodestyle
PEP8ARG=--ignore=E501 --exclude=flipperzero_protobuf_compiled

FILES=flipperzero_protobuf/__init__.py \
	flipperzero_protobuf/flipper_base.py flipperzero_protobuf/flipper_proto.py flipperzero_protobuf/cli_helpers.py \
	flipperzero_protobuf/flipper_gpio.py flipperzero_protobuf/flipper_storage.py flipperzero_protobuf/flipper_app.py \
	flipperzero_protobuf/flipper_gui.py flipperzero_protobuf/flipper_sys.py \
	flipperzero_protobuf/flipperCmd.py flipperzero_protobuf/flipperzero_cmd.py 


all:
	@echo "Makefile targets: build clean pylint pip8"

lint: pylint

# Linting / Code Qual check
# pylint --load-plugins perflint  $$targ  ;

pylint:
	for targ in ${FILES} ; do \
		echo $$targ ; \
		pylint $$targ  ; \
	done


pep8: pycodestyle

pycodestyle:
	${PYCODESTYLE} ${PEP8ARG} flipperzero_protobuf
	

clean:
	/bin/rm -fr dist __pycache__ \
		flipperzero_protobuf.egg-info  \
		flipperzero_protobuf/__pycache__ \
		flipperzero_protobuf/flipperzero_protobuf_compiled/__pycache__

	$(if $(wildcard run_local), /bin/bash run_local $@)

build:
	python3 -m build 
	$(if $(wildcard run_local), /bin/bash run_local $@)
