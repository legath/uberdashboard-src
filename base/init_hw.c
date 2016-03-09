//based on GNU ARM Eclipse distribution
// modifed by uberdashboard project



#include "stm32f4xx.h"
#include "stm32f4xx_hal.h"
#include "stm32f4xx_hal_cortex.h"

extern unsigned int __vectors_start;
void __initialize_hardware(void);

void SystemClock_Config(void);

void
__initialize_hardware(void)
{
  HAL_Init();
  SystemClock_Config();
  SystemCoreClockUpdate();
}


void __attribute__((weak)) SystemClock_Config(void) //TODO: rewrite in order to sysinit.c
{
  __PWR_CLK_ENABLE();

  __HAL_PWR_VOLTAGESCALING_CONFIG(PWR_REGULATOR_VOLTAGE_SCALE1);

  RCC_OscInitTypeDef RCC_OscInitStruct;

#if defined(HSE_VALUE) && (HSE_VALUE != 0)
  // Enable HSE Oscillator and activate PLL with HSE as source.
  // This is tuned for STM32F4-DISCOVERY; update it for your board.
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSE;
  RCC_OscInitStruct.HSEState = RCC_HSE_ON;
  RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSE;
  // This assumes the HSE_VALUE is a multiple of 1 MHz. If this is not
  // your case, you have to recompute these PLL constants.
  RCC_OscInitStruct.PLL.PLLM = (HSE_VALUE/1000000u);
#else
  // Use HSI and activate PLL with HSI as source.
  // This is tuned for NUCLEO-F411; update it for your board.
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSI;
  RCC_OscInitStruct.HSIState = RCC_HSI_ON;
  // 16 is the average calibration value, adjust for your own board.
  RCC_OscInitStruct.HSICalibrationValue = 16;
  RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSI;
  // This assumes the HSI_VALUE is a multiple of 1 MHz. If this is not
  // your case, you have to recompute these PLL constants.
  RCC_OscInitStruct.PLL.PLLM = (HSI_VALUE/1000000u);
#endif

  RCC_OscInitStruct.PLL.PLLN = 336;
#if defined(STM32F401xC) || defined(STM32F401xE) || defined(STM32F411xE)
  RCC_OscInitStruct.PLL.PLLP = RCC_PLLP_DIV4; /* 84 MHz */
#elif defined(STM32F427xx) || defined(STM32F437xx) || defined(STM32F429xx) || defined(STM32F439xx)
  RCC_OscInitStruct.PLL.PLLP = RCC_PLLP_DIV2; /* 168 MHz */
#elif defined(STM32F405xx) || defined(STM32F415xx) || defined(STM32F407xx) || defined(STM32F417xx)
  RCC_OscInitStruct.PLL.PLLP = RCC_PLLP_DIV2; /* 168 MHz */
#elif defined(STM32F446xx)
  RCC_OscInitStruct.PLL.PLLP = RCC_PLLP_DIV2; /* 168 MHz */
#else
  RCC_OscInitStruct.PLL.PLLP = RCC_PLLP_DIV4; /* 84 MHz, conservative */
#endif
  RCC_OscInitStruct.PLL.PLLQ = 7; /* To make USB work. */
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
  HAL_RCC_OscConfig(&RCC_OscInitStruct);

  RCC_ClkInitTypeDef RCC_ClkInitStruct;
  // Select PLL as system clock source and configure the HCLK, PCLK1 and PCLK2
  // clocks dividers
  RCC_ClkInitStruct.ClockType = (RCC_CLOCKTYPE_SYSCLK | RCC_CLOCKTYPE_HCLK
      | RCC_CLOCKTYPE_PCLK1 | RCC_CLOCKTYPE_PCLK2);
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
#if defined(STM32F401xC) || defined(STM32F401xE) || defined(STM32F411xE)
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV2;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;
  HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_2);
#else
  // This is expected to work for most large cores.
  // Check and update it for your own configuration.
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV4;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV2;
  HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_5);
#endif

  HAL_SYSTICK_Config(HAL_RCC_GetHCLKFreq()/1000);

  HAL_SYSTICK_CLKSourceConfig(SYSTICK_CLKSOURCE_HCLK);
}
void
__attribute__((weak))
__initialize_hardware_early(void)
{
  // Call the CSMSIS system initialisation routine.
  SystemInit();

#if defined(__ARM_ARCH_7M__) || defined(__ARM_ARCH_7EM__)
  // Set VTOR to the actual address, provided by the linker script.
  // Override the manual, possibly wrong, SystemInit() setting.
  SCB->VTOR = (uint32_t)(&__vectors_start);
#endif

  // The current version of SystemInit() leaves the value of the clock
  // in a RAM variable (SystemCoreClock), which will be cleared shortly,
  // so it needs to be recomputed after the RAM initialisations
  // are completed.

#if defined(OS_INCLUDE_STARTUP_INIT_FP) || (defined (__VFP_FP__) && !defined (__SOFTFP__))

  // Normally FP init is done by SystemInit(). In case this is not done
  // there, it is possible to force its inclusion by defining
  // OS_INCLUDE_STARTUP_INIT_FP.

  // Enable the Cortex-M4 FPU only when -mfloat-abi=hard.
  // Code taken from Section 7.1, Cortex-M4 TRM (DDI0439C)

  // Set bits 20-23 to enable CP10 and CP11 coprocessor
  SCB->CPACR |= (0xF << 20);

#endif // (__VFP_FP__) && !(__SOFTFP__)


}
