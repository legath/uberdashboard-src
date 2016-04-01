//
// This file is part of the Uberdashboard project
// Copyright (c) 2016 Dmitriy Efimov (daefimov@gmail.com).
//
//
// ----------------------------------------------------------------------------
#ifndef PROCESSES_H
#define PROCESSES_H

#include <scmRTOS.h>
typedef OS::process<OS::pr0, 300> GuiProc; // процесс для GUI
//typedef OS::process<OS::pr1, 300> ...Proc; // процесс для ...


#endif // PROCESSES_H
