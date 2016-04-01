//
// This file is part of the Uberdashboard project
// Copyright (c) 2016 Dmitriy Efimov (daefimov@gmail.com).
//
//
// ----------------------------------------------------------------------------
#ifndef GUI_PROCESS_H
#define GUI_PROCESS_H

#include <scmRTOS.h>
#include "processes.h"

namespace OS
{	
	template <> OS_PROCESS void GuiProc::exec();
}

#endif // GUI_PROCESS_H
