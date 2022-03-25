#include "lib.h"{% if pm %}

#include <hedley.h>
#include <json-c/json_object.h>
#include <json-c/json_tokener.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>

static const char json[] = "{\"name\":\"{= name =}\"}";{% end %}

struct library create_library()
{
  struct library lib;{% if pm %}
  struct json_tokener* tokener = NULL;
  struct json_object* object = NULL;
  struct json_object* name_object = NULL;
  const char* json_name = NULL;
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
  lib.name = name;{% else %}
  lib.name = "{= name =}";{% end %}
  return lib;
}{% if pm %}

void destroy_library(struct library* lib)
{
  free(HEDLEY_CONST_CAST(void*, lib->name));
}{% end %}
