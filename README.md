<h1 align="center"><a href="https://www.youtube.com/watch?v=SCgy9dYVPI4">Langfuse-Kong-Plugin</a></a></h1>

<strong> Langfuse </strong> is an Open Source LLM Engineering Platform to log
Traces, evals, prompt management, and metrics to debug and improve your LLM application.

<h4>Read Langfuse <a href="https://langfuse.com/docs">documentation.</a></h4>


## Key Features of Langfuse:
- <strong> Logging and Tracing: </strong> Langfuse captures detailed logs of interactions with LLMs, allowing developers to trace the exact steps taken during a conversation or process. This helps identify where things might have gone wrong or improvements can be made.

- <strong> Visualization:</strong> The tool provides visual representations of data flows, decision trees, and other critical aspects of the LLM's operations. This can be particularly useful in complex applications where understanding the flow of information is crucial.

- <strong> Debugging:</strong> By offering granular insights into the operations of LLMs, Langfuse aids in debugging issues that might not be immediately apparent. This includes tracking down errors, understanding unexpected behavior, and optimizing responses.

- <strong> Performance Monitoring:</strong> Langfuse helps in monitoring the performance of LLM applications over time, identifying trends, and detecting anomalies. This is essential for maintaining the efficiency and reliability of applications that rely on LLMs.

- <strong> Integrations:</strong> Langfuse often supports integrations with other tools and platforms commonly used in the development and deployment of LLMs, making it easier to incorporate into existing workflows.

<p align="center">
  <img src="data/Langfuse.png" />
</p> 

# 1. Sequence Diagram 

<h4 align="center">Langfuse Kong Plugin Flow to add Logs of the GenAI LLM usage directly from Gateway to monitor usage and cost.</h4>

``` mermaid
sequenceDiagram

    Title: Langfuse Kong Plugin Flow to add Logs of the GenAI LLM usage directly from Gateway to monitor usage and cost.  
    
    participant Client API
    participant Kong API Gateway
    participant Langfuse-Kong-Plugin
    participant LLM Endpoint
    participant Langfuse Dashboard
    
    Client API->>Kong API Gateway: API call redirected to Kong API Gateway 
    
    Kong API Gateway->>Langfuse-Kong-Plugin: API gateway intercepts the call and trigger the plugin  
    
    
    Langfuse-Kong-Plugin->>LLM Endpoint: Plugin redirects the call to the configured LLM Provider and fetches the generated response
    
    Note right of Langfuse-Kong-Plugin: Can be configured to use any LLM Provider

    
    LLM Endpoint-->>Langfuse-Kong-Plugin: LLM provider sends the generated response
    
    Langfuse-Kong-Plugin->>Langfuse Dashboard: Plugin add the log traces to the Langfuse Dashboard
    
    Langfuse-Kong-Plugin-->>Kong API Gateway: Plugin sends the generated response
    
    Kong API Gateway-->>Client API: API Gateway sends the generated response
```


### Tested in Kong Release

- <strong> Kong Community 3.7.1 </strong>

<h3> Setup Up Kong Locally Follow the <a href="https://github.com/raj713335/kong-gateway">GitHub Repository </a> </h3>


# 2. Getting Started With the Langfuse Application (Self-host docker)

- Clone this repository and open it up in your IDE or terminal
- Run `cp .env.example .env` and replace values appropriately in the .env file
- Run `docker compose up -d` to get the langfuse instance running.

```sh
$ cd Langfuse-Kong-Plugin
$ docker-compose up -d --build
```

- Navigate to `http://localhost:3000`
- Click `Sign up` to create your account


### Dashboard
- Create a new project
- Go to settings and click `Create new API keys`
- Copy the Secret Key and Public Key 
- Store keys in the `.env` file within your LLM project:


```
LANGFUSE_SECRET_KEY="sk-your-key"
LANGFUSE_PUBLIC_KEY="pk-your-key"
LANGFUSE_HOST="http://localhost:3000"
```


# 3.  Langfuse-Kong-Plugin Plugin Installation

