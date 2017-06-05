import awareness

class TestComponent(awareness.LocalComponent):

    inputs = 1
    outputs = 2

    def run(self, input_stream, progress_frequency=0, progress_callback=None):
        return awareness.Stream([[1, 2],])


class TestComponent2(awareness.LocalComponent):

    inputs = 1
    outputs = 2

    def run(self, input_stream, progress_frequency=0, progress_callback=None):
        return awareness.Stream([[255, 255],])



def test_algorithm():
    operator1 = awareness.LocalOperator('127.0.0.1', port=1602)
    operator1.components = [TestComponent()]

    operator2 = awareness.LocalOperator('127.0.0.1', port=1603)
    operator2.components = [TestComponent2()]
    operator2.remote_operators.append(awareness.RemoteOperator('127.0.0.1', port=1602))


    input_set = awareness.Set(awareness.Stream([[1,],]), awareness.Stream([[1, 2],]))

    
    res = operator2.search(1, input_set)

    print res.operations

