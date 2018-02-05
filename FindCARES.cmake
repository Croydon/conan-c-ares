find_path(CARES_INCLUDE_DIR NAMES ares.h PATHS ${CONAN_INCLUDE_DIRS_C-ARES})
# This will also look for Ws2_32.lib in Windows, but PATHS are forced, so no problem.
find_library(CARES_LIBRARY NAMES ${CONAN_LIBS_C-ARES} PATHS ${CONAN_LIB_DIRS_C-ARES})

if(NOT EXISTS ${CONAN_BIN_DIRS_C-ARES})
	SET(CARES_DEFINITIONS "-DCARES_STATICLIB")
endif()

MESSAGE("** CARES ALREADY FOUND BY CONAN!")
SET(CARES_FOUND TRUE)
MESSAGE("** CONAN_LIBS_C-ARES:  ${CONAN_LIBS_C-ARES}")
MESSAGE("** CONAN_LIB_DIRS_C-ARES:  ${CONAN_LIB_DIRS_C-ARES}")
MESSAGE("** FOUND CARES:  ${CARES_LIBRARY}")
MESSAGE("** FOUND CARES INCLUDE:  ${CARES_INCLUDE_DIR}")

set(CARES_INCLUDE_DIRS ${CARES_INCLUDE_DIR})
set(CARES_LIBRARIES ${CARES_LIBRARY})

set(CARES_VERSION_STRING "1.13.0")

mark_as_advanced(CARES_LIBRARY CARES_LIBRARIES CARES_INCLUDE_DIR CARES_INCLUDE_DIRS CARES_VERSION_STRING)
