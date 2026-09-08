# Dissonance

Dissonance is a Discord-based **Command-and-Control proof of concept** designed to demonstrate how messaging platforms can be used as a communication layer between agents and a controller.

The project is a simplified and educational demonstration of concepts found in real-world Command-and-Control systems. It runs within isolated Docker containers and is designed to be observable and easy to analyse.

## Features

* Discord used as the communication layer
* Multiple Docker agents
* Automatic agent channel creation
* Agent status panel
* Dynamic module discovery
* Module buttons generated automatically
* Centralised activity logging
* Separate channel for each agent
* Docker-based lab environment

## Architecture

```text
                         Discord
                            │
              ┌─────────────┼─────────────┐
              │             │             │
          #modules       #agents        #logs
              │             │             │
              │       ┌─────┴─────┐       │
              │       │           │       │
              │    Docker-01   Docker-02  │
              │       │           │       │
              └───────┴───────────┴───────┘
                              │
                           Agents
                              │
                        Module loader
                              │
                       Module contents
```

## Modules

Modules are stored in the Discord `#modules` channel as `.txt` files.

Agents automatically discover the available modules and create a button for each one in their control panel.

Selecting a module loads its contents and displays them in the agent's Discord channel.

### Module execution

The original design allowed Python modules to be downloaded and executed by the agents.

This functionality was intentionally removed because executable modules could give the project potential dual-use as a malware framework.

Modules are now stored as text files and **their contents are displayed rather than executed**.

This keeps the project focused on demonstrating:

* Module discovery
* Module loading
* Command-and-Control communication
* Agent management
* Discord-based communication

without providing arbitrary code execution.

## Agent

Each Docker container runs `Agent.py`.

The agent is responsible for:

* Connecting to Discord
* Identifying the machine
* Creating or finding its agent channel
* Discovering available modules
* Displaying the control panel
* Loading module contents
* Logging activity

The agent does not execute module code.

## Module Flow

```text
Module uploaded to Discord
            │
            ▼
       Agent detects it
            │
            ▼
      Module registry
            │
            ▼
      Control panel
            │
            ▼
      Module selected
            │
            ▼
      Module contents loaded
            │
            ▼
    Contents displayed in
       agent channel
```

## Docker Lab

The agents run inside Docker containers to provide isolated environments for testing.

```text
Lab/
├── Docker-01/
│   └── Dockerfile
└── Docker-02/
    └── Dockerfile
```

## Setup

### Requirements

* Python 3
* Docker
* A Discord bot
* A Discord server for the lab

### Clone

```bash
git clone https://github.com/Cn-54/Dissonance.git
cd Dissonance
```

### Environment Variables

Set the required environment variables:

```bash
export DISCORD_TOKEN="your-bot-token"
export GUILD_ID="your-server-id"
```

The Discord token should never be committed to the repository.

### Discord Bot

Create a Discord bot and add it to a test server.

The bot requires permissions to:

* Create and manage channels
* Send messages
* Read messages
* Attach and edit messages

The **Message Content Intent** must also be enabled.

### Build

```bash
chmod +x build.sh
./build.sh
```

### Start

Copy the example script:

```bash
cp run.sh.example run.sh
chmod +x run.sh
```

Set the environment variables and start the agents:

```bash
./run.sh
```

Each container will start an agent and create its own channel under the `AGENTS` category.

### Stop

```bash
chmod +x stop.sh
./stop.sh
```

## Project Structure

```text
.
├── Agent
│   └── Agent.py
├── Lab
│   ├── Docker-01
│   │   └── Dockerfile
│   └── Docker-02
│       └── Dockerfile
├── Modules
│   └── whoami.txt
├── build.sh
├── requirements.txt
├── run.sh.example
└── stop.sh
```

## Security

A malicious Command-and-Control system using a legitimate service such as Discord could still produce detectable host and network activity.

Possible indicators include:

* Unexpected applications communicating with Discord
* Unusual outbound network connections
* Unexpected long-running processes
* Suspicious combinations of process and network activity

Possible defensive measures include:

* Monitoring outbound connections
* Endpoint monitoring
* DNS, proxy and firewall logging
* Restricting unnecessary access to external messaging services

Using a legitimate service as a communication layer does not make activity invisible; it changes what defenders need to monitor.

## Scope

Dissonance is intended strictly for **educational and controlled laboratory use**.

The project intentionally does not implement:

* Module code execution
* Persistence
* Evasion
* Credential theft
* Privilege escalation
* Destructive functionality

The agents are designed to be observable, with activity logged through Discord and within the Docker containers.

The module system uses text files rather than executable Python modules. This was a deliberate design decision to prevent the project from becoming a potentially usable malware framework while retaining the architectural concepts being demonstrated.

## Disclaimer

Dissonance should only be used within controlled environments where the operator has full authorisation over the systems involved.

The project is not intended for use against real-world systems, production environments, or systems without explicit authorisation.
