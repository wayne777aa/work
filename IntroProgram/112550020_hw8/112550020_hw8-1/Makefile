# 定義編譯器
CC = gcc

# 定義編譯器參數
CFLAGS = -Wall -g

# 定義目標執行檔名稱
TARGET = webhistory

# 定義 obj 檔案的目錄
OBJDIR = obj

# 定義所有的 .o 文件
OBJS = $(addprefix $(OBJDIR)/, main.o browser.o webpage.o webpage_stack.o)

# 默認目標
all: $(TARGET)

# 規則：如何從 .o 文件創建目標執行檔
$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) -o $(TARGET) $(OBJS)

# 依賴關係
$(OBJDIR)/main.o: main.c browser.h webpage.h webpage_stack.h
	@mkdir -p $(OBJDIR)
	$(CC) $(CFLAGS) -c main.c -o $(OBJDIR)/main.o

$(OBJDIR)/browser.o: browser.c browser.h
	@mkdir -p $(OBJDIR)
	$(CC) $(CFLAGS) -c browser.c -o $(OBJDIR)/browser.o

$(OBJDIR)/webpage.o: webpage.c webpage.h
	@mkdir -p $(OBJDIR)
	$(CC) $(CFLAGS) -c webpage.c -o $(OBJDIR)/webpage.o

$(OBJDIR)/webpage_stack.o: webpage_stack.c webpage_stack.h
	@mkdir -p $(OBJDIR)
	$(CC) $(CFLAGS) -c webpage_stack.c -o $(OBJDIR)/webpage_stack.o

# 清理規則
clean:
	rm -f $(TARGET) $(OBJS)
	rmdir $(OBJDIR)

run: all
	 ./$(TARGET)