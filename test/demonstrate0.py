
import awareness as a

a.backend.NativeBackend.setup_logger()


thisnode = a.LocalOperator('node0.local')
#thisnode = awareness.LocalOperator('127.0.0.1', port=1600)

node1 = a.RemoteOperator('node1.local')
node2 = a.RemoteOperator('node2.local')
#node1 = awareness.RemoteOperator('127.0.0.1', port=1601)
#node2 = awareness.RemoteOperator('127.0.0.1', port=1602)


thisnode.remote_operators = [node1, node2]

thisnode.provider.join()
