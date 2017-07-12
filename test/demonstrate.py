
import awareness as a

a.backend.NativeBackend.setup_logger()


node0 = a.RemoteOperator('node0.local')


input_stream = a.Stream([a.Item((1,))])
output_stream = a.Stream([a.Item((1,))])
input_set = a.Set(input_stream, output_stream)

with node0:
    print(node0.search(1, input_set).operations)
