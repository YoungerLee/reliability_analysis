from meta.device import Device
from collections import OrderedDict


class Report(object):
    def __init__(self):
        self.__devices = list()
        self.__relia_images = OrderedDict()
        self.__relia_table = OrderedDict()
        self.__maintain_images = OrderedDict()
        self.__maintain_table = OrderedDict()
        self.__fault_images = OrderedDict()
        self.__fault_table = OrderedDict()

    def isEmpty(self):
        return True if len(self.__devices) <= 0 else False
    def setDevice(self, dev_id, dev_name, dev_num):
        self.__devices.append(Device(id=dev_id, name=dev_name, num=dev_num))

    def getDevice(self):
        '''以二维表格形式返回'''
        table = []
        for dev in self.__devices:
            table.append([dev.id, dev.name, dev.num])
        return table

    def setReliaImages(self, title, image_path):
        self.__relia_images[title] = image_path

    def getReliaImages(self):
        return self.__relia_images

    def setReliaTable(self, key, value):
        self.__relia_table[key] = value

    def getReliaTable(self):
        return self.__relia_table

    def setMaintainImages(self, title, image_path):
        self.__maintain_images[title] = image_path

    def getMaintainImages(self):
        return self.__maintain_images

    def setMaintainTable(self, key, value):
        self.__maintain_table[key] = value

    def getMaintainTable(self):
        return self.__maintain_table

    def setFaultImages(self, title, image_path):
        self.__fault_images[title] = image_path

    def getFaultImages(self):
        return self.__fault_images

    def setFaultTable(self, key, value):
        self.__fault_table[key] = value

    def getFaultTable(self):
        return self.__fault_table


