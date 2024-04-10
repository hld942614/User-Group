# Flask Application

## How to start (locally)

### create virtual environment

`python3 -m venv .venv` ## Mac   
`python -m venv .venv` ## Windows

### activate virtual environment

`source .venv/bin/activate` ## Mac  
`.venv\Scripts\activate` ## Windows

### install dependencies

`pip install -r requirements.txt`

### start the flask application

`flask --app app run`

### User
#### Add a new user. (Before creating a user, make sure there is a corresponding group_id in the group table.But it's acceptable if group_id == null)
`curl -X POST http://127.0.0.1:5000/user -H 'Content-Type: application/json' -d '{"name": "David Cheng","group_id":1}'` ## Mac  
`Invoke-WebRequest -Uri 'http://127.0.0.1:5000/user' -Method POST -Headers @{ 'Content-Type' = 'application/json' } -Body '{"name": "David Cheng","group_id":1}'` ## Windows

#### Remove a user by id.
`curl -X DELETE http://127.0.0.1:5000/user/<user_id>` ## Mac  
`Invoke-WebRequest -Uri 'http://127.0.0.1:5000/user/<user_id>' -Method DELETE` ## Windows

#### Retrieve details of a specific user by id. 
`curl -X GET http://127.0.0.1:5000/user/<user_id>` ## Mac  
`Invoke-WebRequest -Uri 'http://127.0.0.1:5000/user/<user_id>' -Method GET` ## Windows

#### List all users with optional filtering by partial name match.
##### With user_name
`curl -X GET http://127.0.0.1:5000/users?name=<user_name>` ## Mac  
`Invoke-WebRequest -Uri 'http://127.0.0.1:5000/users?name=<user_name>' -Method GET` ## Windows
##### Without user_name
`curl -X GET http://127.0.0.1:5000/users` ## Mac  
`Invoke-WebRequest -Uri 'http://127.0.0.1:5000/users' -Method GET` ## Windows

### Group
#### Add a new group.
`curl -X POST http://127.0.0.1:5000/group -H 'Content-Type: application/json' -d '{"name": "Group 1"}'` ## Mac  
`Invoke-WebRequest -Uri 'http://127.0.0.1:5000/group' -Method POST -Headers @{ 'Content-Type' = 'application/json' } -Body '{"name": "Group 1"}'` ## Windows

#### Remove a group by id. Prevent deletion if the group has at least one user and provide an appropriate error message.
`curl -X DELETE http://127.0.0.1:5000/group/<group_id>` ## Mac  
`Invoke-WebRequest -Uri 'http://127.0.0.1:5000/group/<group_id>' -Method DELETE` ## Windows

#### Retrieve details of a specific group by id. 
`curl -X GET http://127.0.0.1:5000/group/<group_id>` ## Mac  
`Invoke-WebRequest -Uri 'http://127.0.0.1:5000/group/<group_id>' -Method GET` ## Windows

#### List all groups.
`curl -X GET http://127.0.0.1:5000/groups` ## Mac  
`Invoke-WebRequest -Uri 'http://127.0.0.1:5000/groups' -Method GET` ## Windows

### Run test
`pytest`

## How to start (docker)
Ensure you have docker install, and start the docker daemon.
### Build docker image

`docker-compose build`

### Start docker

`docker-compose up`

### Stop docker

`docker-compose down`
