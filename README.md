# OLX Raider

Simple web scrapper fetching flat rent offers basing on provided conditions.


## !!! FOR NOW BUILD AND PUSH IMAGES IS ENOUGH !!!

## Prepare a image

### Build image:
```bash
docker build -t olx_raider .
```

### Tag a image:
```bash
docker tag olx_raider:latest 084653813012.dkr.ecr.eu-west-1.amazonaws.com/olx_raider:latest
```

### Push a image:
```bash
docker push 084653813012.dkr.ecr.eu-west-1.amazonaws.com/olx_raider:latest
```

## Get chromedriver

### Chromedriver:
```bash
curl -SL https://chromedriver.storage.googleapis.com/2.37/chromedriver_linux64.zip > chromedriver.zip
```
### Binary headless chromium:
Download from, used version v1.0.0-57:
https://github.com/adieuadieu/serverless-chrome/releases


## Prepare a package (optional)

This method allow to prepare zip file with lambda function and dependencies in one package

### Create a packages dir:
```bash
mkdir packages
```

### Install dependencies:
```bash
pip install --target ./packages -r requirements.txt
```


### Pack packages directory:
```bash
cd packages
zip -r ../deployment_package.zip .
```

### Pack packages directory and lambda file:
```bash
cd ..
zip deployment_package.zip lambda_function.py
```

## Prepare layer (optional)

TO DO...