import awareness


class TestAbility(awareness.ability.LocalAbility):
    def run(self, input):
        return input + 1

def test_localability():
    endp = awareness.endpoint.LocalEndpoint()
    endp.abilities.append(TestAbility(endp, 0, 1, 1))
    assert endp.processData(0, 4) == 5