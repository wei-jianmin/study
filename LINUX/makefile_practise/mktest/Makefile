.PHONY : all

all : clear a.lib

clear :
	@echo "clear"
	@if [ -e a.lib ]; then rm a.lib; fi
#	@if [ -e "*.o" ]; then rm *.o ; fi
#	@if [ -e "a/*.o" ]; then rm a/*.o; fi
#	@if [ -e "a/b/*.o" ]; then rm a/b/*.o; fi
#	@if [ -e "a/b/c/*.o" ]; then rm a/b/c/*.o; fi
	@for ff in `find ./ -name "*.o"`; do rm $$ff; done

%.o : %.c
	@echo "gcc -c $@ $<"
	@gcc -c $< -o $@

a/%.o : a/%.c
	@echo "gcc -c $@ $<"
	@gcc -c $< -o $@

a/b/%.o : a/b/%.c
	@echo "gcc -c $@ $<"
	@gcc -c $< -o $@

a/b/c/%.o : a/b/c/%.c
	@echo "gcc -c $@ $<"
	@gcc -c $< -o $@

OBJS:=$(subst .c,.o,$(wildcard *.c))
$(info "OBJS=$(OBJS)")
#a.lib : $(OBJS)
#	@echo "ar rus $@ $^"
#	@ar rus $@ $^
a.lib : a.o b.o c.o a/y.o
	@echo "ar rus $@ $^"
	@ar rus $@ $^

#a/b/c/%.o : a/b/c/%.c
#	@echo "------gcc"
#	gcc -c $< -o $@
#
#a.lib : a/y.o a/b/c/%.o
#	@echo "------ar"
#	ar rus $@ $^
#
