[[_TOC_]]

![Coverage](https://gitlab.ics.muni.cz/cryton/cryton-worker/badges/master/coverage.svg)

# Cryton Worker

## Description
Cryton Worker is used for executing attack modules remotely. It utilizes [RabbitMQ](https://www.rabbitmq.com/) 
as its asynchronous remote procedures call protocol. It connects to the Rabbit MQ server and consumes messages from 
the Core component or any other app that implements its [RabbitMQ API](#rabbit-api).

To be able to execute attack scenarios, you also need to install **[Cryton Core](https://gitlab.ics.muni.cz/cryton/cryton-core)** 
(or your custom tool that implements Worker's API). 
Modules provided by Cryton can be found [here](https://gitlab.ics.muni.cz/cryton/cryton-modules).

Cryton toolset is tested and targeted primarily on **Debian** and **Kali Linux**. Please keep in mind that 
**only the latest version is supported** and issues regarding different OS or distributions may **not** be resolved.

[Link to the documentation](https://cryton.gitlab-pages.ics.muni.cz/cryton-documentation/).

## Settings
Cryton Worker uses environment variables for its settings. Please update them to your needs.

| name                               | value   | example                          | description                                                                                                                                                              |
|------------------------------------|---------|----------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| CRYTON_WORKER_NAME                 | string  | my_worker1                       | Unique name used to identify the Worker.                                                                                                                                 |
| CRYTON_WORKER_MODULES_DIR          | string  | /path/to/cryton-modules/modules/ | Path to the directory containing the modules.                                                                                                                            |
| CRYTON_WORKER_DEBUG                | boolean | false                            | Make Worker run with debug output.                                                                                                                                       |
| CRYTON_WORKER_INSTALL_REQUIREMENTS | boolean | true                             | Install requirements.txt for each module on startup.                                                                                                                     |
| CRYTON_WORKER_CONSUMER_COUNT       | int     | 7                                | Number of consumers used for Rabbit communication <br> (more equals faster request processing and heavier processor usage).                                              |
| CRYTON_WORKER_PROCESSOR_COUNT      | int     | 7                                | Number of processors used for internal requests <br> (more equals faster internal requests processing, but heavier processor usage).                                     |
| CRYTON_WORKER_MAX_RETRIES          | int     | 3                                | How many times to try to re-connect when the connection is lost.                                                                                                         |
| CRYTON_WORKER_MSFRPCD_HOST         | str     | localhost                        | Metasploit Framework RPC host.                                                                                                                                           |
| CRYTON_WORKER_MSFRPCD_PORT         | int     | 55553                            | Metasploit Framework RPC port.                                                                                                                                           |
| CRYTON_WORKER_MSFRPCD_SSL          | boolean | true                             | Use SSL to connect to Metasploit Framework RPC.                                                                                                                          |
| CRYTON_WORKER_MSFRPCD_USERNAME     | string  | msf                              | Username for Metasploit Framework RPC login.                                                                                                                             |
| CRYTON_WORKER_MSFRPCD_PASSWORD     | string  | toor                             | Password for Metasploit Framework RPC login.                                                                                                                             |
| CRYTON_WORKER_RABBIT_HOST          | string  | 127.0.0.1                        | RabbitMQ server host.                                                                                                                                                    |
| CRYTON_WORKER_RABBIT_PORT          | int     | 5672                             | RabbitMQ server port.                                                                                                                                                    |
| CRYTON_WORKER_RABBIT_USERNAME      | string  | admin                            | Username for RabbitMQ server login.                                                                                                                                      |
| CRYTON_WORKER_RABBIT_PASSWORD      | string  | mypass                           | Password for RabbitMQ server login.                                                                                                                                      |
| CRYTON_WORKER_EMPIRE_HOST          | string  | 127.0.0.1                        | Empire server host.                                                                                                                                                      |
| CRYTON_WORKER_EMPIRE_PORT          | int     | 1337                             | Empire server port.                                                                                                                                                      |
| CRYTON_WORKER_EMPIRE_USERNAME      | string  | empireadmin                      | Username for Empire server login.                                                                                                                                        |
| CRYTON_WORKER_EMPIRE_PASSWORD      | string  | password123                      | Password for Empire server login.                                                                                                                                        |
| CRYTON_WORKER_APP_DIRECTORY        | string  | ~/.local/cryton-worker/          | Path to the Cryton Worker directory. **(do not change/set/export, if you don't know what you're doing)** <br> If changed, update the commands in this guide accordingly. |

To save the settings **create an app directory**:
```shell
mkdir ~/.local/cryton-worker/
```

The directory will be also used to store logs and other data created by Cryton Worker.  
**This doesn't apply to the Docker installation.** It will be available in the same directory as the Dockerfile 
(`/path/to/cryton-worker/cryton-worker`).

Next, we download example settings (**change the version to match the app version - versions can be found [here](https://gitlab.ics.muni.cz/cryton/cryton-worker/-/tags)**):
```shell
curl -o ~/.local/cryton-worker/.env https://gitlab.ics.muni.cz/cryton/cryton-worker/-/raw/<version>/.env
```
Update these settings to your needs.

### Overriding the settings
**NOTICE: This doesn't apply to the Docker Compose installation.**

To override the persistent settings, you can set/export the variables yourself using the **export** command 
(use **unset** to remove the variable). For example:
```shell
export CRYTON_WORKER_NAME=my_worker1
```

Some environment variables can be overridden in CLI. Try using `cryton-worker --help`.

### Setting up modules
To be able to **execute** (validate) **attack modules** you must download them into one directory. Then update 
`CRYTON_WORKER_MODULES_DIR` environment variable to point to the correct location. If you're using the provided modules 
from the [modules' repository](https://gitlab.ics.muni.cz/cryton/cryton-modules), then the variable 
will look similar to this `CRYTON_WORKER_MODULES_DIR=/path/to/cryton-modules/modules/`.

Modules are hot-swappable, which means the modules don't have to be present at startup. 
This is especially useful for development but **not recommended for production**.

Modules directory example:
```
tree $CRYTON_WORKER_MODULES_DIR
CRYTON_WORKER_MODULES_DIR/
├── mod_hydra
│   └── mod.py
└── mod_cmd
    └── mod.py
```

## Prerequisites
Worker can run without these prerequisites. However, they are **highly recommended** since they allow Worker to use all of its functionality.
- [Metasploit Framework](https://docs.metasploit.com/docs/using-metasploit/getting-started/nightly-installers.html) allows using Metasploit sessions and MSF listeners.
- [Empire post-exploitation framework](https://bc-security.gitbook.io/empire-wiki/quickstart/installation) allows deployment and interaction with Empire agents.

Additionally, to start the MSF as a service follow [this guide](https://docs.rapid7.com/metasploit/running-metasploit-remotely/) or simply use:
```shell
msfrpcd -U <CRYTON_WORKER_MSFRPCD_USERNAME> -P <CRYTON_WORKER_MSFRPCD_PASSWORD>
```

## Installation (using pip/pipx)
Cryton Worker is available in the [PyPI](https://pypi.org/project/cryton-worker/) and can be installed using *pip* (`pip install --user cryton-worker`). 
However, we **highly recommend** installing the app in an isolated environment using [pipx](https://pypa.github.io/pipx/).

### Requirements
Install the following requirements:
- [Python](https://www.python.org/about/gettingstarted/) >=3.8
- [pipx](https://pypa.github.io/pipx/)

### Installing with pipx
Once you have *pipx* ready on your system, you can start the installation:
```shell
pipx install cryton-worker
```

Make sure you've correctly set the [settings](#settings).

Optionally, you can set up [shell completion](#shell-completion).

Everything should be set. Check out the [usage section](#usage).

## Installation (using Docker Compose)
Cryton Worker can be installed using Docker Compose.

To allow the Worker to start listeners, the container has raw access to the host’s network interface.

**This guide won't describe how to install or mount the tools/applications used by the (attack) modules.** 
More information can be found in the [Docker documentation](https://docs.docker.com/storage/volumes/).

### Requirements
- [Docker Compose](https://docs.docker.com/compose/install/)

Add yourself to the group *docker*, so you can work with Docker CLI without *sudo*:
```shell
sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker
docker run hello-world
```

### Installing and running with Docker Compose
First, we have to clone the repo and switch to the correct version.
```shell
git clone https://gitlab.ics.muni.cz/cryton/cryton-worker.git
cd cryton-worker
git checkout <version>
```

Make sure you've correctly set the [settings](#settings). You can't change the settings on a running container.

Finally, copy your settings:
```shell
cp ~/.local/cryton-worker/.env .env
```

We are now ready to build and start the Worker:
```shell
docker compose up -d --build
```

After a while you should see a similar output:
```
[+] Running 1/1
 ⠿ Container cryton_worker  Started
```

Everything should be set. Check if the installation was successful and the Worker is running:
```shell
docker compose logs
```
You should see `[*] Waiting for messages.` in the output.

Docker can sometimes create dangling (`<none>:<none>`) images which can result in high disk space usage. You can remove them using: 
```shell
docker image prune
```

## Development
To install Cryton Worker for development, you must install [Poetry](https://python-poetry.org/docs/).

Clone the repository:
```shell
git clone https://gitlab.ics.muni.cz/cryton/cryton-worker.git
```

Then go to the correct directory and install the project:
```shell
cd cryton-worker
poetry install
```

To spawn a shell use:
```shell
poetry shell
```

Make sure you've correctly set the [settings](#settings).  
To override the settings quickly, you can use this handy one-liner:
```shell
export $(grep -v '^#' .env | xargs)
```

Optionally, you can set up [shell completion](#shell-completion)

Everything should be set, check out the [usage section](#usage).

## Usage
**NOTICE: If you're using Docker Compose to install the app, you can skip this section.**

Use the following to invoke the app:
```shell
cryton-worker
```

You should see a help page:
```
Usage: cryton-worker [OPTIONS] COMMAND [ARGS]...

  Cryton Worker CLI.

Options:
  ...
```

**To learn about each command's options use**:
```shell
cryton-worker <your command> --help
```

To start Worker use `cryton-worker start` and you should see something like:
```
Starting Worker <Worker name>..
To exit press CTRL+C
Connection does not exist. Retrying..
Connection to RabbitMQ server established.
[*] Waiting for messages.
```

## Executing modules
To be able to execute a module (Python script), it must have the following structure and IO arguments.

### Modules' structure
- Each module must have its own directory with its name.
- Script (module) must be called `mod.py`.
- Module must contain an `execute` function that takes a dictionary and returns a dictionary. It's an entry point for executing it.
- Module should contain a `validate` function that takes a dictionary, validates it, and returns 0 if it's okay, else raises an exception.

Path example:  
`/CRYTON_WORKER_MODULES_DIR/my-module-name/mod.py`

Where:  
- **CRYTON_WORKER_MODULES_DIR** has to be the same path as is defined in the *CRYTON_WORKER_MODULES_DIR* variable.
- **my-module-name** is the directory containing your module.
- **mod.py** is the module file.

Module (`mod.py`) example:  
```python
def validate(arguments: dict) -> int:
    if arguments != {}:
        return 0  # If arguments are valid.
    raise Exception("No arguments")  # If arguments aren't valid.

def execute(arguments: dict) -> dict:
    # Do stuff.
    return {"return_code": 0, "serialized_output": ["x", "y"]}

```

### Input parameters
Every module has its own input parameters. These input parameters are given as a dictionary to the 
module `execute` (when executing the module) or `validate` (when validating the module parameters) function. 

### Output parameters
Every attack module (its `execute` function) returns a dictionary with the following keys:

| Parameter name      | Parameter meaning                                                                                                                                                                                                                                 |
|---------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `return_code`       | Numeric representation of result (0, -1, -2). <br />0 (OK) means the module finished successfully.<br />-1 (FAIL) means the module finished unsuccessfully.<br />-2 (ERROR) means the module finished with an unhandled error.                    |
| `serialized_output` | Parsed output of the module. Eg. for a bruteforce module, this might be a list of found usernames and passwords.                                                                                                                                  |                                                                                                                                                                           |
| `output`            | Raw output of the module                                                                                                                                                                                                                          |

## Prebuilt functionality for modules
Worker provides prebuilt functionality to make building modules easier. Import it using:
```python
from cryton_worker.lib.util import module_util
```

It gives you access to:
### Metasploit
Wrapper for *MsfRpcClient* from *[pymetasploit3](https://github.com/DanMcInerney/pymetasploit3)*.
Examples:
```python
# Check if the connection to msfrpcd is OK before doing anything.
from cryton_worker.lib.util.module_util import Metasploit
msf = Metasploit()
if msf.is_connected():
    msf.do_stuff()
```
```python
from cryton_worker.lib.util.module_util import Metasploit
search_criteria = {"via_exploit": "my/exploit"}
found_sessions = Metasploit().get_sessions(**search_criteria)
```
```python
from cryton_worker.lib.util.module_util import Metasploit
output = Metasploit().execute_in_session("my_command", "session_id")
```

```python
from cryton_worker.lib.util.module_util import Metasploit

options = {"exploit_arguments": {}, "payload_arguments": {}}
Metasploit().execute_exploit("my_exploit", "my_payload", **options)
```
```python
from cryton_worker.lib.util.module_util import Metasploit
token = Metasploit().client.add_perm_token()
```
```python
from cryton_worker.lib.util.module_util import Metasploit
output = Metasploit().get_parameter_from_session("session_id", "my_param")
```

### get_file_binary
Function to get a file as binary.  
Example:
```python
from cryton_worker.lib.util.module_util import get_file_binary
my_file_content = get_file_binary("/path/to/my/file")
```

### File
Class used with *[schema](https://pypi.org/project/schema/)* for validation if file exists.  
Example:
```python
from schema import Schema
from cryton_worker.lib.util.module_util import File
schema = Schema(File(str))
schema.validate("/path/to/file")
```

### Dir
Class used with *[schema](https://pypi.org/project/schema/)* for validation if directory exists.  
Example:
```python
from schema import Schema
from cryton_worker.lib.util.module_util import Dir
schema = Schema(Dir(str))
schema.validate("/path/to/directory")
```

## Rabbit API
Worker is able to process any request sent through RabbitMQ to its Queues (`cryton_worker.WORKER_NAME.attack.request`, 
`cryton_worker.WORKER_NAME.control.request`, `cryton_worker.WORKER_NAME.agent.request`)
defined using *WORKER_NAME* (can be changed using CLI or in the settings).

The response is sent to the queue defined using the `reply_to` parameter in a *message.properties*.

### Attack requests
Requests to execute a command or a module are being processed in the `cryton_worker.WORKER_NAME.attack.request` queue.  
List of supported requests:

#### Execute attack module
To execute an attack module, send a message to `cryton_worker.WORKER_NAME.attack.request` queue in a format 
```json lines
{"ack_queue": "confirmation_queue", "step_type": "worker/execute", "module": module_name, "module_arguments": module_arguments}
```

ACK response format:
```json
{"return_code": 0, "correlation_id": "id"}
```

Response format:
```json
{"return_code": 0, "output": "", "serialized_output": ""}
```

#### Execute command on agent
To execute a command on a deployed agent, send a message to the `cryton_worker.WORKER_NAME.attack.request` queue in a format 
```json
{"step_type": "empire/execute", "arguments": {"shell_command": "whoami", "use_agent": "MyAgent"}}
```

ACK response format:
```json
{"return_code": 0, "correlation_id": "id"}
```

Response format:
```json
{"return_code": 0, "output": "", "serialized_output": ""}
```

#### Execute empire module on agent
To execute an empire module on a deployed agent, send a message to the `cryton_worker.WORKER_NAME.attack.request` queue in a format 
```json
{"step_type": "empire/execute", "arguments": { "empire_module": "python/collection/linux/pillage_user", "use_agent": "MyAgent"}}
```

ACK response format:
```json
{"return_code": 0, "correlation_id": "id"}
```

Response format: 
```json
{"return_code": 0, "output": "", "serialized_output": ""}
```

### Agent requests
Requests to control empire agents are being processed in `cryton_worker.WORKER_NAME.agent.request` queue.  
List of supported requests:

#### Deploy agent
Deploy an agent and send a response containing the result.  
Example: 
```json
{"step_type": "empire/agent-deploy", "arguments": {"stager_type": "multi/bash", "agent_name": "MyAgent", "listener_name": "TestListener", "listener_port": 80, "session_id": "MSF_SESSION_ID"}}
```

Response example: 
```json
{"return_code": 0, "output": "Agent 'MyAgent' deployed on target 192.168.33.12."}
```
### Control requests
To perform a control event send a message to `cryton_worker.WORKER_NAME.control.request` queue in a format 
```json lines
{"event_t": type, "event_v": value}
```

Response format:
```json lines
{"event_t": type, "event_v": value}
```

**List of supported requests:**

#### Validate module
Validate a module and send a response containing the result.  
Example: 
```json lines
{"event_t": "VALIDATE_MODULE", "event_v": {"module": module_name, "module_arguments": module_arguments}}
```

Response example: 
```json
{"event_t": "VALIDATE_MODULE", "event_v": {"return_code": 0, "output": "output"}}
```

#### List modules
List available modules and send a response containing the result.  

Request example: 
```json
{"event_t": "LIST_MODULES", "event_v": {}}
```

Response example: 
```json
{"event_t": "LIST_MODULES", "event_v": {"module_list": ["module_name"]}}
```

#### List sessions
List available Metasploit sessions and send a response containing the result.

Request example:
```json lines
{"event_t": "LIST_SESSIONS", "event_v": {"target_host": target_ip}}
```

Response example: 
```json
{"event_t": "LIST_SESSIONS", "event_v": {"session_list": ["session_id"]}}
```

#### Kill Step execution
Kill running Step (module) and send a response containing the result.  
Example:
```json lines
{"event_t": "KILL_STEP_EXECUTION", "event_v": {"correlation_id": correlation_id}}
```

Response example:
```json
{"event_t": "KILL_STEP_EXECUTION", "event_v": {"return_code": -2, "output": "exception"}}
```

#### Health check
Check if Worker is alive and send a response containing the result.  
Example: 
```json
{"event_t": "HEALTH_CHECK", "event_v": {}}
```

Response example: 
```json
{"event_t": "HEALTH_CHECK", "event_v": {"return_code": 0}}
```

#### Add trigger for HTTPListener
Add trigger with parameters and start listener with `host` and `port` if it doesn't already exists, send a response containing the result afterwards.  

Request example: 
```json lines
{"event_t": "ADD_TRIGGER", "event_v": {"host": host, "port": port, "listener_type": "HTTP", "reply_to": reply_to_queue, 
  "routes": [{"path": path, "method": method, "parameters": [{"name": name, "value": value}]}]}}
```

Response example:
```json
{"event_t": "ADD_TRIGGER", "event_v": {"return_code": 0, "trigger_id": "123"}}
```
#### Remove trigger for HTTPListener
Remove trigger, optionally stop the  HTTPListener if there are no triggers left and send a response containing the result.  

Request example: 
```json
{"event_t": "REMOVE_TRIGGER", "event_v": {"trigger_id": "123"}}
```

#### Add trigger for MSFListener
Add trigger with session identifiers and start MSFListener.

Request example:
```json
{"event_t": "ADD_TRIGGER", "event_v": {"listener_type": "MSF", "reply_to": "cryton_core.control.response", "identifiers": {"via_exploit": "auxiliary/scanner/ssh/ssh_login"}}}
```

Response example: 
```json
{"event_t": "ADD_TRIGGER", "event_v": {"return_code": 0, "trigger_id": "123"}}
```

#### Remove trigger for MSFListener
This will stop the MSFListener because it can't have multiple triggers.

Request example:
```json
{"event_t": "REMOVE_TRIGGER", "event_v": {"trigger_id": "123"}}
```

Response example:
```json
{"event_t": "REMOVE_TRIGGER", "event_v": {"return_code": -2, "output": "exception"}}
```

#### List triggers
List available triggers and send a response containing the result.  

Example:
```json
{"event_t": "LIST_TRIGGERS", "event_v": {}}
```

Response example:
```json lines
{"event_t": "LIST_TRIGGERS", "event_v": {"trigger_list": [{"id": "123", "trigger_param": "trigger_param_value", ...}]}}
```

#### Trigger Stage (Response only)
Sent when a trigger is activated.

Response example:
```json lines
{"event_t": "TRIGGER_STAGE", "event_v": {"stage_execution_id": stage_execution_id}}
```

## Shell completion
Shell completion is available for the *Bash*, *Zsh*, and *Fish* shell and has to be manually enabled (**the tool must be installed first**).

### Bash
First, **create an app directory** (if you haven't already):
```shell
mkdir ~/.local/cryton-worker/
```

Generate and save the completion script:
```shell
_CRYTON_WORKER_COMPLETE=bash_source cryton-worker > ~/.local/cryton-worker/cryton-worker-complete.bash
```

Source the file in the `~/.bashrc` file:
```shell
echo ". ~/.local/cryton-worker/cryton-worker-complete.bash" >> ~/.bashrc
```

You may need to restart your shell for the changes to take effect.

### Zsh
First, **create an app directory** (if you haven't already):
```shell
mkdir ~/.local/cryton-worker/
```

Generate and save the completion script:
```shell
_CRYTON_WORKER_COMPLETE=zsh_source cryton-worker > ~/.local/cryton-worker/cryton-worker-complete.zsh
```

Source the file in the `~/.zshrc` file:
```shell
echo ". ~/.local/cryton-worker/cryton-worker-complete.zsh" >> ~/.zshrc
```

You may need to restart your shell for the changes to take effect.

### Fish
Generate and save the completion script:
```shell
_CRYTON_WORKER_COMPLETE=fish_source cryton-worker > ~/.config/fish/completions/cryton-worker-complete.fish
```

You may need to restart your shell for the changes to take effect.
