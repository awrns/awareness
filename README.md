
<a href="#">

![A new way to think about data on the Internet, like nothing ever before. Computers can program themselves now. Well, somewhat. Awareness represents the data-processing capabilities of each device on the Internet as a set of numerical inputs and outputs. This way, its crazy new algorithm can solve computational problems automatically by forming an optimal "pipeline" of processing steps available on the network. Designed for data,
from the ground up. Awareness works with whatever data you have, and whatever data you want. No matter what format your application uses, Awareness can handle it. What's more, it can computationally analyze the capabilities of your application in order to help other devices on the Internet solve problems. Capable, intuitive
and elegant. Awareness is designed for everyone. You don't have to be a software expert to use it and understand it, but if scientific computing is your thing, Awareness is happy with that too. No matter what you use it for, Awareness stays out of the way and lets your application do what it does best. Crafted for prowess
when speed matters. Every element of Awareness is capable of low-latency, high-bandwidth communication. With its unique "zero polling" network architecture ard asynchronous task system, Awareness guarantees that your application will always be able to keep tabs on the progress of its communications. Open to the 
world's creations. For Awareness's crazy new algorithm to work, we need software developers everywhere to come on board and connect their applications to this crazy new system. It'll be interesting and fun. And maybe the future of the Internet will appear along the way. Let's go.](graphics/banner.png)

</a>

```bash
$ pip3 install awareness
$ python3
```
###### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;More of a Python 2 person? Awareness is happy with that too.
```bash
$ pip install awareness
$ python
```

<br />

```python
>>> import awareness as a
>>>
```

<br />
<br />

#### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Ready? Head over to [the Awareness documentation](https://github.com/awrns/awareness/wiki/Awareness-Documentation) to learn a lot more.

<br />

#### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;You can also ask questions and give feedback [on Gitter](https://gitter.im/awrns/Lobby) if you'd like.

<br />
<br />
<br />
<br />
<br />
<br />

<hr />

#### Building from source and contributing
###### If you'd like to mess with the source code a bit and submit a pull request to make Awareness better for everyone, we'd be very grateful. Awareness is developed using the Gradle build system and [PyGradle](https://github.com/linkedin/pygradle). Getting started with a virtualenv-based installation of Awareness is simple:
```bash
$ sudo apt install python3 python3-dev libopenblas-dev
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
