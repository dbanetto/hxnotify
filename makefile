CC:=gcc
OUT:=hxnotify.so
SRC:=src/notify.c
OBJDIR:=obj/
OBJ:=$(patsubst src/%,$(OBJDIR)%.o,$(SRC))
PKG:=`pkg-config --cflags --libs libnotify`
CFLAGS:=-export-dynamic -Wall -g1 -shared -fPIC $(PKG) -std=c11

%.c.o: $(SRC) $(OBJDIR)
	$(CC) -c -o $@ $< $(CFLAGS)

$(OUT): $(OBJ)
	$(CC) $(CFLAGS) $^ -o $(OUT)

.PHONEY: $(OBJDIR)
.PHONEY: clean

$(OBJDIR):
	@mkdir -p $(OBJDIR)

clean:
	rm -rf $(OBJDIR) $(OUT)

install: $(OUT)
	cp -f $(PWD)/$(OUT) $(HOME)/.config/hexchat/addons/$(OUT)

install-link: $(OUT)
	ln -s $(PWD)/$(OUT) $(HOME)/.config/hexchat/addons/$(OUT)
