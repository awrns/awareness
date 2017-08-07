
<a href="#">

![Awareness is the networking architecture of the future. It makes each device on the Internet a powerful center of data processing and machine learning. Each device uses the characteristics and quirks of its own human-created software to help other devices solve computational problems without human help. When the bits of software that are already available aren't good enough, Awareness creates new software tidbits using machine learning and then shares them so that other devices can use them too. Designed for data,
from the ground up. Awareness works with whatever data you have, and whatever data you want. No matter what format your application uses, Awareness can handle it. What's more, it can computationally analyze the capabilities of your application in order to help other devices on the Internet solve problems. Deep learning 
built in. Whether you have some LEDs to blink or an autonomous vehicle to navigate, Awareness can do the job. It seamlessly supports both CUDA and OpenCL, and treats trained models in the same way as human-created software, sharing them on the Internet in order to help other devices solve problems. Crafted for prowess
when speed matters. Every element of Awareness is capable of low-latency, high-bandwidth communication. With its unique "zero polling" network architecture ard asynchronous task system, Awareness guarantees that your application will always be able to keep tabs on the progress of its communications. Capable, intuitive
and elegant. Awareness is designed for everyone. You don't have to be a software expert to understand it, but if you're looking to be at the cutting edge of computing, Awareness is happy with that too. No matter what you use it for, Awareness stays out of the way and lets your application do what it does best. ](graphics/banner.png)

</a>

```bash
$ pip3 install awareness
```
###### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;More of a Python 2 person? Awareness is happy with that too.
```bash
$ pip install awareness
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

#### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Awareness will have an exhibit at [World Maker Faire 2017](//makerfaire.com/new-york/) in New York!

<br />

 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="//makerfaire.com/new-york/">
  <img src="http://yydxg3i41b1482qi9hidybgs.wpengine.netdna-cdn.com/wp-content/uploads/2017/06/MF17NY_Badge.png" alt="World Maker Faire New York" width="150" height="150" border="0" />
</a>

<br />
<br />
<br />

<hr />

#### Building from source and contributing
###### If you'd like to mess with the source code a bit and submit a pull request to make Awareness better for everyone, we'd be very grateful. Awareness is developed using the Gradle build system and [PyGradle](https://github.com/linkedin/pygradle). Getting started with a virtualenv-based installation of Awareness is simple:
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
