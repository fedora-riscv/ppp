# Makefile for source rpm: ppp
# $Id$
NAME := ppp
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
