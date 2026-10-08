ASM = nasm
ASMFLAGS = -f elf64

CC = gcc
LDFLAGS = -no-pie

TARGET = average
SOURCE = main.asm
OBJECT = main.o
INPUTFILE = data.txt

.PHONY: all run clean

all: $(TARGET)

$(TARGET): $(OBJECT)
	$(CC) $(LDFLAGS) $(OBJECT) -o $(TARGET)

$(OBJECT): $(SOURCE)
	$(ASM) $(ASMFLAGS) $(SOURCE) -o $(OBJECT)

run: $(TARGET)
	./$(TARGET) $(INPUTFILE)

clean:
	rm -f $(OBJECT) $(TARGET)
