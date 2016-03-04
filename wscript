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
    ctx.env.append_value('CXXFLAGS', '-mcpu=cortex-m4')
    ctx.env.append_value('CXXFLAGS', '-mthumb')
    ctx.env.append_value('CXXFLAGS', '-mfloat-abi=hard')
    ctx.env.append_value('CXXFLAGS', '-mfpu=fpv4-sp-d16')
    ctx.env.append_value('CXXFLAGS', '-fmessage-length=0')
    ctx.env.append_value('CXXFLAGS', '-fsigned-char')
    ctx.env.append_value('CXXFLAGS', '-ffunction-sections')
    ctx.env.append_value('CXXFLAGS', '-fdata-sections')

def printSize(ctx):
        print('Image size :')

def build(ctx):
    ctx.objects(
                source = ['scmrtos/core/os_kernel.cpp',
                                'scmrtos/core/os_services.cpp',
                                'scmrtos/port/cortex/mx-gcc/os_target.cpp'],
                target = 'scmrtos')
    ctx.objects(
                source = '',
                defines = ['STM32F429xx',
                                'DATA_IN_ExtSDRAM'],
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
        source = ['app/main.cpp'],
        cxxflags = ['-std=c++11', '-O2', '-Wall', '-Werror'],
        use    = 'scmrtos ugfx newlib',
        target = 'uberdashboard-fw.elf'
    )
    ctx.add_post_fun(printSize)
