#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <stdbool.h>

bool is_string_in_array(const char *target, const char **array, int size)
{
    // get if a string lives in the given array
    for (int i = 0; i < size; i++)
    {
        if (strcmp(target, array[i]) == 0)
        {
            return true;
        }
    }
    return false;
}

char *get_unique_name(
    char *name,
    const char *default_name,
    const char **assigned_names,
    const int size)
{
    // Get a unique name from a name and a list of names.
    // - name : The name we want to set. If none given, use the default name.
    // - default_name : The default name to use if no name was given
    // - assigned_names : The list of already assigned names.
    // - size : The number of already assigned names.

    // intialize the variables
    int length = strlen(name);
    char base_name[512];
    // base_name[length + 3] = '\0';

    // if no name given make up a name from the data type
    // try making up a valid name
    if (length == 0)
    {
        // set the default name as base name
        strcpy(base_name, default_name);
        // set the default name as base name
        strcpy(name, default_name);
        strcat(name, "1");
    }
    else
    {
        // if the given name ends with an index, remove it from the base_name
        for (int i = length - 1; i > -1; i--)
        {
            char character = name[i];
            if (!isdigit(character))
            {
                // copy characters from start to last letter
                strncpy(base_name, name + 0, i + 1);
                break;
            }
        }
    }

    // figure out an available name
    int index = 1;
    while (is_string_in_array(name, assigned_names, size) == true)
    {
        strcpy(name, base_name);
        sprintf(name, "%s%d", base_name, index);
        index++;
    }
    return name;
}
