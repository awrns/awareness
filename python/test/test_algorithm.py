import awareness

class TestComponent(awareness.LocalComponent):

    inputs = 1
    outputs = 1

    def run(self, input_stream, progress_frequency=0, progress_callback=None):
        return input_stream


class TestComponent2(awareness.LocalComponent):

    inputs = 1
    outputs = 1

    def run(self, input_stream, progress_frequency=0, progress_callback=None):
        return awareness.Stream([awareness.Item((100,))] * len(input_stream.items))



def test_algorithm():
    operator1 = awareness.LocalOperator('127.0.0.1', port=1602)
    operator1.components = [TestComponent(operator1, 0)]

    operator2 = awareness.LocalOperator('127.0.0.1', port=1603)
    operator2.components = [TestComponent(operator2, 0)]
    operator2.remote_operators.append(awareness.RemoteOperator('127.0.0.1', port=1602))


    input_set = awareness.Set(awareness.Stream([[1]]), awareness.Stream([[1]]))

    
    res = operator2.search(1, input_set)

    print res.operations

