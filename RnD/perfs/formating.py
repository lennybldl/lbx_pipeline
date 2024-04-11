from lbx_python import context

count = 10**7

base_name = "test"

with context.TimeIt(message="join"):
    for i in range(count):
        name = " ".join([base_name, str(i)])

with context.TimeIt(message="format"):
    for i in range(count):
        name = "{} {}".format(base_name, i)

with context.TimeIt(message="concatenate convert to str"):
    for i in range(count):
        name = base_name + str(i)

with context.TimeIt(message="%"):
    for i in range(count):
        name = "%s %s" % (base_name, i)

with context.TimeIt(message="concatenate map"):
    for i in map(str, range(count)):
        name = base_name + i

iterations = map(str, range(count))
with context.TimeIt(message="concatenate already str"):
    for i in iterations:
        name = base_name + i

# result for count = 10**7:
# join - 2.51222 secs
# format - 2.346042 secs
# concatenate convert to str - 2.040422 secs
# % - 1.963295 secs
# concatenate map - 1.91274 secs
# concatenate already str - 1.862228 secs
