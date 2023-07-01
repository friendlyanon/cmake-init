#pragma once{% if pm %}

#ifdef {= uc_name =}_IMPLEMENTATION
#  include <json-c/json_object.h>
#  include <json-c/json_tokener.h>
#  include <stddef.h>
#  include <stdlib.h>
#  include <string.h>
#endif{% end %}

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief Reports the name of the library{% if pm %} that must be freed by the caller{% end %}
 */
char const* header_only_name(void);

#ifdef {= uc_name =}_IMPLEMENTATION
{% if pm %}
static char const json[] = "{\"name\":\"{= name =}\"}";
{% end %}
char const* header_only_name()
{{% if pm %}
  struct json_tokener* tokener = NULL;
  struct json_object* object = NULL;
  struct json_object* name_object = NULL;
  char const* json_name = NULL;
  size_t name_size = 0;
  char* name = NULL;

  tokener = json_tokener_new();
  if (tokener == NULL) {
    goto exit;
  }

  object = json_tokener_parse_ex(tokener, json, sizeof(json));
  if (object == NULL) {
    goto cleanup_tokener;
  }

  if (json_object_object_get_ex(object, "name", &name_object) == 0) {
    goto cleanup_object;
  }

  json_name = json_object_get_string(name_object);
  if (json_name == NULL) {
    goto cleanup_object;
  }

  name_size = strlen(json_name) + 1;
  name = malloc(name_size);
  if (name == NULL) {
    goto cleanup_object;
  }

  (void)memcpy(name, json_name, name_size);

cleanup_object:
  (void)json_object_put(object);

cleanup_tokener:
  json_tokener_free(tokener);

exit:
  return name;{% else %}
  return "{= name =}";{% end %}
}

#endif

#ifdef __cplusplus
}  // extern "C"
#endif
