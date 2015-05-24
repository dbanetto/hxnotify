CC:=gcc
OUT:=hxnotify.so
SRC:=notify.c
OBJDIR:=obj/
OBJ:=$(patsubst %,$(OBJDIR)%.o,$(SRC))
PKG:=`pkg-config --cflags --libs libnotify`
CFLAGS:=-export-dynamic -Wall -O1 -shared -fPIC $(PKG) -std=c11

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
