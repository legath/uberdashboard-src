//
// This file is part of the Uberdashboard project
// Copyright (c) 2016 Alexander Bulychev (a.f.bulychev@gmail.com).
//
//
// ----------------------------------------------------------------------------

#include <stdio.h>
#include <stdlib.h>
#include "stm32f4xx.h"
#include <scmRTOS.h>

#include "processes.h"
#include "gui_process.h"

int main(void)
{
	OS::run();
}

extern "C" uint32_t HAL_GetTick(void)
{
  return OS::get_tick_count();
}

// ----------------------------------------------------------------------------
