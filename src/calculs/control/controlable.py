from abc import ABCMeta, abstractmethod


class Controlable:
    __metaclass__ = ABCMeta

    @abstractmethod
    def x_plus(self):
        """
        :return: 
        """
        return

    @abstractmethod
    def x_minus(self):
        """
        :return: 
        """
        return

    @abstractmethod
    def y_plus(self):
        """
        :return: 
        """
        return

    @abstractmethod
    def y_minus(self):
        """
        :return: 
        """
        return

    @abstractmethod
    def z_plus(self):
        """
        :return: 
        """
        return

    @abstractmethod
    def z_minus(self):
        """
        :return: 
        """
        return

    @abstractmethod
    def roll_plus(self):
        """
        :return: 
        """
        return

    @abstractmethod
    def roll_minus(self):
        """
        :return: 
        """
        return

    @abstractmethod
    def pitch_plus(self):
        """
        :return: 
        """
        return

    @abstractmethod
    def pitch_minus(self):
        """
        :return: 
        """
        return

    @abstractmethod
    def yaw_plus(self):
        """
        :return: 
        """
        return

    @abstractmethod
    def yaw_minus(self):
        """
        :return: 
        """
        return

