#pragma once

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief Reports the name of the library
 */
const char* header_only_name(void);

#ifdef %(uc_name)s_IMPLEMENTATION
const char* header_only_name(void)
{
  return "%(name)s";
}
#endif

#ifdef __cplusplus
}  // extern "C"
#endif
