#pragma once

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief Reports the name of the library
 */
const char* header_only_name(void);

#ifdef {= uc_name =}_IMPLEMENTATION
const char* header_only_name()
{
  return "{= name =}";
}
#endif

#ifdef __cplusplus
}  // extern "C"
#endif
