import awareness

class TestAffinity(awareness.LocalAffinity):

    inputs = 1
    outputs = 1

    def run(self, input_stream, progress_frequency=0, progress_callback=None):
        return input_stream


def algorithm():
    operator1 = awareness.LocalOperator()
    operator1.affinities.append(TestAffinity(operator1, 0))

    operator2 = awareness.LocalOperator(port=1601)
    operator2.remote_operators.append(awareness.RemoteOperator('127.0.0.1'))


    set = awareness.Set(awareness.Stream([]), awareness.Stream([]))
    set.input_stream.items.append(awareness.Item((1,)))


    with operator2:
        print operator2.search

