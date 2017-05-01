
import awareness as a

node0 = a.RemoteOperator('127.0.0.1', port=1600)


input_stream = a.Stream([a.Item((1,))])
output_stream = a.Stream([a.Item((1,))])
input_set = a.Set(input_stream, output_stream)

with node0:
    print node0.search(1, input_set).operations
