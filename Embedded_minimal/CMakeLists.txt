project(msp430_delta_robot)
cmake_minimum_required(VERSION 2.8)

# Configuration
# =============
#

#defines where static libraries are stored
SET(LIBRARY_OUTPUT_PATH ${CMAKE_HOME_DIRECTORY}/lib)

#defines where the executables are stored
SET(EXECUTABLE_OUTPUT_PATH ${CMAKE_HOME_DIRECTORY}/bin)

#defines where dynamic libraries (plugins) are stored
SET (CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_HOME_DIRECTORY}/bin)

# stuff to make eclipse work correctly with error parsing
IF(CMAKE_COMPILER_IS_GNUCC)
  SET(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -fmessage-length=0")
ENDIF(CMAKE_COMPILER_IS_GNUCC)
IF(CMAKE_COMPILER_IS_GNUCXX)
  SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fmessage-length=0")
ENDIF(CMAKE_COMPILER_IS_GNUCXX)
# end of eclipse stuff
# set out dicovery
SET(CMAKE_VERBOSE_MAKEFILE ON)
# frequenecy is 2^20 =1048576
set(CONF_FREQUENCY_IN_HZ "1000000UL" CACHE STRING "CPU frequency used")
#set(CMAKE_TOOLCHAIN_FILE ${CMAKE_CURRENT_SOURCE_DIR}/cmake/msp430.cmake)
# Compiler Settings
add_definitions("-DF_CPU=${CONF_FREQUENCY_IN_HZ}")
set(ENERGIA_PATH /Applications/Energia.app/Contents/Resources/Java/hardware/)
set(MSP430_CORE_DIR ${ENERGIA_PATH}msp430/cores/msp430)

include_directories(${ENERGIA_PATH}msp430/cores/msp430)
include_directories(${ENERGIA_PATH}msp430/variants/launchpad)
include_directories(${ENERGIA_PATH}tools/msp430/msp430/include)


message(STATUS "MSP430_CORE_DIR '${MSP430_CORE_DIR}'")
#FILE(GLOB_RECURSE MSP430_CORE_SOURCE RELATIVE ${MSP430_CORE_DIR} "*.cpp" )
aux_source_directory(${MSP430_CORE_DIR} MSP430_CORE_SOURCE)
message(STATUS "main '${MSP430_CORE_DIR}'main.cpp")
list(REMOVE_ITEM MSP430_CORE_SOURCE ${MSP430_CORE_DIR}/main.cpp)
message(STATUS "MSP430_CORE_SOURCE '${MSP430_CORE_SOURCE}'")
add_library(msp430_core STATIC  ${MSP430_CORE_SOURCE})


include_directories(${CMAKE_HOME_DIRECTORY})

# NRF24NetworkingModule
#include_directories(${CMAKE_CURRENT_SOURCE_DIR}/msp430lib/include)
add_executable(main 
    main.cpp
	PWMServo.cpp
)

target_link_libraries(
  main
  msp430_core
)