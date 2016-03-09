#!/usr/bin/env python
import os
top = '.'
out = 'build'
APPNAME = 'uberdashboard-fw'
VERSION = '0.0'

def options(ctx):
    ctx.load('compiler_cxx')
    ctx.load('compiler_c')
    if os.path.exists('eclipse.py'):
		ctx.load('eclipse')
    ctx.add_option('--debug', action='store', default=False, help='Build project with debug info')
    ctx.add_option('--usb-console', action='store', default=False, help='Build project with USB CDC shell support')

# -Og -g3 -gdwarf-2
def configure(ctx):
    ctx.env.CC = 'arm-none-eabi-gcc'
    ctx.env.CXX = 'arm-none-eabi-g++' #TODO: need to add logic for clang
    ctx.env.AR = 'arm-none-eabi-ar'
    ctx.env.LD = 'arm-none-eabi-ld'
    ctx.load('compiler_c')
    ctx.load('compiler_cxx')
    ctx.env.append_unique('CFLAGS', ['-mcpu=cortex-m4', '-mthumb', '-mfloat-abi=hard', '-mfpu=fpv4-sp-d16' ,'-fmessage-length=0','-fsigned-char', '-ffunction-sections','-fdata-sections'  ])
    ctx.env.append_unique('CXXFLAGS', ['-mcpu=cortex-m4', '-mthumb', '-mfloat-abi=hard', '-mfpu=fpv4-sp-d16' ,'-fmessage-length=0','-fsigned-char', '-ffunction-sections','-fdata-sections' ,'-fabi-version=0', '-fno-exceptions', '-fno-rtti', '-fno-use-cxa-atexit', '-fno-threadsafe-statics' ])
    ctx.env.append_unique('LDFLAGS', ['-mcpu=cortex-m4', '-mthumb', '-mfloat-abi=hard', '-mfpu=fpv4-sp-d16' ,'-fmessage-length=0','-fsigned-char', '-ffunction-sections','-fdata-sections' ,'-fabi-version=0', '-fno-exceptions', '-fno-rtti', '-fno-use-cxa-atexit', '-fno-threadsafe-statics' ])
    ctx.env.append_unique('LDFLAGS', ['-L./','-T ldscripts/mem.ld','-T ldscripts/libs.ld','-T ldscripts/sections.ld','-nostartfiles','-Xlinker','--gc-sections'])
    ctx.env.append_unique('FILES_HAL', ['HAL/Drivers/STM32F4xx_HAL_Driver/Src/*.c'])

def printSize(ctx):
        print('Image size :')

def build(ctx):
    ctx.objects(
                source = ['scmrtos/core/os_kernel.cpp',
                                'scmrtos/core/os_services.cpp',
                                'scmrtos/core/usrlib.cpp',
                                'scmrtos/port/cortex/mx-gcc/os_target.cpp'],
                includes = ['scmrtos/core',
                            'scmrtos/port/cortex/mx-gcc',
                            'conf'],
                cxxflags = ['-std=c++11', '-O2'],
                target = 'scmrtos')
    ctx.objects(
                source = ctx.path.ant_glob(ctx.env.FILES_HAL),
                defines = ['STM32F429xx',
                                'DATA_IN_ExtSDRAM'],
                includes = ['HAL/Drivers/STM32F4xx_HAL_Driver/Inc/',
                                   'HAL/Drivers/CMSIS/Device/ST/STM32F4xx/Include/',
                                   'HAL/Drivers/CMSIS/Include/',
                                   'conf'],
                target = 'hal')
    ctx.objects(
                source = '',
                target = 'ugfx')
    ctx.objects(
                source = ['newlib/_cxx.cpp',
                                'newlib/_exit.c',
                                'newlib/_sbrk.c',
                                'newlib/_startup.c',
                                'newlib/_syscalls.c'],
                target = 'newlib')
    ctx.program(
        defines = ['STM32F429xx',
                        'DATA_IN_ExtSDRAM',
                        'HSE_VALUE=8000000'],
        source = ['app/main.cpp',
                        'base/init_hw.c',
                        'base/vectors.c',
                        'base/system_stm32f4xx.c'],
        cxxflags = ['-std=c++11', '-O2', '-Wall'],
        includes = ['HAL/Drivers/CMSIS/Device/ST/STM32F4xx/Include/',
                          'HAL/Drivers/CMSIS/Include/',
                          'HAL/Drivers/STM32F4xx_HAL_Driver/Inc/',
                           'conf'],
        use    = 'scmrtos hal newlib',
        target = 'uberdashboard-fw.elf'
    )
    ctx.add_post_fun(printSize)
