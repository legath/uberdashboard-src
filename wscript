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
    optgr = ctx.add_option_group("Uberdashboard options")
    optgr.add_option('--debug', action='store_true',  help='Build project with debug info')
    optgr.add_option('--usb-console',  action='store_true', help='Build project with USB CDC shell support')

# -Og -g3 -gdwarf-2
def configure(ctx):
    ctx.env.CC = 'arm-none-eabi-gcc'
    ctx.env.CXX = 'arm-none-eabi-g++' #TODO: need to add logic for clang
    ctx.env.AR = 'arm-none-eabi-ar'
    ctx.env.LD = 'arm-none-eabi-ld'
    ctx.env.OBJCOPY = 'arm-none-eabi-objcopy'
    ctx.env.SIZE = 'arm-none-eabi-size'
    ctx.load('compiler_c')
    ctx.load('compiler_cxx')
    ctx.find_program('openocd', var='OPENOCD')
    ctx.env.append_unique('CFLAGS', ['-mcpu=cortex-m4', '-mthumb', '-mfloat-abi=hard', '-mfpu=fpv4-sp-d16' ,'-fmessage-length=0','-fsigned-char', '-ffunction-sections','-fdata-sections'  ])
    ctx.env.append_unique('CXXFLAGS', ['-mcpu=cortex-m4', '-mthumb', '-mfloat-abi=hard', '-mfpu=fpv4-sp-d16' ,'-fmessage-length=0','-fsigned-char', '-ffunction-sections','-fdata-sections' ,'-fabi-version=0', '-fno-exceptions', '-fno-rtti', '-fno-use-cxa-atexit', '-fno-threadsafe-statics' ])
    ctx.env.append_unique('LDFLAGS', ['-mcpu=cortex-m4', '-mthumb', '-mfloat-abi=hard', '-mfpu=fpv4-sp-d16' ,'-fmessage-length=0','-fsigned-char', '-ffunction-sections','-fdata-sections' ,'-fabi-version=0', '-fno-exceptions', '-fno-rtti', '-fno-use-cxa-atexit', '-fno-threadsafe-statics' ])
    ctx.env.append_unique('INCLUDES',['HAL/Drivers/STM32F4xx_HAL_Driver/Inc/', 'HAL/Drivers/CMSIS/Device/ST/STM32F4xx/Include/', 'HAL/Drivers/CMSIS/Include/', 'scmrtos/core', 'scmrtos/port/cortex/mx-gcc' , 'conf'])
    ctx.env.append_unique('DEFINES',['STM32F429xx','DATA_IN_ExtSDRAM','HSE_VALUE=8000000', 'USE_HAL_DRIVER'])
    if ctx.options.debug:
        ctx.env.append_unique('DEFINES',['DEBUG'])
    if ctx.options.usb_console:
        ctx.env.append_unique('DEFINES',['USB_SHELL'])

def build(ctx):
    ctx.objects(
                source = ctx.path.ant_glob('scmrtos/core/*.cpp')+
                                [ 'scmrtos/port/cortex/mx-gcc/os_target.cpp'],
                cxxflags = ['-std=c++11', '-O2'],
                target = 'scmrtos')
    ctx.objects(
                source = ctx.path.ant_glob('HAL/Drivers/STM32F4xx_HAL_Driver/Src/*.c'),
                target = 'hal')
    ctx.objects(
                source = '',
                target = 'ugfx')
    ctx.objects(
                source = [#'newlib/_cxx.cpp',
                                'newlib/_exit.c',
                                'newlib/_sbrk.c',
                                'newlib/_startup.c',
                                'newlib/_syscalls.c'],
                target = 'newlib')
    ctx.program(
        source = ['app/main.cpp']+
                        ctx.path.ant_glob('base/*.c'),
        cxxflags = ['-std=c++11', '-O2', '-Wall'],
        linkflags = ['-nostartfiles', '-T{0}'.format('../ldscripts/mem.ld'),'-T{0}'.format('../ldscripts/sections.ld'),'-Xlinker', '--gc-sections'],
        use    = 'scmrtos hal newlib',
        target = 'uberdashboard-fw.elf')
    ctx(rule='${OBJCOPY} -O ihex ${SRC} ${TGT}', source='uberdashboard-fw.elf', target='uberdashboard-fw.hex', name='objcopy')
    ctx(rule='${SIZE} --format=berkeley ${SRC}', source='uberdashboard-fw.elf', always=True, name='size')
    ctx(rule='${SIZE} --format=sysv ${SRC}', source='uberdashboard-fw.elf', always=True, name='size_sysv')
