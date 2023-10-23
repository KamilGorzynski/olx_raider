# OLX Raider

Simple web scrapper fetching flat rent offers basing on provided conditions.



## Prepare a package


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