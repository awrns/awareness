
import awareness

thisnode = awareness.LocalOperator('node0.local')

node1 = awareness.RemoteOperator('node1.local')
node2 = awareness.RemoteOperator('node2.local')

thisnode.remote_operators = [node1, node2]