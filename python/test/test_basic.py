import awareness


class TestAffinity(awareness.affinity.LocalAffinity):
    def run(self, input, progressFrequency=0, progressCallback=None):
        output = [None] * len(self.profile)
        output[0] = input[0] + 1
        return output

def test_localability():
    op = awareness.operator.LocalOperator()
    op.affinities.append(TestAffinity(op, 0, [(0, 1)]))
    assert op.process(0, [4]) == [5]
