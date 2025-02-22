cmake_minimum_required(VERSION 3.1)

project(aws-crt-jni C)
option(BUILD_DEPS "Builds aws common runtime dependencies as part of build" ON)

if (POLICY CMP0069)
    cmake_policy(SET CMP0069 NEW) # Enable LTO/IPO if available in the compiler, see AwsCFlags
endif()

if (POLICY CMP0077)
    cmake_policy(SET CMP0077 NEW) # Enable options to get their values from normal variables
endif()

if (DEFINED CMAKE_PREFIX_PATH)
    file(TO_CMAKE_PATH "${CMAKE_PREFIX_PATH}" CMAKE_PREFIX_PATH)
endif()

if (DEFINED CMAKE_INSTALL_PREFIX)
    file(TO_CMAKE_PATH "${CMAKE_INSTALL_PREFIX}" CMAKE_INSTALL_PREFIX)
endif()

if (UNIX AND NOT APPLE)
    include(GNUInstallDirs)
elseif(NOT DEFINED CMAKE_INSTALL_LIBDIR)
    set(CMAKE_INSTALL_LIBDIR "lib")
endif()

if (${CMAKE_INSTALL_LIBDIR} STREQUAL "lib64")
    set(FIND_LIBRARY_USE_LIB64_PATHS true)
endif()

if (NOT WIN32 AND NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE "RelWithDebInfo")
endif()

# This is required in order to append /lib/cmake to each element in CMAKE_PREFIX_PATH
set(AWS_MODULE_DIR "/${CMAKE_INSTALL_LIBDIR}/cmake")
string(REPLACE ";" "${AWS_MODULE_DIR};" AWS_MODULE_PATH "${CMAKE_PREFIX_PATH}${AWS_MODULE_DIR}")
# Append that generated list to the module search path
list(APPEND CMAKE_MODULE_PATH ${AWS_MODULE_PATH})

# Local CMake scripts
list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_LIST_DIR}/cmake")

set(AWS_LIBRARY_OUTPUT_DIR "${CMAKE_BINARY_DIR}/lib")

if (ANDROID)
    set(ANDROID_DEPS_DIR ${CMAKE_CURRENT_SOURCE_DIR}/target/cmake-build/deps/${ANDROID_ABI})
    set(AWS_LIBRARY_OUTPUT_DIR "${CMAKE_BINARY_DIR}/../../../lib")
endif()

if (BUILD_DEPS)
    list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_LIST_DIR}/aws-crt-ffi/crt/aws-c-common/cmake")
    include(AwsFindPackage)

    set(IN_SOURCE_BUILD ON)
    set(BUILD_TESTING OFF)

    if (UNIX AND NOT APPLE)
        set(BUILD_LIBSSL OFF CACHE BOOL "Don't need libssl, only need libcrypto")
        set(DISABLE_PERL ON CACHE BOOL "Disable codegen")
        set(DISABLE_GO ON CACHE BOOL "Disable codegen")

        # temporarily disable certain warnings as errors for the aws-lc build
        set(OLD_CMAKE_C_FLAGS "${CMAKE_C_FLAGS}")
        if (NOT MSVC)
            check_c_compiler_flag(-Wno-stringop-overflow HAS_WNO_STRINGOP_OVERFLOW)
            if (HAS_WNO_STRINGOP_OVERFLOW)
                set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Wno-stringop-overflow")
            endif()

            check_c_compiler_flag(-Wno-array-parameter HAS_WNO_ARRAY_PARAMETER)
            if (HAS_WNO_ARRAY_PARAMETER)
                set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Wno-array-parameter")
            endif()
        endif()

        # restore previous build flags
        set(CMAKE_C_FLAGS "${OLD_CMAKE_C_FLAGS}")

        set(SEARCH_LIBCRYPTO OFF CACHE BOOL "Let S2N use libcrypto from AWS-LC.")
        set(UNSAFE_TREAT_WARNINGS_AS_ERRORS OFF CACHE BOOL "Disable warnings-as-errors when building S2N")

    endif()
    add_subdirectory(aws-crt-ffi)

