#pragma once

#include "{= name =}/{= name =}_export.h"

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief Reports the name of the library
 */
{= uc_name =}_EXPORT const char* exported_function(void);

#ifdef __cplusplus
}  // extern "C"
#endif
