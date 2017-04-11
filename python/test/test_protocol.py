import awareness


class TestAffinity(awareness.LocalAffinity):

    profile = (1,1)

    def run(self, input_stream, progress_frequency=0, progress_callback=None):
        return input_stream

def test_accessprovide():
    operator1 = awareness.LocalOperator()
    operator1.affinities.append(TestAffinity(operator1, 0))

    operator2 = awareness.RemoteOperator('127.0.0.1', port=1600)
    input_stream = awareness.Stream([awareness.Item((1.0,))])
    with operator2:
        operator2.retrieve_affinities()
        res = operator2.process(0, input_stream)

    assert res.items[0].parameters[0] == 1.0

