# Dissonance

Dissonance is a Discord-based **Command-and-Control proof of concept** designed to demonstrate how real-world Command-and-Control systems can operate using a messaging platform as their communication layer.

The project is **not intended to showcase malware or host malicious functionality**. It is a simplified demonstration of concepts that can be found in real-world systems, implemented within an isolated Docker environment for educational purposes.

The project consists of lightweight agents running inside isolated Docker containers. Each agent connects to Discord, identifies itself, receives module requests, runs the selected module and communicates the results back through Discord.

The project is intended to demonstrate the basic architecture and communication flow of a Command-and-Control system rather than provide a fully featured framework.


## Features

* Discord used as the communication layer
* Multiple Docker containers running the agents
* Automatic agent channel creation
* Agent status panel
* Dynamic module loading
* Module buttons generated automatically
* Modules can be added or removed through Discord
* Centralised activity logging
* Separate channel for each agent
* Isolated Docker lab environment

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
                         whoami.py
```

## Modules

Currently available modules are:

* `whoami.py`

Modules are stored in the `#modules` Discord channel as Python file attachments.

When a module is added, edited or removed, the agents detect the change and update their control panels automatically.

## Agent

Each Docker container runs `Agent.py`.

The agent is responsible for:

* Connecting to Discord
* Identifying the machine
* Creating or finding its agent channel
* Discovering available modules
* Displaying the control panel
* Running selected modules
* Logging activity

The agent does not contain the implementation of individual modules. Modules are kept separate from the agent and handle their own functionality and communication.

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
      Module downloaded
            │
            ▼
       Module executed
            │
            ▼
    Module sends its result
        through Discord
```

## Docker Lab

The agents are designed to run inside Docker containers.

```text
Lab/
├── Docker-01/
│   └── Dockerfile
└── Docker-02/
    └── Dockerfile
```

This provides isolated environments for testing multiple agents without running the agents directly on the host system.

## How To Use

### Requirements

* Python 3
* Docker
* A Discord bot
* A Discord server for the lab

### Clone The Repository

```bash
git clone https://github.com/Cn-54/Dissonance.git
cd Dissonance
```

### Discord Bot Setup

Create a Discord bot and add it to a test Discord server.

The bot requires the necessary permissions to:

* Create and manage channels
* Send messages
* Read messages
* Attach and edit messages

The **Message Content Intent** must also be enabled for the bot.

### Environment Variables

The agents require two environment variables:

```bash
export DISCORD_TOKEN="your-bot-token"
export GUILD_ID="your-server-id"
```

The token should not be placed directly inside the source code or committed to the repository.

### Build The Docker Images

The included `build.sh` script builds all Docker images found under `Lab/`:

```bash
chmod +x build.sh
./build.sh
```

The script automatically finds each `Docker-*` directory and builds an image using its Dockerfile.

### Start The Agents

Copy the example run script:

```bash
cp run.sh.example run.sh
```

Make the script executable:

```bash
chmod +x run.sh
```

Make sure the required environment variables are set:

```bash
export DISCORD_TOKEN="your-bot-token"
export GUILD_ID="your-server-id"
```

Then start the agents:

```bash
./run.sh
```

Each Docker container will start an agent and connect to the Discord server.

The agents will create their own channels under the `AGENTS` category.

### Using Modules

Modules can be added through the Discord `#modules` channel by uploading a Python file.

Once uploaded, the agents detect the new module and add it to their control panels.

For example:

```text
#modules
    │
    └── whoami.py
          │
          ▼
      Agent detects module
          │
          ▼
      Control panel updates
          │
          ▼
      [whoami.py]
```

Selecting a module from an agent's control panel runs that module inside the corresponding Docker container.

The module then sends its output back to the agent's Discord channel.

### Stopping The Agents

The included `stop.sh` script stops and removes the running agent containers:

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
│   └── whoami.py
├── build.sh
├── requirements.txt
├── run.sh.example
└── stop.sh
```

## Security

A malicious Command-and-Control system using Discord could still be detected through a combination of host and network indicators.

### Detection

* Unexpected applications connecting to Discord
* Long-running Python processes on systems where they are not normally used
* Unusual outbound connections from servers or workstations
* Unexpected processes communicating with external services
* Suspicious process activity occurring alongside external network communication

### Mitigation

* Monitor outbound network connections
* Restrict unnecessary access to external messaging services
* Use endpoint monitoring to identify unexpected processes
* Log DNS, proxy and firewall activity
* Investigate systems showing unusual combinations of process and network activity

Using a legitimate service such as Discord does not make the activity invisible; it changes what defenders need to look for.

## Scope

Dissonance is a **proof of concept for educational and controlled laboratory use**.

The project intentionally does not implement:

* Persistence
* Evasion
* Credential theft
* Privilege escalation
* Destructive functionality

These features were intentionally not implemented to avoid turning the project from an educational PoC into working malware.

The agents are designed to be as observable as possible. Agent activity is extensively logged both through Discord and directly within the Docker containers. This makes it possible to see what the agents are doing while they are running and makes the behaviour easier to understand and analyse.

The project is also accompanied by documentation explaining how the different components work and how they communicate with each other. The intention is for the behaviour and architecture of the agents to be as clear and transparent as possible.

The agents are intended to run within the provided Docker lab environment and are intentionally designed not to run without the required environment variables.

## Disclaimer

Dissonance is an educational proof of concept designed to demonstrate Command-and-Control concepts within **controlled Docker lab environments**.

The project is **not designed or intended for use in real-world systems, production environments, or against systems without explicit authorisation**. It should only be run within an isolated environment where the operator has full control over the systems involved.

The author is **not responsible or liable for any damage, misuse, data loss, security issues, or other consequences resulting from the use or misuse of this project**. Users are responsible for ensuring that the project is only used in appropriate and authorised environments.