else()
    include(AwsFindPackage)
    include(AwsCFlags)
    set(IN_SOURCE_BUILD OFF)
endif()

include(UseJava)

file(GLOB AWS_CRT_JAVA_HEADERS
        "smithy-crt-test/javalib/*.h"
        )

file(GLOB AWS_CRT_JAVA_SRC
        "smithy-crt-test/javalib/*.c"
        )

file(GLOB CRT_JAVA_HEADERS
        ${AWS_CRT_JAVA_HEADERS}
        )

file(GLOB CRT_JAVA_SRC
        ${AWS_CRT_JAVA_SRC}
        )

# figure out the target platform info and output the lib there
set(TARGET_LIB_DIR "${AWS_LIBRARY_OUTPUT_DIR}/")

# shared lib that contains the CRT and JNI bindings, to be loaded by java
add_library(${PROJECT_NAME} SHARED ${CRT_JAVA_HEADERS} ${CRT_JAVA_SRC})
aws_use_package(aws-crt-ffi)

target_link_libraries(${PROJECT_NAME} ${DEP_AWS_LIBS})
if (NOT MSVC AND NOT APPLE)
    set_target_properties(${PROJECT_NAME} PROPERTIES LINK_FLAGS "-z noexecstack")
endif()

set_target_properties(${PROJECT_NAME} PROPERTIES LINKER_LANGUAGE C)
# for non-msvc, library output will control the shared lib output
set_target_properties(${PROJECT_NAME} PROPERTIES LIBRARY_OUTPUT_DIRECTORY ${TARGET_LIB_DIR})
# for msvc, runtime controls where dlls are output
set_target_properties(${PROJECT_NAME} PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${TARGET_LIB_DIR})
set_target_properties(${PROJECT_NAME} PROPERTIES RUNTIME_OUTPUT_DIRECTORY_DEBUG ${TARGET_LIB_DIR})
set_target_properties(${PROJECT_NAME} PROPERTIES RUNTIME_OUTPUT_DIRECTORY_RELEASE ${TARGET_LIB_DIR})
set_target_properties(${PROJECT_NAME} PROPERTIES RUNTIME_OUTPUT_DIRECTORY_RELWITHDEBINFO ${TARGET_LIB_DIR})

aws_set_common_properties(${PROJECT_NAME})

set(CMAKE_C_FLAGS_DEBUGOPT "")
set_property(TARGET ${PROJECT_NAME} PROPERTY C_STANDARD 99)

#set warnings
if (MSVC)
    target_compile_options(${PROJECT_NAME} PRIVATE /W4 /WX -D_CRT_SECURE_NO_WARNINGS)
else ()
    target_compile_options(${PROJECT_NAME} PRIVATE -Wall -Wno-long-long -pedantic -Werror)
endif ()

# find JNI and add the include path (except on android where gradle injects it)
if (NOT ANDROID)
    if (NOT APPLE)
        set(JAVA_AWT_LIBRARY NotNeeded)
        set(JAVA_AWT_INCLUDE_PATH NotNeeded)
    endif()
    message(STATUS "JAVA_HOME=$ENV{JAVA_HOME}")
    find_package(JNI REQUIRED)
    target_include_directories(${PROJECT_NAME} PRIVATE ${JNI_INCLUDE_DIRS})
endif()

target_include_directories(${PROJECT_NAME} PRIVATE "aws-crt-ffi")

if (CMAKE_BUILD_TYPE STREQUAL "" OR CMAKE_BUILD_TYPE MATCHES Debug)
    target_compile_definitions(${PROJECT_NAME} PRIVATE "-DDEBUG_BUILD")
endif ()

target_include_directories(${PROJECT_NAME} PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
        $<INSTALL_INTERFACE:include>)