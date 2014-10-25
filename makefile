CC=gcc
OUTLIB=hxnotify.so
src=notify.c
PKG=`pkg-config --cflags --libs libnotify`
CFLAGS=-export-dynamic -Wall -O1 -shared -fPIC
all: build

build:
	$(CC) $(CFLAGS) $(PKG) $(src) -o $(OUTLIB)
