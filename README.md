# Audio Position Controller

*This project uses Deepgram speech to text API to create a controller for software/mechanical systems (here the control for the snake in the [classic snake game](https://theprint.in/features/nokias-snake-the-mobile-game-that-became-an-entire-generations-obsession/462873/)). Applications include Voice controlled wheelchairs, emulators for games with audio keys, etc.*

## This Project was contributed to the [Cambridge Hackathon](https://hackcambridge.com) held on 22-23 January 2022

[Link to Devpost Submission](https://devpost.com/software/audio-position-controller)

System Requirements: Python 3.x

Libraries Required: ```pygame, time, random, sounddevice, deepgram, asyncio, json, soundfile, os```

API: [Deepgram](https://deepgram.com/)

Can be installed using ```pip install <library-name>```

## Instructions 
- Clone this repository/fork it on to your local pc
- Modify ```Line 43``` in ```audio_controller.py```, replace this with your API-KEY obtained after creating an account on [Deepgram](https://deepgram.com/)

```python
DEEPGRAM_API_KEY = 'ENTER YOUR API KEY HERE'
```

- Run the python script using 
```bash
python audio_controller.py
```
- Now verbally speak out when you notice see ```Speak Now:``` in the terminal output. Stop speaking when you see ```Don't Speak Now:``` in the output.
- Commands you can speak out : ```UP, DOWN, LEFT, RIGHT``` to make the snake go UP, DOWN, LEFT and RIGHT respectively.
- The snake will now follow your commands. The game works like the classic snake game, eat the white pixels(food) and do not crash the wall or yourself. 

## Improvements and Future Work
(We couldn't implement these given the finite time constraint of the hackathon, but we'd love to)
- We can build an emulator where more games with common keys can run via audio instructions.
- Currently the only way to terminate the game is by crashing on to the wall. An endgame button GUI implementation can be further worked on.
- Since the recording and snake motion are sequential, they need to happen one at a time. This causes lag. If parallel processing is used to run both the processes concurrently the lag can be significantly reduced.
- The ```Speak Now:``` and ```Don't Speak Now:``` alerts appear in the terminal output. Addition of a GUI (Maybe Mute/Unmute icons) to make these visible on the main screen would allow the user to when to speak and when not to.

### Team members:
- [Rohan Kalbag](https://github.com/rohankalbag)
- [Aabir Lal Biswas](https://github.com/the-flyinggoat)
- [Kalp Vyas](https://github.com/kalp121212)
- [Hastyn Doshi](https://github.com/Hastyn)
