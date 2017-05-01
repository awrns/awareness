
import awareness as a

a.backend.NativeBackend.setup_logger()


thisnode = a.LocalOperator('node2.local')
#thisnode = awareness.LocalOperator('127.0.0.1', port=1602)

class TestAffinity2(a.LocalAffinity):

    inputs = 1
    outputs = 1

    def run(self, input_stream, progress_frequency=0, progress_callback=None):
        return a.Stream([a.Item((345,))] * len(input_stream.items))


thisnode.affinities = [TestAffinity2(thisnode, 0)]

thisnode.provider.join()
