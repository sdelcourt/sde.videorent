#!/usr/bin/make
#

options =

all: run

.PHONY: setup
setup:
	virtualenv-2.7 .
	./bin/pip install --upgrade pip
	./bin/pip install -r requirements.txt

.PHONY: buildout
buildout:
	if ! test -f bin/buildout;then make setup;fi
	bin/buildout -vt 60

.PHONY: run
run:
	if ! test -f bin/instance;then make buildout;fi
	bin/instance fg

.PHONY: test_coverage
test_coverage:
	bin/createcoverage

.PHONY: cleanall
cleanall:
	rm -fr bin/instance develop-eggs downloads eggs parts .installed.cfg
