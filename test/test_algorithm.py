import awareness

class TestComponent(awareness.LocalComponent):

    inputs = 1
    outputs = 1

    def run(self, input_stream, progress_frequency=0, progress_callback=None):
        out = []
        for item in input_stream.items:
            out += [item[0] + 1,]
        return awareness.Stream(out)


class TestComponent2(awareness.LocalComponent):

    inputs = 1
    outputs = 1

    def run(self, input_stream, progress_frequency=0, progress_callback=None):
        out = []
        for item in input_stream.items:
            out += [item[0] * 2,]
        return awareness.Stream(out)



def test_algorithm():
    operator1 = awareness.LocalOperator(b'127.0.0.1', port=1602)
    operator1.components = [TestComponent()]

    operator2 = awareness.LocalOperator(b'127.0.0.1', port=1603)
    operator2.components = [TestComponent2()]
    operator2.remote_operators.append(awareness.RemoteOperator(b'127.0.0.1', port=1602))


    input_set = awareness.Set(
        awareness.Stream(
            [
                [1,],
                [2,]
            ]
        ),
        awareness.Stream(
            [
                [2,],
                [3,]
            ]
        )
    )

    
    res = operator2.search(1, input_set, 1)

    print(res.operations)

