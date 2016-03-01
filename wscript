#!/usr/bin/env python
top = '.'
out = 'build'
APPNAME = 'uberdashboard-fw'
VERSION = '0.0'

def options(opt):
    opt.load('compiler_cxx')
    opt.load('compiler_c')
    opt.add_option('--debug', action='store', default=False, help='Build project with debug info')
    opt.add_option('--usb-console', action='store', default=False, help='Build project with USB CDC shell support')

#-mcpu=cortex-m4 -mthumb -mfloat-abi=hard -mfpu=fpv4-sp-d16 -Og -fmessage-length=0 -fsigned-char -ffunction-sections -fdata-sections  -g3 -gdwarf-2
def configure(conf):
    conf.env.CC = 'arm-none-eabi-gcc'
    conf.env.CXX = 'arm-none-eabi-g++' #TODO: need to add logic for clang
    conf.env.AR = 'arm-none-eabi-ar'
    conf.env.LD = 'arm-none-eabi-ld'
    conf.load('compiler_c')
    conf.load('compiler_cxx')

def post(printSize):
        print('Image size :')

def build(bld):
    bld.objects(
                source = '',
                target = 'scmrtos')
    bld.objects(
                source = '',
                target = 'hal')
    bld.objects(
                source = '',
                target = 'ugfx')
    bld.program(
        source = ['app/main.cpp'],
        cxxflags = ['-std=c++11', '-O2', '-Wall', '-Werror'],
        use    = 'scmrtos hal ugfx'
    )
    bld.add_post_fun(printSize)
