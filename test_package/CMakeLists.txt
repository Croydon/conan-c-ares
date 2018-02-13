project(cares_test)
cmake_minimum_required(VERSION 3.2.1)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

set(CARES_TESTS_COMMON ares_strcasecmp.c ares_nowarn.c ares_getopt.c ares_search.c ares_gethostbyname.c ares_init.c)

#set(CARES_USE_STATIC TRUE)
find_package (CARES REQUIRED)
include_directories(${CARES_INCLUDE_DIRS})
add_definitions(${CARES_DEFINITIONS})
add_executable(ahost ahost.c ${CARES_TESTS_COMMON})

target_link_libraries(ahost ${CARES_LIBRARIES})
if(WIN32)
  target_link_libraries(ahost wsock32)
endif()
