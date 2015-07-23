project(msp430_delta_robot)
cmake_minimum_required(VERSION 2.8)

# Configuration
# =============
#
set(CONF_FREQUENCY_IN_HZ "1000000UL" CACHE STRING "CPU frequency used")
#set(CMAKE_TOOLCHAIN_FILE ${CMAKE_CURRENT_SOURCE_DIR}/cmake/msp430.cmake)
# Compiler Settings
add_definitions("-DF_CPU=${CONF_FREQUENCY_IN_HZ}")


# NRF24NetworkingModule
#include_directories(${CMAKE_CURRENT_SOURCE_DIR}/msp430lib/include)
add_executable(main 
    main.cpp
)

