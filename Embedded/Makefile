TARGET := /Users/yury/workspaces/git/msp430_delta_robot/Embedded/bin/main

ifndef ENERGIADIR
ENERGIADIR := $(firstword $(wildcard ~/energia /usr/share/energia /Applications/Energia.app/Contents/Resources/Java))
endif
ifeq "$(wildcard $(ENERGIADIR)/hardware/msp430/boards.txt)" ""
$(error ENERGIADIR is not set correctly; energia software not found)
endif

COMPILER_PREFIX =$(ENERGIADIR)/hardware/tools/msp430/bin
MSPDEBUG := $(COMPILER_PREFIX)/../mspdebug/mspdebug
MSPOBJCOPY = /Applications/Energia.app/Contents/Resources/Java/hardware/tools/msp430/bin/msp430-objcopy
MSPDEBUG_PROTOCOL:= rf2500
MSPDEBUG_LD:=
MSPDEBUGFLAGS :=  $(MSPDEBUG_PROTOCOL) 'erase' 'load $(TARGET).elf' 'exit'

all: 
	mkdir -p build
	cd build ; cmake .. -DCMAKE_TOOLCHAIN_FILE=../../cmake/msp430.cmake && make
target: all $(TARGET)
	 $(MSPOBJCOPY) -O ihex -R .eeprom $(TARGET) $(TARGET).elf
	
upload: target
	@echo "\nUploading to board..."
	$(MSPDEBUG_LD) $(MSPDEBUG) $(MSPDEBUGFLAGS)
	
debug:
	@echo $(MSPDEBUG) $(MSPDEBUG_PROTOCOL) gdb
	$(MSPDEBUG) $(MSPDEBUG_PROTOCOL) gdb
#	cgdb  -d $(GDB) $(TARGET).elf
clean:
	rm -rf build 
	rm -rf bin
