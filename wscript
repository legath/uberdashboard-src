#!/usr/bin/env python
top = '.'
out = 'build'
APPNAME = 'uberdashboard-fw'
VERSION = '0.0'

def options(opt):
    opt.load('compiler_cxx')

def configure(conf):
    conf.env.CXX = 'arm-none-eabi-g++' #TODO: need to add logic for clang
    conf.env.AR = 'arm-none-eabi-ar'
    conf.load('compiler_cxx')
def build(bld):
    bld.program(
        source = ['app/main.cpp'],
        cxxflags = ['-std=c++11', '-O2', '-Wall', '-Werror']
    )
