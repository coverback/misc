# Name all the source files here
# If you even add a new source file to the project, make sure you add it here too
SOURCES   := main.cpp

# Filename of the actual executable file
TARGET    := executable_name

# Generate list of object files. .o is added instead of files' normal
# suffixes, like .cc or .cpp. Each source file will be compiled into
# according object file before linking.
_OBJS     := $(addsuffix .o,$(basename $(SOURCES)))

# Object files should be kept in hidden subfolder
OBJDIR    := .obj
# Add folder name in front of every object filename
OBJS      := $(_OBJS:%=$(OBJDIR)/%)

# Name of the used compiler
CXX       := g++

# Debug symbols for using with gdb. Can be commented out
# to save executable size (and maybe compilation time?)
DEBUG     := -g

# Compilation and include flags
# Use our include-dir first and then specify other dirs in IFLAGS.
IDIR      := include
IFLAGS    := -I./$(IDIR)
CFLAGS    := -Wall -Wextra $(DEBUG) $(IFLAGS)

# Linking flags and variables for some libs used in linking.
# pkg-config returns all related libs which library installation has
# provided in a pkg file lib_name.pc in /usr/lib/pkgconfig or similar.
# This way is significantly more reliable than manually adding libs.
# If pkgconfig file are not provided, add -lname to LIBS.
LIBS      :=
LIBCONFIG := $(shell pkg-config --libs lib_name)
LDFLAGS   := $(LIBS) $(LIBCONFIG)


################### targets ######################

# This first target is the one which is executed by default.
# It is a mere alias for a target with a same name as our executable.
all: $(TARGET)

# This target is designed to create dependencies for source files.
# For each .o file there is a .d file, naming all .cpp and header files
# the object file depends on. These files are generated using
#    gcc -MM
# command. Horrible lines below parse the gcc output to suit Makefile
# needs more correctly. @ in front surpresses the output.
$(OBJDIR)/%.d: %.cpp
	@set -e; rm -f $@; \
	 $(CXX) -MM $(CFLAGS) $< > $@.$$$$; \
	 sed 's,\($*\)\.o[ :]*,$(OBJDIR)\/\1.o $@: ,g' < $@.$$$$ > $@; \
	 rm -f $@.$$$$

# Include all generated .d files so that this Makefile is aware of
# all the dependencies. Hyphen make make ignore errors.
-include $(OBJS:.o=.d)

# This next rule is applied to every object file target
# that come from $(OBJS) list.
# Each object file depends on according .cpp file and a .d makefile,
# that means the once .cpp gets changed, according object file is rebuilt,
# and once any of the headers the cpp file depends on is changed, object file
# is also rebuilt. Dependencies are stored in .d files.
#    %  gets assigned a matched part of a target name, a basename
#    $@ is current target name
#    $< the name of the first dependency (.cpp file in our case)
$(OBJDIR)/%.o: %.cpp $(OBJDIR)/%.d
	$(CXX) $(CFLAGS) -o $@ -c $<

# Objects order-depend on object directory.
# Pipe means no object files must be rebuilt if directory timestamp changes
$(OBJS): | $(OBJDIR)

# This will create a directory if none is present
$(OBJDIR):
	mkdir $(OBJDIR)

# Depend on all object files. Once they're done, link everything and
# create a target executable.
$(TARGET): $(OBJS)
	$(CXX) $(LDFLAGS) $(OBJS) -o $(TARGET)

# Clean target deletes executable and all generated object files.
# PHONY target is used to make sure clean rule doesn't break in case there's
# a 'clean' file in current directory.
# - before rm means ignore errors
.PHONY: clean
clean:
	-rm $(TARGET) $(OBJS)
	-rm $(OBJDIR)/*.d

