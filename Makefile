

# E201 whitespace after '['
# E202 whitespace before ']'
# E302 expected 2 blank lines, found 1
# E303 too many blank lines
# E501 line too long
# E741 ambiguous variable name

# PEP8=pep8
PYCODESTYLE=pycodestyle
PEP8ARG=--ignore=E501,E128 --exclude=flipperzero_protobuf_compiled

FILES=flipperzero_protobuf/*.py flipperzero_protobuf/flipperCmd/*.py

all:
	@echo "Makefile targets: build clean pylint pip8"

lint: pylint

# Linting / Code Qual check
# pylint --load-plugins perflint  $$targ  ;

pylint:
	pylint flipperzero_protobuf

pylint_each:
	for targ in ${FILES} ; do \
		echo $$targ ; \
		pylint $$targ  ; \
	done


pep8: pycodestyle

pycodestyle:
	${PYCODESTYLE} ${PEP8ARG} flipperzero_protobuf
	

clean:
	/bin/rm -fr dist __pycache__ build \
		flipperzero_protobuf.egg-info  \
		flipperzero_protobuf/__pycache__ \
		flipperzero_protobuf/flipperCmd/__pycache__ \
		flipperzero_protobuf/flipperzero_protobuf_compiled/__pycache__

	$(if $(wildcard run_local), /bin/bash run_local $@)

build:
	python3 -m build 
	$(if $(wildcard run_local), /bin/bash run_local $@)

install:
	pip3 install .
