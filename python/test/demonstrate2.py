
import awareness

thisnode = awareness.LocalOperator('node2.local')


class TestAffinity2(awareness.LocalAffinity):

    inputs = 1
    outputs = 1

    def run(self, input_stream, progress_frequency=0, progress_callback=None):
        return awareness.Stream([awareness.Item((345,))] * len(input_stream.items))


thisnode.affinities = [TestAffinity2(thisnode, 0)]

thisnode.provider.join()