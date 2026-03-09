import os
from configparser import ConfigParser

# config = ConfigParser()
# config.read("config.ini")
# print(config.get("locator","username"))
# print(config.get("basic info","testsiteurl"))


def readConfig(section,key):
    config = ConfigParser()
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Directory where configReader.py is located
    # print(BASE_DIR)
    CONFIG_PATH = os.path.join(BASE_DIR, "..", "ConfigurationData", "conf.ini")  # Navigate to conf.ini
    # print(CONFIG_PATH)
    #config.read("..\\ConfigurationData\\conf.ini")
    #config.read("ConfigurationData\\conf.ini")
    config.read(CONFIG_PATH)
    return config.get(section,key)
