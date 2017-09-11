
<a href="#">

![Awareness is the networking architecture of the future. It makes each device on the Internet a powerful center of data processing and machine learning. Each device uses the characteristics and quirks of its own human-created software to help other devices solve computational problems without human help. When the bits of software that are already available aren't good enough, Awareness creates new software tidbits using machine learning and then shares them so that other devices can use them too. Designed for data,
from the ground up. Awareness works with whatever data you have, and whatever data you want. No matter what format your application uses, Awareness can handle it. What's more, it can computationally analyze the capabilities of your application in order to help other devices on the Internet solve problems. Deep learning 
built in. Whether you have some LEDs to blink or an autonomous vehicle to navigate, Awareness can do the job. It seamlessly supports both CUDA and OpenCL, and treats trained models in the same way as human-created software, sharing them on the Internet in order to help other devices solve problems. Crafted for prowess
when speed matters. Every element of Awareness is capable of low-latency, high-bandwidth communication. With its unique "zero polling" network architecture ard asynchronous task system, Awareness guarantees that your application will always be able to keep tabs on the progress of its communications. Capable, intuitive
and elegant. Awareness is designed for everyone. You don't have to be a software expert to understand it, but if you're looking to be at the cutting edge of computing, Awareness is happy with that too. No matter what you use it for, Awareness stays out of the way and lets your application do what it does best. ](graphics/banner.png)

</a>

###### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Check out [the documentation](https://github.com/awrns/awareness/wiki/Awareness-Documentation) if you're confused by this tutorial.

```bash
$ pip3 install awareness
$ python3
```

```python

>>> import awareness as a

>>> # Let's make a simple Component that does something with data.

>>> class AdderComponent(a.LocalComponent):
...     inputs = 2 # We'll take two numerical inputs
...     outputs = 1 # and produce one numerical output.
...
...     def run(self, input, progress_callback=None):
...         output = []
...         for item in input.items:
...             value1 = item[0] # The first of the two numerical inputs
...             value2 = item[1] # The second
...             output.append([value1 + value2]) # Let's just add them.
...         return a.Stream(output)
...

>>> # Now let's put it on the network using an Operator.

>>> operator = a.LocalOperator(b'192.168.1.2') # The IP address of this computer 
>>> operator.components.append(AdderComponent())

>>> # Now let's make another Operator on the same network.
>>> # You'll need to switch to a different computer now.

>>> operator2 = a.LocalOperator(b'192.168.1.3') # The IP address of this other computer
>>> # It should know about the other Operator that we created earlier on 192.168.1.2.
>>> operator2.remote_operators.append(a.RemoteOperator(b'192.168.1.2'))

>>> # Now, we'll make some 'examples' of data that our AdderComponent should be able to handle.

>>> example1 = [2, 2]
>>> result1 = [4]
>>> example2 = [3, 1]
>>> result2 = [4]
>>> example3 = [1, 1]
>>> result3 = [3]
>>> examples = a.Set(
...     a.Stream([example1, example2, example3]),
...     a.Stream([result1, result2, result3])
... )

>>> # Let's feed that to the new operator2 on 192.168.1.3.
>>> # It will research which Component on the network is best.
>>> # (The result should be our AdderComponent on 192.168.1.2.)

>>> suggestion = operator2.search(1, examples, 2)
>>> print(suggestion.operations)
[(b'192.168.1.2', 1600, 0, 0, 0)]

>>> # It knows that the AdderComponent is probably a good fit for our examples! Let's try it:

>>> result = suggestion.run(a.Stream([example1, example2, example3]))
>>> result = result.extract(0, 1) # Restrict the result to just one output for readability
>>> print(result.items)
[[4]
 [4]
 [3]]

>>> # That's very cool. Imagine how easy it might be to find solutions to computational problems
>>> # if all software was in the form of Components!

```

<br />
<br />

#### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Ready? Head over to [the Awareness documentation](https://github.com/awrns/awareness/wiki/Awareness-Documentation) to learn a lot more.

<br />
<br />
<br />

#### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;You can also ask questions and give feedback [on Gitter](https://gitter.im/awrns/Lobby) if you'd like.
#### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Seriously - if you're interested, please go there and say hi. Or, send [Aedan](https://github.com/aedancullen) an email.

<br />

#### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Awareness will also have an exhibit at [World Maker Faire 2017](//makerfaire.com/new-york/) in New York!

<br />


<br />
<br />
<br />

<hr />

#### Building from source and contributing
###### If you'd like to mess with the source code a bit and submit a pull request to make Awareness better for everyone, we'd be very grateful. Awareness is still a young project, and pull requests are welcome. You can head over [to Gitter](https://gitter.im/awrns/Lobby) to discuss changes and improvements too.
###### Awareness is developed using the Gradle build system and [PyGradle](https://github.com/linkedin/pygradle). Getting started with a virtualenv-based installation of Awareness is simple:
```bash
$ git clone https://github.com/awrns/awareness
$ cd awareness
$ ./gradlew build
```
###### Now, you can type
```bash
$ source activate
```
###### and `python3` will become a virtual Python installation with Awareness available. When you're finished, just type
```bash
$ deactivate
```
###### to leave the virtual environment. Of course, if you do make any changes to the code located in the `src/awareness` directory, don't forget to re-run `./gradlew build` in the root of the repository before re-activating the virtual environment.

<br />

#### Licensing
###### Awareness is distributed under the GNU Lesser General Public License. More details are in the files COPYING and COPYING.LESSER. Copyright (c) 2016-2017 Aedan S. Cullen.


