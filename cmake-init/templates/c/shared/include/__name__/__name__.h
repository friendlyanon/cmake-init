#pragma once

#include "{= name =}/{= name =}_export.h"

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief Reports the name of the library{% if pm %} that must be freed by the caller{% end %}
 */
{= uc_name =}_EXPORT char const* exported_function(void);

#ifdef __cplusplus
}  // extern "C"
#endif
