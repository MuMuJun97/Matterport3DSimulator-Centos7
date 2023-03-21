project(Matterport_Simulator CXX)
cmake_minimum_required(VERSION 2.8)
message("\n\n*************************************************\n\n")


# https://stackoverflow.com/questions/44487053/set-pkg-config-path-in-cmake
# 设置 system environment variable 
# set(ENV{PKG_CONFIG_PATH} "/data/pkgconfig/lib64/pkgconfig")
# 手动指定pkg-config执行文件路径. 
# set(PKG_CONFIG_EXECUTABLE "/data/pkgconfig/bin/pkg-config")


# 设置环境变量. 
# export MPDIR=$(pwd)
# export PKG_CONFIG_EXECUTABLE=$MPDIR/extra/pkgconfig/bin/pkg-config:$PKG_CONFIG_EXECUTABLE
# export PATH=$MPDIR/extra/pkgconfig/bin:$PATH
# export PKG_CONFIG_PATH=$MPDIR/extra:$PKG_CONFIG_PATH
# 编译指令
# cmake -DEGL_RENDERING=ON ..


# $PKG_CONFIG_EXECUTABLE 手动指定pkgconfig的路径
# >>> /data/pkgconfig/bin/pkg-config:
# echo $PKG_CONFIG_PATH 手动指定glm的路径
# >>> /data/epoxy/lib64/pkgconfig:/data/GLM/lib64/pkgconfig:/data/jsoncpp/lib64/pkgconfig

option(OSMESA_RENDERING "Offscreen CPU rendering with OSMesa" OFF)

# cmake -DEGL_RENDERING=ON ..
option(EGL_RENDERING "Offscreen GPU rendering with EGL" ON)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
# Make custom find-modules available
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${PROJECT_SOURCE_DIR}/cmake/Modules")

if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release)
endif()

include_directories("${PROJECT_SOURCE_DIR}/include")


message("******** [INFO] PROJECT_SOURCE_DIR: ${PROJECT_SOURCE_DIR}\n")

set(OpenCV_DIR "${PROJECT_SOURCE_DIR}/extra/opencv3/share/OpenCV")
set(PkgConfig_DIR "${PROJECT_SOURCE_DIR}/extra/pkgconfig")
set(JSONCPP_DIR "${PROJECT_SOURCE_DIR}/extra/jsoncpp")

message("******** [INFO] OpenCV_DIR: ${OpenCV_DIR}\n")
message("******** [INFO] PkgConfig_DIR: ${PkgConfig_DIR}\n")
message("******** [INFO] JSONCPP_DIR: ${JSONCPP_DIR}\n")

find_package(OpenCV REQUIRED)
find_package(PkgConfig REQUIRED)
find_package(OpenMP)



if (OPENMP_CXX_FOUND)
    set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
    set (CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${OpenMP_EXE_LINKER_FLAGS}")
endif()

pkg_check_modules(JSONCPP REQUIRED jsoncpp)

message("******** [INFO] JSONCPP_INCLUDE_DIRS:  ${JSONCPP_INCLUDE_DIRS}") # include_directories(${jsoncpp_INCLUDE_DIRS})
message("******** [INFO] JSONCPP_LIBRARIES:  ${JSONCPP_LIBRARIES}")
message("******** [INFO] OpenCV_LIBS:  ${OpenCV_LIBS}")
link_directories("${PROJECT_SOURCE_DIR}/extra/jsoncpp/lib64")

include_directories("${JSONCPP_INCLUDE_DIRS}")
find_package(PythonInterp 3.8)
if(EGL_RENDERING)
  message(" EGL ....... ")
  add_definitions(-DEGL_RENDERING)
  find_package(OpenGL REQUIRED COMPONENTS OpenGL EGL)

  # pkg-config find epoxy
  pkg_check_modules(EPOXY REQUIRED epoxy)
  
  # -lepoxy
  set(EPOXY_LIBRARIES "${PROJECT_SOURCE_DIR}/extra/epoxy/lib64/libepoxy.so")
  
  message("EPOXY_LIBRARIES ${EPOXY_LIBRARIES}")
  message("******** [INFO] EPOXY_INCLUDE_DIRS:  ${EPOXY_INCLUDE_DIRS}")
  include_directories("${EPOXY_INCLUDE_DIRS}")

  pkg_check_modules(GLM REQUIRED glm)
  message("******** [INFO] GLM_INCLUDE_DIRS:  ${GLM_INCLUDE_DIRS}")
  include_directories("${GLM_INCLUDE_DIRS}")

  set(GL_LIBS OpenGL::OpenGL OpenGL::EGL ${EPOXY_LIBRARIES})

  message("******** [INFO] EPOXY_LIBRARIES:  ${EPOXY_LIBRARIES}")

elseif(OSMESA_RENDERING)
  add_definitions(-DOSMESA_RENDERING)
  pkg_check_modules(OSMESA REQUIRED osmesa)
  set(GL_LIBS ${OSMESA_LIBRARIES})
else()
  cmake_policy(SET CMP0072 OLD)
  find_package(OpenGL REQUIRED)
  find_package(GLEW REQUIRED)
  set(GL_LIBS ${OPENGL_LIBRARIES} ${GLEW_LIBRARIES})
endif()

add_library(MatterSim SHARED src/lib/MatterSim.cpp src/lib/NavGraph.cpp src/lib/Benchmark.cpp src/lib/cbf.cpp)
if(OSMESA_RENDERING)
  target_compile_definitions(MatterSim PUBLIC "-DOSMESA_RENDERING")
endif()
target_include_directories(MatterSim PRIVATE ${JSONCPP_INCLUDE_DIRS})
target_link_libraries(MatterSim ${JSONCPP_LIBRARIES} ${OpenCV_LIBS} ${GL_LIBS})

add_executable(tests src/test/main.cpp)
target_include_directories(tests PRIVATE ${JSONCPP_INCLUDE_DIRS})
target_link_libraries(tests MatterSim ${JSONCPP_LIBRARIES} ${OpenCV_LIBS})

add_executable(mattersim_main src/driver/mattersim_main.cpp)
target_link_libraries(mattersim_main MatterSim)

add_subdirectory(pybind11)

find_package(PythonInterp 3.8)
message(${PYTHON_EXECUTABLE})

# Need to search for python executable again to pick up an activated
# virtualenv python, if any.
unset(PYTHON_EXECUTABLE CACHE)
find_program(PYTHON_EXECUTABLE python
      PATHS ENV PATH         # look in the PATH environment variable
      NO_DEFAULT_PATH        # do not look anywhere else...
      )

find_package(NumPy REQUIRED)

pybind11_add_module(MatterSimPython src/lib_python/MatterSimPython.cpp)
target_include_directories(MatterSimPython PRIVATE ${NUMPY_INCLUDES})
target_link_libraries(MatterSimPython PRIVATE MatterSim)
set_target_properties(MatterSimPython
  PROPERTIES
  OUTPUT_NAME MatterSim)
