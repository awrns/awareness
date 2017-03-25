import awareness


class TestAffinity(awareness.affinity.LocalAffinity):

    profile = (1,1)

    def run(self, inputStream, progressFrequency=0, progressCallback=None):
        return inputStream

def test_accessprovide():
    operator1 = awareness.operator.LocalOperator()
    operator1.affinities.append(TestAffinity(operator1, 0))