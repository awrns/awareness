import awareness


class TestAbility(awareness.ability.LocalAbility):
    def run(self, input, progressCallback=None):
        output = [None] * len(self.profile)
        output[0] = input[0] + 1
        return output

def test_localability():
    op = awareness.operator.LocalOperator()
    op.abilities.append(TestAbility(op, 0, [(0, 1)]))
    assert op.process(0, [4]) == [5]
