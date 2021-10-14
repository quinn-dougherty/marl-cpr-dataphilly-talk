# [DataPhilly talk: multiagent reinforcement learning in common pool resource problems](https://www.meetup.com/DataPhilly/events/281132668)

Slides: `marl-cpr-talk.odp` right here in this repo. 

## _Fork this repo to do exercises, steal it's skeletal parts for template or starter code in a project, etc._

## [Auxiliary repo](https://github.com/RedTachyon/cpr_reputation/) joint work with Ben Greenberg and Ariel Kwiatkowski. 

This is a little harder, once you grok all the concepts in the talk and this repo head over there to keep learning.

# Meetup.com text

Event Schedule:
1. Meeting opens at 5:45pm
2. Introductions (Starts at 6pm)
3. Speaker Event
4. Networking Event (30 minutes)

Speaker Event
Topic: Multi-Agent Reinforcement Learning: Dodging Tragedy of the Commons with Simple Mechanisms
Speaker: Quinn Dougherty

Some problems can be described in terms of states, actions, and rewards. A computer program that maximizes rewards in such an environment by selecting actions is called an agent, and the study of these agents is called reinforcement learning. You can select actions with deep learning, leading the research community to advances in playing Go and autonomous vehicles. Naturally, problems and environments arise that are best thought of as a confluence of two or more such agents, the study of which is called multi-agent reinforcement learning. Meanwhile, over in economics, common pool resources are studied as an approximate prisoner's dilemma: if the collective harvests too much, everyone loses, yet if any individual unilaterally implements a sustainable policy others are incentivized not to follow suit. In the literature this is called tragedy of the commons, but economist Elinor Ostrom took an empirical approach [2][3] and found emergent mechanisms all over the world that caused communities to dodge this outcome. You're asking a natural question: do we want to simulate these environments with multi-agent reinforcement learning, simulate a mechanism suggested by Ostrom, and observe if our agents can dodge tragedy of the commons? In this talk, we will discuss my team's journey through this research question and observe the surprisingly easy interface to Ray's RLlib library [4] for training agents to play multi-player games in python. There will be a follow-along repo, if not a notebook.

[1] https://www.lesswrong.com/posts/LBwpubeZSi3ottfjs/aisc5-retrospective-mechanisms-for-avoiding-tragedy-of-the
[2] https://www.amazon.com/Governing-Commons-Evolution-Institutions-Collective/dp/1107569788/ref=sr_1_1?dchild=1&keywords=governing+the+commons&qid=1632844671&sr=8-1
[3] https://en.wikipedia.org/wiki/Elinor_Ostrom#Design_principles_for_Common_Pool_Resource_(CPR)_institution
[4] https://docs.ray.io/en/latest/rllib.html

Speaker Bio:
Quinn Dougherty is a logician at platonic.systems, working on auditing a new decentralized finance project for the Cardano ecosystem and on formal verification. Previously he was a research intern at the Stanford Existential Risks Initiative profiling how the AGI Safety and Alignment research community should prioritize multi-stakeholder and/or multi-agent scenarios. In 2020 he worked on the hospital traffic forecasting app CHIME and did some python and cloud security work for a startup. Quinn is also a coorganizer at Effective Altruism Philadelphia. More information including socials and contact at quinnd.net.

Networking event:
Join us after the talk for a chance to chat with Quinn and network with the other members of the DataPhilly community.

# Usage

CI (more on that below) checks pythons 3.6-3.10. As of this writing (10-13) I haven't checked that they all work. 3.8 or 3.9 is gonna be your safest bet.

## Build env 
```
$ nix-build
```
Enter its virtual world with 
```
$ nix-shell
```

That's what I use for the talk. `Nix` isn't a huge deal in data science ecosystems, so you can safely ignore it (but it is a great tool). You can use any virtualization you want and `requirements.txt` should work. I think there's something broken in the `environment.yaml` so if you want to use `conda` you're on your own (do submit a pull request if you get a working `environment.yaml`, tho).

## Validate
```
$ flake8 .
$ pytype .
$ pytest
```

## Run
```
$ python main.py --help
usage: main.py [-h] [--game GAME] [--n N]

Learn to play games with ray.

optional arguments:
  -h, --help   show this help message and exit
  --game GAME  g for guessinggame, rps for rockpaperscissors
  --n N        if game==g then n is observation/action size, if game==rps then n-1 is number of agents.
```
## Guide to the repo

I put some stuff in this repo that you should know about. Yes it has minimal examples for the purposes of the talk, but I also wanted to take this opportunity to soapbox about things that have added value in every situation, OSS or professional, I've ever been in. Even though they're all things that weren't in my training and that I had to teach myself.

### Property-based testing
Read files in `test/property/`. The library is called `hypothesis`, it's important. It generates scores unit tests and provides an operation called "shrinking" to make it's randomness reveal the maximum information about the pathologies of your code. If you don't know what unit tests are, you have to know that; but if you only know what unit tests are, you need to know property tests too.

As of this writing (10-12) I haven't tested `rockpaperscissors` adequately, as the astute reader may point out.

### Type hints and `pytype` 
Python's "type system" if you can call it that occasionally identifies bugs for you, if you use it! `pytype` is the command line tool that emits warnings when you've made a misstep in logic.

### CI: cloud jobs that can check your code. 

in `.github/workflows/` there's a file. Read it. It describes a "job" that happens in the github cloud. That way every time I push to github I can check across different python versions that my code works at least well enough to pass lint, typechecking, and testing.
