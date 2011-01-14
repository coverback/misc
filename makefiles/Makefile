# Name all the source files here
# If you even add a new source file to the project, make sure you add it here too
SOURCES  = analysis.cpp capture.cpp main.cpp presentation.cpp

# List all header files here. Don't include folder path, folder is named separately
_HEADERS = analysis.hpp capture.hpp presentation.hpp
IDIR     = include

# Prepend all header files with their directory name
HEADERS  = $(patsubst %, $(IDIR)/%, $(_HEADERS))

# Filename of the actual executable file
TARGET   = iwb

# Generate list of object files. .o is added instead of files' normal
# suffixes, like .cc or .cpp. Each source file will be compiled into
# according object file before linking.
_OBJS  = $(addsuffix .o, $(basename $(SOURCES)))

# Object files should be kept in hidden subfolder
OBJDIR = .obj
# Add folder name in front of every object filename
OBJS   = $(patsubst %, $(OBJDIR)/%, $(_OBJS))

# Name of the used compiler
CXX    = g++

# Debug symbols for using with e.g. gdb. Can be commented out
# to save executable size (and maybe compilation time?)
DEBUG  = -g

# Compilation and include flags
# Use our include-dir first and then specify other dirs.
# Note, there is no need to include opencv folders, as all files
# should use <opencv2/filename.h> format relative to /usr/include
IFLAGS    = -I./$(IDIR)
CFLAGS    = -Wall -Wextra $(DEBUG) $(IFLAGS)

# Linking flags and variables for some libs used in linking
# pkg-config returns all opencv libs which opencv installatoion has
# provided in a pkg file opencv.pc in /usr/lib/pkgconfig or similar.
# This way is significantly more reliable than manually adding libs.
LIBS      =
LIBCONFIG = $(shell pkg-config --libs opencv)
LFLAGS    = $(LIBS) $(LIBCONFIG)


################### targets ######################

# This first target is the one which is executed by default.
# It is a mere alias for a target with a same name as our executable.
all: $(TARGET)

# This next rule is applied to every object file target
# that come from $(OBJS) list.
# Each object file depends on according .cpp file and ALL header files,
# that means the once .cpp gets changed, according object file is rebuilt,
# and if any header files is changed, all object files are rebuilt to
# avoid missing an interface change of some classes or functions.
#    %  gets assigned a matched part of a target name, a basename
#    $@ is current target name
#    $< the name of the first dependency (.cpp file in our case)
$(OBJDIR)/%.o: %.cpp $(HEADERS)
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
	$(CXX) $(LFLAGS) $(OBJS) -o $(TARGET)

# Clean target deletes executable and all generated object files.
# PHONY target is used to make sure clean rule doesn't break in case there's
# a 'clean' file in current directory.
.PHONY: clean
clean:
	rm $(TARGET) $(OBJS)

