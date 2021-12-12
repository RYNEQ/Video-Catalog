# Project Setup
- [Create VirtualEnv](#Create-VirtualEnv)
- [Fork Project](#Fork-Project)
- [Clone Project](#Clone-Project)
- [Setup Docker](#Setup-Docker)
- [Setup Project](#Setup-Project)

## <a name='Create-VirtualEnv'></a>Create VirtualEnv
1. Create a virtualenv either using `virtualenv` or `virtualenvwrapper` or any other env manager
	```bash 
    mkvirtualenv -p python3 video-catalog-project
	```
2. Activate your env
	```bash
    workon video-catalog-project
	```
##  <a name='Fork-Project'></a>Fork Project
1. Enter your github account 
2. Enter Project page
3. Click on `Fork` button to make a fork of repository in your account

##  <a name='Clone-Project'></a>Clone Project
First Setup your public key in your profile if you didn't before
Then:
```bash
git clone git@github.com:AnisaAdvancedDjangoClass/video-catalog.git
```
## <a name='Setup-Docker'></a>Setup Docker
```bash
sudo apt install apt-transport-https ca-certificates curl software-properties-common
```
```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
```
```bash
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
```
```bash
sudo apt install docker-ce
```
```bash
sudo usermod -aG docker ${USER}
```
```bash
su - ${USER}
```
```bash
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```
```bash
echo -e '{\n"registry-mirrors": ["https://dockerhub.ir"] \n}' | sudo tee /etc/docker/daemon.json
```
```bash 
sudo systemctl restart docker.service
```

## <a name='Setup-Project'></a>Setup Project
1. Enter project directory with virtualenv enabled
2. Install PostgreSQL bindings
	- if you can install system package first install postgres and python C headers:
		```bash
		sudo apt install libpq-dev python3-dev
		```
		then install `psycopg2`
		```bash
		pip install psycopg2
		```  
	- Otherwise only install `psycopg2-binary`
		```bash
		pip install psycopg2-binary
		```
3. Import `requirements.txt`
	```bash
	pip install -r requirements.txt
	```
4. Start docker containers
	```bash
	docker-compose up -d
	```
5. Apply migrations
	```bash
	python manage.py migrate
	```
