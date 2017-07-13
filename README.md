
<a href="#">

![Awareness introduction image](graphics/banner.png)

</a>

```bash
$ pip3 install awareness
$ python3
```
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
