#include "{= name =}/{= name =}.h"{% if pm %}

#include <assert.h>
#include <json-c/json_object.h>
#include <json-c/json_tokener.h>
#include <stdlib.h>
#include <string.h>

static char const json[] = "{\"name\":\"{= name =}\"}";{% end %}

char const* exported_function(void)
{{% if pm %}{% if not c99 %}
  struct json_tokener* tokener = NULL;
  struct json_object* object = NULL;
  struct json_object* name_object = NULL;
  char const* json_name = NULL;
  int name_size = 0;{% end %}
  char* name = NULL;

  {% if c99 %}struct json_tokener* {% end %}tokener = json_tokener_new();
  if (tokener == NULL) {
    goto exit;
  }

  {% if c99 %}struct json_object* object =
      {% else %}object = {% end %}json_tokener_parse_ex(tokener, json, sizeof(json));
  if (object == NULL) {
    goto cleanup_tokener;
  }
{% if c99 %}
  struct json_object* name_object = NULL;{% end %}
  if (json_object_object_get_ex(object, "name", &name_object) == 0) {
    goto cleanup_object;
  }

  {% if c99 %}char const* {% end %}json_name = json_object_get_string(name_object);
  if (json_name == NULL) {
    goto cleanup_object;
  }

  {% if c99 %}int {% end %}name_size = json_object_get_string_len(name_object);
  name = malloc((size_t)name_size + 1);
  if (name == NULL) {
    goto cleanup_object;
  }

  (void)memcpy(name, json_name, name_size);
  name[name_size] = '\0';

cleanup_object:
  if (json_object_put(object) != 1) {
    assert(0);
  }

cleanup_tokener:
  json_tokener_free(tokener);

exit:
  return name;{% else %}
  return "{= name =}";{% end %}
}
