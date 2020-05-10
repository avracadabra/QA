# Quality assurance

This repo is about dev environment, integration testing, tools to release to make
consistency versions over each repo, deploy process and so on.

!!! warning
    we are using [git submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules)
    to other repo.



## Setup with docker

* **requirement**: docker ready to execute

### Build docker dev images

``make docker-build``

### Run dev env

``make docker-run-dev``

### Run tests


``make docker-tests``

### Create released docker images

We are using [multistage build](https://docs.docker.com/develop/develop-images/multistage-build/#use-multi-stage-builds)
in order to create tight Docker images.

``ake