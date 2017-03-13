from abc import ABCMeta, abstractproperty, abstractmethod
import misc
import affinity as i_affinity
import backend as i_backend
import data as i_data
import operator as i_operator
import protocol as i_protocol


class Algorithm:
    __metaclass__ = ABCMeta

    @abstractmethod
    def search(self,
               localAbilities,
               remoteOperators,
               propagationLimit,
               trainingSet,
               testSet,
               progressCallback=None):

        raise NotImplementedError()


class DefaultAlgorithm(Algorithm):

    def search(self,
               localAbilities,
               remoteOperators,
               propagationLimit,
               trainingSet,
               testSet,
               progressCallback=None):

        pass