### Install Kong Pdk and Python Packages 
```
$ apt-get update && apt-get add python3 py3-pip python3-dev musl-dev libffi-dev gcc g++ file make && PYTHONWARNINGS=ignore pip3 install kong-pdk
$ pip install -r requirements.txt
```

### Make the Below Changes in Kong.conf

```
$ pluginserver_names=python
$ pluginserver_python_socket=/usr/local/kong/python_pluginserver.sock
$ pluginserver_python_start_cmd = /opt/kong-python-pdk/kong-pluginserver --no-lua-style --plugins-directory <PATH_OF_PLUGIN_FOLDER> -v
$ pluginserver_python_query_cmd = /opt/kong-python-pdk/kong-pluginserver --no-lua-style --plugins-directory <PATH_OF_PLUGIN_FOLDER> --dump-all-plugins
```
After Installing the Plugin using any of the above steps . Add the Plugin Name in Kong.conf

```
plugins = bundled,Langfuse-Kong-Plugin
```
### Restart Kong

```
kong restart
```
# 4. Configuration Reference

## Enable the plugin on a Route

### Admin-API
For example, configure this plugin on a service by making the following request:
		
	curl -X POST http://{HOST}:8001/routes/{ROUTE}/plugins \
	--data "name=Langfuse-Kong-Plugin"  \
	--data "config.OPENAI_API_KEY={OPENAI_API_KEY}"
	--data "config.OPENAI_API_MODEL={OPENAI_API_MODEL}"
    --data "config.LANGFUSE_SECRET_KEY={LANGFUSE_SECRET_KEY}"
    --data "config.LANGFUSE_PUBLIC_KEY={LANGFUSE_PUBLIC_KEY}"
    --data "config.LANGFUSE_HOST={LANGFUSE_HOST}"

### Declarative(YAML)
For example, configure this plugin on a service by adding this section to your declarative configuration file:
			
	routes : 
        name: {ROUTE}
	    plugins:
	    - name: Langfuse-Kong-Plugin
	    config:
	        OPENAI_API_KEY: {OPENAI_API_KEY}
	        OPENAI_API_MODEL : {OPENAI_API_MODEL}
            LANGFUSE_SECRET_KEY : {LANGFUSE_SECRET_KEY}
            LANGFUSE_PUBLIC_KEY : {LANGFUSE_PUBLIC_KEY}
            LANGFUSE_HOST : {LANGFUSE_HOST}
	    enabled: true
	    protocols:
	    - grpc
	    - grpcs
	    - http
	    - https

ROUTE is the id or name of the route that this plugin configuration will target.
OPENAI_API_KEY is the openAI Key .
MODEL_NAME is the AI Model name
LANGFUSE_SECRET_KEY is the Langfuse Secret Key.
LANGFUSE_PUBLIC_KEY is the Langfuse Public Key.
LANGFUSE_HOST is the Langfuse Host Url.


### Parameters

| FORM PARAMETER               | Type         | DESCRIPTION                                |
|------------------------------|--------------|--------------------------------------------|
| ROUTE                        |              | The name of the Route  the plugin targets. |
| config.OPENAI_API_KEY        | Type:string  | OpenAI Secret Key                          |
| config.OPENAI_API_MODEL      | Type:string  | OpenAI Model Name                          |
| config.LANGFUSE_SECRET_KEY   | Type:string  | LANGFUSE SECRET KEY                        |
| config.LANGFUSE_PUBLIC_KEY   | Type:string  | LANGFUSE PUBLIC KEY                        |
| config.LANGFUSE_HOST         | Type:string  | LANGFUSE HOST URL                          |





## 5. Project Requirements

<h4>Languages and Tools version used</h4>
<ul>
    <li>Python 3.11.4</li>
    <li>Langfuse 2.73.0</li>
    <li>Kong 3.7.1</li>
</ul>



## 6. Application Screenshots / <a href="https://www.youtube.com/watch?v=SCgy9dYVPI4">Demo.</a>

<p align="center">
  <a href="https://www.youtube.com/watch?v=SCgy9dYVPI4"><img src="data/Kong_Response.png" /></a>
</p> 





## Contributors
Design & Developed By: raj713335@gmail.com
