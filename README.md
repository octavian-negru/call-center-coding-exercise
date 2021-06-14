# call-center-coding-exercise
Simulating some call-center interactions, considering real-life situations, with real-life like actors.
The actors which interact in the current project are of two types:
 - InsuranceAgents
 - Consumers

There are 1000 Consumers and 20 InsuranceAgents.

## Behavioral traits
- Consumers:
    - The Consumers can make calls (in the present code, they call one single method) in order to reach to an agent.
    - Consumers can receive calls, but they are busy 80% of the time, so they cannot receive calls at those times and if that’s the case an agent has to try calling again at a later time.

- Agents:
    - Agents can receive calls from the Consumers
    - Agents can make outbound calls to consumers that have called before.
    - Each agent should be assigned to handle certain type of consumers that meet a range or value of the attributes
    - Voice mail inbox per agent exists. If a consumer calls and there are no agents available to answer because they are all busy, then calls are saved to the voicemail inbox for the best matched agent so that the agent can call back with the consumer’s saved phone number.

  
## How to build/run the project
 - build: `./build.sh`
 - run: `./run.sh`
- see coverage percent: `pytest --cov`

