

# E303 : too many blank lines
# E302 : expected 2 blank lines, found 1
# E201 whitespace after '['
# E202 whitespace before ']'
# E501 line too long

# E203,E201,E202,E501
PEP8=pep8
PEP8ARG=--ignore=E303,E302,E201,E202,E501 --exclude=flipperzero_protobuf_compiled

FILES=flipperzero_protobuf/__init__.py \
	flipperzero_protobuf/flipper_base.py flipperzero_protobuf/flipper_proto.py flipperzero_protobuf/cli_helpers.py \
	flipperzero_protobuf/flipper_gpio.py flipperzero_protobuf/flipper_storage.py flipperzero_protobuf/flipper_app.py \
	flipperzero_protobuf/flipper_gui.py flipperzero_protobuf/flipper_sys.py \
	flipperzero_protobuf/flipperzero_cmd.py 


pep8 --ignore=E203,E201,E202,E501 --exclude=flipperzero_protobuf_compiled  flipperzero_protobuf/

all:
	@echo "Makefile targets: build clean pylint"

pylint:
	for targ in ${FILES} ; do \
		echo $$targ ; \
		pylint $$targ  ; \
	done



pep8:
	${PEP8} ${PEP8ARG} flipperzero_protobuf
	

clean:
	/bin/rm -fr flipperzero_protobuf.egg-info dist flipperzero_protobuf/__pycache__ flipperzero_protobuf/flipperzero_protobuf_compiled/__pycache__

build:
	python3 -m build 
