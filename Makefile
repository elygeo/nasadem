MAKEFLAGS += --warn-undefined-variables
SHELL := bash

.DELETE_ON_ERROR:
.SECONDARY:
.SUFFIXES:
.PHONY: format check clean

format:
	black *.py

check:
	flake8 *.py

clean:
	/bin/rm tmp/*
