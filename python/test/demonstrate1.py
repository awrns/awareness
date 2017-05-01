
import awareness

#thisnode = awareness.LocalOperator('node1.local')
thisnode = awareness.LocalOperator('127.0.0.1', port=1601)

class TestAffinity1(awareness.LocalAffinity):

    inputs = 1
    outputs = 1

    def run(self, input_stream, progress_frequency=0, progress_callback=None):
        return input_stream


thisnode.affinities = [TestAffinity1(thisnode, 0)]

thisnode.provider.join()
