import awareness


class TestComponent(awareness.LocalComponent):

    inputs = 1
    outputs = 1

    def run(self, input_stream, progress_frequency=0, progress_callback=None):
        return input_stream

def test_accessprovide():
    operator1 = awareness.LocalOperator('127.0.0.1')
    operator1.components = [TestComponent()]

    operator2 = awareness.RemoteOperator('127.0.0.1', port=1600)
    input_stream = awareness.Stream([[255]])
    with operator2:
        operator2.retrieve_components()
        res = operator2.process(0, input_stream)

    assert res.items[0][0] == 255

