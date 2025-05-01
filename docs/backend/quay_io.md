# Quay.io and Github Actions

Instructions on how to to configure Github Actions to push a new image to Quay.io repository.

#### Quay.io

- Create a new Quay.io account (optional).
- Create a new empty repository under it.
	- This will be the same name as the to be created image (i.e. elisaohtuprojekti-backend).
- Create a new robot user
	- Preferrable use same name as the github repository (i.e. elisaohtuprojekti).
- Give that robot WRITE permissions to the quay.io project repository (i.e. elisaohtuprojekti-backend).

#### Github Actions

- On a repository level move to 'Settings' >> 'Environments'.
- Create a new environment (i.e. 'testing', 'staging', 'production').
- Add new environment secrets with their secret values (i.e. REGISTRY_USERNAME and REGISTRY_PASSWORD)
	- Take "username + robot account" and token value from Quay.io Robot Accounts -page.


```
username: ohtuprojekti+github
password: ${{ secrets.REGISTRY_PASSWORD }}
```
