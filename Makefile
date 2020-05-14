.PHONY: build clean help install uninstall test upload-test wheel_check
.SILENT: help install uninstall test wheel_check

define HELP

Targets:

  - build      - builds the 'wheel' distribution file (calls clean)
  - clean      - cleans temporary files
  - install    - builds and locally installs to your interpreter (calls uninstall and build)
  - uninstall  - removes locally installed copy
  - test       - runs unit tests

endef

export HELP
help:
	echo "$${HELP}"
	false

build: wheel_check clean
	python3 setup.py sdist bdist_wheel

clean:
	rm -rf build dist *.egg-info __pycache__

install: build uninstall
	pip3 install --user ./dist/sd_notify-*.whl

uninstall:
	-pip3 uninstall -y sd_notify

test:
	./test_sd_notify.py

upload-test:
	python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

WHEEL_INSTALLED = $(shell pip3 list | egrep '^wheel\s')
wheel_check:
ifeq ($(WHEEL_INSTALLED),)
  $(error Need to 'pip3 install wheel')
endif
	true
