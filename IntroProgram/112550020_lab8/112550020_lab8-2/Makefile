CC=gcc
EXE=main
OBJDIR=obj
OBJ=$(addprefix $(OBJDIR)/, stack.o custom_assert.o $(EXE).o)

$(OBJDIR)/%.o: %.c
	@mkdir -p $(OBJDIR)
	@$(CC) -c $< -o $@

all: $(OBJ)
	 $(CC) $(OBJ) -o $(EXE)

run: all
	 ./$(EXE)

debug: CC += -DDEBUG -g
debug: all
.PHONY: debug

clean:
	rm -f $(OBJDIR)/*.o $(EXE)
	rmdir $(OBJDIR)
.PHONY: clean