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

typedef OS::process<OS::pr0, 300> TProc0;

TProc0 Proc0;

int main(void)
{
	
	OS::run();

}
namespace OS
{
    template <>
    OS_PROCESS void TProc0::exec()
    {
        for(;;)
        {
        	
        }
    }
}


extern "C" uint32_t HAL_GetTick(void)
{
  return OS::get_tick_count();
}

// ----------------------------------------------------------------------------
