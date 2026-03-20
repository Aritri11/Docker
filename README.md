# 🐳 Docker — Complete Notes

> A comprehensive guide to Docker: concepts, networking, volumes, and hands-on development.

---

## Table of Contents

1. [What is Docker?](#what-is-docker)
2. [Why Docker is Needed](#why-docker-is-needed)
3. [Core Docker Concepts](#core-docker-concepts)
   - [Docker Engine](#1-docker-engine)
   - [Docker Image](#2-docker-image)
   - [Dockerfile](#3-dockerfile)
   - [Container](#4-container)
   - [Registry](#5-registry)
4. [Docker vs Virtual Machines](#docker-vs-virtual-machines)
5. [Detach Mode (-d)](#detach-mode--d-flag)
6. [Port Binding in Docker](#port-binding-in-docker)
7. [Docker Networking](#docker-networking)
   - [Default Network](#default-docker-network)
   - [Bridge Network](#1-bridge-network-default)
   - [Host Network](#2-host-network)
   - [None Network](#3-none-network)
   - [Custom Networks](#4-custom-docker-networks)
   - [Container Communication](#5-container-communication-in-custom-networks)
   - [Inspecting Networks](#6-inspecting-networks)
   - [Connecting Containers](#7-connecting-containers-to-networks)
8. [Developing with Docker](#developing-with-docker)
   - [Frontend + Backend + Containerized DB](#1-connecting-frontend--backend-with-a-containerized-database)
   - [Docker Compose](#docker-compose)
   - [Dockerizing Your Own App](#2-dockerizing-your-own-app)
9. [Volumes and Data Persistence](#volumes-and-data-persistence)
   - [Named Volumes](#named-volumes)
   - [Anonymous Volumes](#anonymous-volumes)
   - [Bind Mounts](#bind-mounts)

---

## What is Docker?

Docker is a platform to **build**, **share**, and **run** containerized applications so they run identically across machines and environments.

---

## Why Docker is Needed

| Reason | Description |
|---|---|
| **Consistency** | Containers bundle code + dependencies so behavior is identical in dev, test, and prod |
| **Isolation** | Multiple apps/services on one server are isolated — security issues or resource spikes in one don't affect others |
| **Scalability** | Easy to spin up/down many container instances across machines to handle variable traffic |

### Key Use Cases

- Microservices architecture
- CI/CD pipelines
- Cloud migration
- Scalable web applications
- Testing / QA environments
- ML and AI deployments
- API deployments

---

## Core Docker Concepts

### 1. Docker Engine

The **core runtime** that builds and runs containers. It consists of:

| Component | Role |
|---|---|
| **Docker Daemon** (server) | Manages images, containers, networks, and volumes |
| **Docker CLI** | Command-line tool used by developers |
| **REST API** | Mediates between CLI and daemon; allows programmatic control |

---

### 2. Docker Image

A **lightweight, standalone, executable package** containing:
- Application code
- Runtime environment
- Libraries and dependencies
- Environment variables and configuration

**Lifecycle:**

```
Creation (docker build + Dockerfile)
    → Storage (registry)
        → Distribution (pull)
            → Execution (run as container)
```

**Components of an image:**
- Base image (e.g., Debian, Alpine, Python)
- Application code
- Dependencies
- Metadata

---

### 3. Dockerfile

A text file with instructions to build an image. Each instruction creates a **layer**.

| Instruction | Purpose |
|---|---|
| `FROM` | Define the base image |
| `WORKDIR` | Set the working directory inside the image |
| `COPY` | Copy files from host into the container image |
| `RUN` | Execute a command during build (e.g., install dependencies) |
| `EXPOSE` | Declare the port the container listens on |
| `CMD` / `ENTRYPOINT` | Set the default startup command |
| `ENV` | Set environment variables for the running container |

---

### 4. Container

A **running instance of an image** on a host machine — analogous to a *movie instance from a DVD*.

- Created with `docker run <image>`
- Gets an isolated filesystem and resources
- Shares the host OS kernel

---

### 5. Registry

A storage and distribution system for Docker images.

| Registry | Type |
|---|---|
| **Docker Hub** | Main public registry |
| AWS ECR, GCP, Azure | Cloud-hosted private registries |
| Self-hosted | Organization's own private registry |

**Key concepts:**
- **Repository** — a collection of image versions
- **Tags** — version labels (e.g., `latest`, `v1`, `v2`)

---

### Full Architecture Flow

```
Developer
    → Writes Dockerfile
        → docker build → Image
            → Pushed to Registry
                → Tester / Production pulls image
                    → docker run → Container
```

---

## Docker vs Virtual Machines

| Feature | Docker Containers | Virtual Machines |
|---|---|---|
| **Architecture** | Share host OS kernel; package app + dependencies | Virtualize entire hardware; run full guest OS |
| **Resource Usage** | Lightweight, fewer resources | Heavy; more CPU, memory, storage |
| **Startup Time** | Seconds (no OS boot) | Minutes (full OS boot) |
| **Isolation** | Process-level isolation within same OS | Stronger isolation (each has its own OS) |
| **Typical Use** | App deployment, microservices, cloud-native | Running multiple OSes or strong security isolation |

---

## Detach Mode (-d flag)

The `-d` flag stands for **detached mode** — Docker runs the container in the background instead of attaching it to your terminal.

**With `-d`:**
```bash
docker run -d nginx
```
- Container runs in the background
- Terminal is free immediately
- Docker prints the container ID

**Without `-d`:**
```bash
docker run nginx
```
- Container runs in the foreground
- Logs stream to your terminal
- Terminal is blocked until the container stops

---

## Port Binding in Docker

To access a container's service from your host machine, you need to **bind a host port to a container port**.

```bash
docker run -p <host_port>:<container_port> <image>
```

**Example:**
```bash
docker run -p 8080:80 nginx
```
- `8080` → port on your host machine
- `80` → port inside the container

---

## Docker Networking

Docker networking allows containers to communicate with each other, the host machine, and external networks. By default, Docker isolates containers, but networking features allow controlled communication.

### Why Docker Networking is Needed

Without networking, containers cannot talk to each other or interact across services.

**Example microservice flow:**
```
Frontend container → Backend API container → Database container
```
These services must communicate through Docker networking.

---

### Default Docker Network

When Docker is installed, it automatically creates default networks.

```bash
docker network ls
```

Typical output:
```
NETWORK ID     NAME      DRIVER
xxxxxx         bridge    bridge
xxxxxx         host      host
xxxxxx         none      null
```

---

### 1. Bridge Network (Default)

The default networking mode for containers. Containers on the same bridge network can communicate using IP addresses or container names.

```
Host machine
      │
Docker Bridge Network
 ├── Container A
 ├── Container B
 └── Container C
```

```bash
docker run -d --name container1 nginx
docker run -d --name container2 ubuntu
```

> ⚠️ Communication using container names is limited on the **default** bridge network. Use custom networks for DNS-based discovery.

---

### 2. Host Network

The container **shares the host machine's network stack**.

```bash
docker run --network host nginx
```

If nginx listens on port 80 inside the container, it becomes directly accessible at `Host:80` — no port mapping (`-p`) required.

| | |
|---|---|
| ✅ Advantages | Faster networking; no NAT overhead |
| ❌ Disadvantages | No network isolation from host; possible port conflicts |

---

### 3. None Network

Disables networking entirely.

```bash
docker run --network none nginx
```

The container has:
- No internet access
- No communication with other containers

> Used mainly for high-security workloads.

---

### 4. Custom Docker Networks

User-defined networks created manually. They provide:
- Automatic DNS-based container discovery
- Better isolation
- Easier container-to-container communication

```bash
# Create a custom network
docker network create my_network

# Verify
docker network ls

# Run containers inside the network
docker run -d --name web --network my_network nginx
docker run -d --name db  --network my_network mysql
```

Now containers can communicate using names:
```
web → db
```
instead of IP addresses.

---

### 5. Container Communication in Custom Networks

In a custom network, **container name = DNS hostname**.

```
web container → db container
Connection string: mysql://db:3306
```

Docker automatically resolves `db` to the container's IP — making microservice communication straightforward.

---

### 6. Inspecting Networks

```bash
docker network inspect my_network
```

Shows:
- Connected containers
- IP addresses
- Subnet configuration
- Network driver

---

### 7. Connecting Containers to Networks

```bash
# Attach a running container to a network
docker network connect my_network container_name

# Detach a container from a network
docker network disconnect my_network container_name
```

---

## Developing with Docker

### 1. Connecting Frontend + Backend with a Containerized Database

**Stack:**
- Frontend: HTML + CSS
- Backend: `server.js` (Node.js)
- Database: MongoDB (pulled as a Docker image — not installed locally)

**Approach:**
1. Create a custom Docker network
2. Pull MongoDB and Mongo Express images into that network so they can communicate
3. `server.js` on the local system communicates with the containerized MongoDB — without installing MongoDB locally

**Run MongoDB:**
```bash
docker run -d \
  -p 27017:27017 \
  --name mongo \
  --network mongo-network \
  -e MONGO_INITDB_ROOT_USERNAME=admin \
  -e MONGO_INITDB_ROOT_PASSWORD=secret \
  mongo
```

**Run Mongo Express (web UI for MongoDB):**
```bash
docker run -d \
  -p 8081:8081 \
  --name mongo-express \
  --network mongo-network \
  -e ME_CONFIG_MONGODB_ADMINUSERNAME=admin \
  -e ME_CONFIG_MONGODB_ADMINPASSWORD=qwerty \
  -e ME_CONFIG_MONGODB_URL="mongodb://admin:qwerty@mongo:27017" \
  -e ME_CONFIG_BASICAUTH_USERNAME=admin \
  -e ME_CONFIG_BASICAUTH_PASSWORD=qwerty \
  mongo-express
```

---

### Docker Compose

Instead of long `docker run` commands for multiple containers, describe them in a **YAML file** and start everything with one command.

This is the **standardized way** to define and manage multiple containers running at the same time.

**Structure of a Compose file:** `version`, `services`, each service with `image`, `ports`, `environment`, and optionally `networks`.

> Docker Compose automatically creates a **default network** for all services in the file — no explicit `docker network create` needed.

**Example: `mongodb.yaml`**
```yaml
version: '3'
services:
  mongo:
    image: mongo
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: secret

  mongo-express:
    image: mongo-express
    ports:
      - "8081:8081"
    environment:
      ME_CONFIG_MONGODB_ADMINUSERNAME: admin
      ME_CONFIG_MONGODB_ADMINPASSWORD: qwerty
      ME_CONFIG_MONGODB_URL: "mongodb://admin:qwerty@mongo:27017"
      ME_CONFIG_BASICAUTH_USERNAME: admin
      ME_CONFIG_BASICAUTH_PASSWORD: qwerty
```

**Commands:**
```bash
# Start all containers defined in the file (detached mode)
docker compose -f mongodb.yaml up -d

# Stop and permanently remove all containers in the file
docker compose -f mongodb.yaml down
```

---

### 2. Dockerizing Your Own App

Converting your own application into a Docker image (containerizing it) so it can be deployed anywhere.

> In CI/CD pipelines, a Jenkins pipeline handles this for the entire organization.

**Example Dockerfile:**
```dockerfile
FROM node:18
WORKDIR /app
COPY . .
RUN npm install
EXPOSE 3000
CMD ["node", "server.js"]
```

**Build the image:**
```bash
docker build -t testapp:1.0 .
```

**Run a container from the image:**
```bash
docker run testapp:1.0
```

**Publish to Docker Hub:**
```bash
docker login
docker push ratri/testapp
```

---

## Volumes and Data Persistence

By default, a container's filesystem is **ephemeral** — all data is lost when the container is stopped or removed.

**Docker volumes** provide persistent storage managed by Docker or the host.

```bash
# Mount a host directory into a container
docker run -it \
  -v /Users/YourName/Desktop/data:/test/data \
  ubuntu
```

**Volume commands:**
```bash
docker volume ls                  # List all volumes
docker volume inspect my-volume   # Inspect a volume
docker volume create my-volume    # Create a named volume
docker volume rm my-volume        # Remove a named volume
```

> Created named volumes are stored at: `C:\ProgramData\docker\volumes` (Windows)

---

### Named Volumes

Fully managed by Docker, easy to reuse across containers, and persist even after the container is deleted.

```bash
docker run -v my-volume:/app/data nginx
```

| | |
|---|---|
| ✅ Best for | Databases (PostgreSQL, MySQL), application data, production environments |

---

### Anonymous Volumes

Volumes without a specific name. Docker automatically assigns a random name.

```bash
docker run -v /app/data nginx
# Docker creates something like: random_id_volume → /app/data
```

| | |
|---|---|
| ⚠️ Problem | Hard to reference or reuse later |
| ✅ Best for | Temporary storage when data reuse doesn't matter |

---

### Bind Mounts

Connects a **specific folder on your host machine** directly to a path inside the container.

```bash
docker run -v /home/user/project:/app nginx
```

- Changes on the host reflect **immediately** inside the container
- Not managed by Docker

| | |
|---|---|
| ✅ Best for | Development, live code editing, debugging |

---

### Volume Types — Quick Comparison

| Feature | Named Volume | Anonymous Volume | Bind Mount |
|---|---|---|---|
| Managed by Docker | ✅ Yes | ✅ Yes | ❌ No |
| Persistent | ✅ Yes | ✅ Yes (until removed) | ✅ Yes |
| Easy to reuse | ✅ Yes | ❌ No | ✅ Yes |
| Host path control | ❌ No | ❌ No | ✅ Yes |
| Best for | Production databases | Temporary data | Development |

---

*Happy containerizing! 🚀*
