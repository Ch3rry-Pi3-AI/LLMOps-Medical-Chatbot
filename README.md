# 🧰 **Jenkins Deployment Setup — LLMOps Medical Chatbot**

This branch introduces the **custom Jenkins environment** required to build, test, and deploy the Medical Chatbot through a fully containerised CI/CD pipeline.
A Docker-enabled Jenkins controller image is created, allowing pipelines to build Docker images directly inside Jenkins using Docker-in-Docker (DinD) behaviour.

This step prepares the project for automated deployment workflows.

## 🗂️ **Project Structure (Updated)**

```text
LLMOPS-MEDICAL-CHATBOT/
├── custom_jenkins/
│   └── Dockerfile        # NEW: Docker-enabled Jenkins controller image
│
├── app/
│   └── ...               # Flask UI + RAG pipeline
│
├── data/
│   └── ...
│
├── Dockerfile            # App container
└── ...
```

## ⚙️ **What Was Implemented in This Branch**

### 🐳 1. Created the `custom_jenkins` Directory

A new directory was added to the project containing a fully documented Dockerfile that constructs a **Jenkins controller image with Docker Engine installed**.
This allows Jenkins to:

* Build Docker images
* Run containers during pipelines
* Push images to container registries
* Interface with Docker from inside its own container

### 🛠️ 2. Built the Custom Jenkins Image

From inside the `custom_jenkins` folder, the custom Jenkins DinD image is built using:

```bash
docker build -t jenkins-dind .
```

This produces a reproducible Jenkins environment suitable for CI/CD.

### 🚦 3. Launched the Jenkins Container

A runnable Jenkins instance is created with:

```bash
docker run -d \
  --name jenkins-dind \
  --privileged \
  -p 8080:8080 \
  -p 50000:50000 \
  -v //var/run/docker.sock:/var/run/docker.sock \
  -v jenkins_home:/var/jenkins_home \
  jenkins-dind
```

This container:

* Runs in privileged mode
* Mounts the host Docker socket
* Uses a persistent Jenkins home volume
* Exposes the standard Jenkins ports

### 📄 4. Retrieved Initial Jenkins Password

After running the container, logs and admin credentials are retrieved with:

```bash
docker logs jenkins-dind
```

or:

```bash
docker exec jenkins-dind cat /var/jenkins_home/secrets/initialAdminPassword
```

This password is required for the first login.

### 🖥️ 5. Accessed Jenkins Dashboard

The Jenkins UI is now available at:

```
http://localhost:8080
```

The welcome wizard loads and prompts for plugin installation.

### 🐍 6. Installed Python Inside the Jenkins Container

Since pipelines will run Python code, Python 3 and pip were installed directly into the Jenkins container:

```bash
docker exec -u root -it jenkins-dind bash
apt update -y
apt install -y python3 python3-pip
ln -s /usr/bin/python3 /usr/bin/python
exit
```

This ensures that Python-based stages (tests, linting, packaging, ML steps) can run inside Jenkins.

### 🔄 7. Restarted Jenkins to Apply Changes

```bash
docker restart jenkins-dind
```

After restarting, Jenkins is ready with full Python + Docker support.

### 🔐 8. Signed in Again and Completed Setup

Final login at:

```
http://localhost:8080
```

You can now create pipelines, connect GitHub, and begin setting up automated deployment.

## ✅ **Summary**

This branch delivers the full Jenkins CI/CD foundation:

* Custom Jenkins controller image with Docker installed
* Containerised Jenkins instance with persistent storage
* Python environment added inside Jenkins
* Ready for Docker-based build and deployment pipelines

The project is now set up for the next stage: **configuring Jenkins pipelines**, integrating GitHub, and later deploying to Kubernetes or cloud environments.
