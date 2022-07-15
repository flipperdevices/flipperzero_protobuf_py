


FILES=flipperzero_protobuf/__init__.py \
	flipperzero_protobuf/flipper_base.py flipperzero_protobuf/flipper_proto.py flipperzero_protobuf/cli_helpers.py \
	flipperzero_protobuf/flipper_gpio.py flipperzero_protobuf/flipper_storage.py flipperzero_protobuf/flipper_app.py \
	flipperzero_protobuf/flipper_gui.py flipperzero_protobuf/flipper_sys.py \
	flipperzero_protobuf/flipperzero_cmd.py 


all: pylint

pylint:
	for targ in ${FILES} ; do \
		echo $$targ ; \
		@pylint $$targ  ; \
	done

# python -m py_compile $$targ ; \

clean:
	/bin/rm -fr flipperzero_protobuf.egg-info dist flipperzero_protobuf/__pycache__ flipperzero_protobuf/flipperzero_protobuf_compiled/__pycache__

build:
	python3 -m build
