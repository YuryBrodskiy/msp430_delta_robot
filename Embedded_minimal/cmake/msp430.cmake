# TOOLCHAIN FILE for MSP430
#
# Not yet tested with plain C stuff but with C++
#
# Usage:
# cmake .. -DCMAKE_TOOLCHAIN_FILE=../cmake/msp430.cmake

if( DEFINED CMAKE_CROSSCOMPILING )
  # subsequent toolchain loading is not really needed
  return()
endif()



SET(CMAKE_SYSTEM_NAME Generic)
SET(CMAKE_SYSTEM_VERSION 1)
SET(CMAKE_SYSTEM_PROCESSOR msp430g2553)
list( APPEND CMAKE_FIND_ROOT_PATH /opt/local/msp430)
list( APPEND CMAKE_FIND_ROOT_PATH /Applications/Energia.app/Contents/Resources/Java/hardware/tools/msp430/)
message(STATUS "CMAKE_FIND_ROOT_PATH '${CMAKE_FIND_ROOT_PATH}'")

find_program(MSP430_CC msp430-gcc)
find_program(MSP430_CXX msp430-g++)
find_program(MSP430_OBJCOPY msp430-objcopy)
find_program(MSP430_SIZE_TOOL msp430-size)
find_program(MSP430_OBJDUMP msp430-objdump)
find_program(MSPDEBUG mspdebug)

# Compiler & Linker Settings
include(CMakeForceCompiler)
CMAKE_FORCE_C_COMPILER(${MSP430_CC} GNU)
CMAKE_FORCE_CXX_COMPILER(${MSP430_CXX} GNU)

SET(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
SET(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
SET(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)

get_property(_CMAKE_IN_TRY_COMPILE GLOBAL PROPERTY IN_TRY_COMPILE)
if( _CMAKE_IN_TRY_COMPILE )
endif()

if(NOT MCU)
  message(STATUS "Setting default MCU type 'msp430g2553'")
  set(MCU "msp430g2553" CACHE STRING "MSP430 MCU TYPE")
else()
  message(STATUS "MCU defined as '${MCU}'")
endif()

message(STATUS "CMAKE_CXX_FLAGS original '${CMAKE_CXX_FLAGS}'")
message(STATUS "CMAKE_CXX_LINK_FLAGS original '${CMAKE_CXX_LINK_FLAGS}'")
set(CMAKE_CXX_FLAGS " -Wall -mmcu=${MCU} -Os -g -ffunction-sections -fdata-sections" CACHE STRING "C++ Flags")
set(CMAKE_CXX_LINK_FLAGS "-0s, -Wl,-gc-sections" CACHE STRING "Linker Flags")

set(CMAKE_C_FLAGS " -Wall  -mmcu=${MCU} -Os -g -ffunction-sections -fdata-sections" CACHE STRING "C Flags")
set(CMAKE_C_LINK_FLAGS "-Wl,-gc-sections" CACHE STRING "Linker Flags")

# Use GCC for linking executables to avoid linking to stdlibc++ _BUT_ get all the math libraries etc.
set(CMAKE_CXX_LINK_EXECUTABLE
  "<CMAKE_C_COMPILER> <FLAGS> <CMAKE_CXX_LINK_FLAGS> <LINK_FLAGS> <OBJECTS> -o <TARGET> ${CMAKE_GNULD_IMAGE_VERSION} <LINK_LIBRARIES>")
  
# /Applications/Energia.app/Contents/Resources/Java/hardware/tools/msp430/bin/msp430-objcopy -O ihex -R .eeprom main main.hex
# /Applications/Energia.app/Contents/Resources/Java/hardware/tools/msp430/mspdebug/mspdebug rf2500 --force-reset prog main.hex
  
  
 
