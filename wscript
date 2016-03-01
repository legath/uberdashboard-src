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


def configure(conf):
    conf.env.CC = 'arm-none-eabi-gcc'
    conf.env.CXX = 'arm-none-eabi-g++' #TODO: need to add logic for clang
    conf.env.AR = 'arm-none-eabi-ar'
    conf.load('compiler_c')
    conf.load('compiler_cxx')

def post(printSize):
        print('Image size :')

def build(bld):
    bld.stlib(source='x.c foo.src', target='scmrtoslib')
    bld.program(
        source = ['app/main.cpp'],
        cxxflags = ['-std=c++11', '-O2', '-Wall', '-Werror']
    )
    bld.add_post_fun(printSize)
