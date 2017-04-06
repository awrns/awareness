import awareness


class TestAffinity(awareness.LocalAffinity):

    profile = (1,1)

    def run(self, inputStream, progressFrequency=0, progressCallback=None):
        return inputStream

def test_accessprovide():
    operator1 = awareness.LocalOperator()
    operator1.affinities.append(TestAffinity(operator1, 0))

    operator2 = awareness.RemoteOperator('127.0.0.1', port=1600)
    inputStream = awareness.Stream([awareness.Item([1])])
    with operator2:
        res = operator2.process(0, inputStream)

