#pragma once

#include "%(name)s/%(name)s_export.h"

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief Reports the name of the library
 */
%(uc_name)s_EXPORT const char* exported_function(void);

#ifdef __cplusplus
}  // extern "C"
#endif
