import algorithm as i_algorithm
import backend as i_backend
import data as i_data
import operator as i_operator
import protocol as i_protocol


class ProgressingResult:

    result = None
    stopping = False

    def progressCallback(self, result):
        self.result = result
        return self.stopping

    def stop(self):
        self.stopping = True




