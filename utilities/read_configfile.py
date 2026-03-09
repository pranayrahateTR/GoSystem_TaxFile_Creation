from configparser import ConfigParser
#
# CONFIG = ConfigParser()
# CONFIG.read('config.ini')
# print(CONFIG.get("locator","fname"))
# print(CONFIG.get("basic info","browser"))

def read_configfile(section, key):
    CONFIG = ConfigParser()
    CONFIG.read('config.ini')
    return CONFIG.get(section,key)
print(read_configfile('basic info','testsiteurl'))