# OPA HTTP API

## Task

Write an authorization policy that controls which HTTP APIs individual users are
permitted to execute. The following APIs return the JSON value true if the API call is authorized and false otherwise.

| Method   | Path            | Meaning                         |
| -------- | --------------- | ------------------------------- |
| `POST`   | `/v1/cars`      | Create a new car                |
| `GET`    | `/v1/cars/<id>` | Read details of the given car   |
| `PUT`    | `/v1/cars/<id>` | Update details of the given car |
| `DELETE` | `/v1/cars/<id>` | Delete the given car            |

The input for this policy (the input provided to OPA) is the JSON shown below.

| Schema                                                                                                                  | Example                                                                                                                         |
| ----------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| `{`<br>&nbsp;&nbsp;`"method": string,`<br>&nbsp;&nbsp;`"path": array of strings`<br>&nbsp;&nbsp;`"user": string`<br>`}` | `{`<br>&nbsp;&nbsp;`"method": "GET",`<br>&nbsp;&nbsp;`"path": ["v1", "cars", "id1234"]`<br>&nbsp;&nbsp;`"user": "alice,`<br>`}` |

Access policy:

- Anyone can run a GET
- Employees can update a car via PUT
- Employees can create new cars via POST
- Only the employee who created a car can DELETE it

Additional information:

- Employees:
  - alice
  - eve
  - ricardo
  - carmen
- Car creator:
  - id1234: alice
  - id2345: alice
  - id3456: ricardo

## Process

I started by Googling `"OPA HTTP API"` and found the following result: https://www.openpolicyagent.org/docs/v0.11.0/http-api-authorization/.

The document was well written and easy to follow, but I didn't see a link to the source code anywhere. I decided to pull down the `openpolicyagent/demo-restful-api:0.2` image and look inside the container. I used the code in there as a starting point/template.

I decided to create a VSCode project using some `docker-compose` scaffolding that I typically use. I've included everything in this repo. This allowed me to spin up a development/test environment and enable live reloading of the Python Flask application. I wasn't able to figure out if it was possible to enable live reloading of the `opa` server so I ended up restarting using `docker-compose` to make changes live in the `opa` container.

It took some tweaking and tuning of the Flask application to get it working correctly with the Python 3.8.4 Alpine image. Once the Flask application was working, it was straightforward to create the Repo policy and test everything out. I used the following Rego documents as reference https://www.openpolicyagent.org/docs/latest/policy-language/ and https://www.openpolicyagent.org/docs/latest/policy-reference/. I then created requests in Postman to test the various scenarios and started experimenting, debugging, and fixing any issues. Seeing that VSCode has a REST Client extension, I would probably convert the Postman requests to use that so I could keep everything in a single project.

Overall it probably took me around an hour or two to get everything to a point where I was satisfied with the results.

I would probably extend this even further to create a more "production" grade `Dockerfile` and `docker-compose.yml` file as well as Kubernetes YAML.

## Policy

[Rego Policy](opa/policy/api_authz.rego)

## Feedback

- Put the link to any source code for examples at the start of the tutorial/exercise. It wasn't until I completed the exercise that I noticed the link at the bottom of the page.
- Provide a direct link to the source code https://github.com/open-policy-agent/contrib/tree/master/api_authz instead of https://github.com/open-policy-agent/contrib
- Easier to find or better documentation on the possible `opa run` flags, a simple man page style section would be helpful.
- A more guided experience or walkthrough of the Rego language with real-world examples and exercises.

## Using this repo

This repo only requires that you have `docker` and `docker-compose` installed. You can use your IDE of choice; I prefer VSCode.

Once you clone the repository, you can use the `development-compose-up.sh` and `development-compose-down.sh` scripts located in the `bin` directory to spin up a development environment.

Saving changes to the `server.py` file will trigger a live reload of the Flask application, but changes to the `api_authz.rego` file will require restarting the application.
