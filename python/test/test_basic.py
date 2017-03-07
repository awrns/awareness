import awareness


class TestAbility(awareness.ability.LocalAbility):
    def run(self, input):
        output = [None] * len(self.profile)
        output[0] = input[0] + 1
        return output

def test_localability():
    endp = awareness.endpoint.LocalEndpoint()
    endp.abilities.append(TestAbility(endp, 0, [(0, 1)]))
    assert endp.process(0, [4]) == [5]