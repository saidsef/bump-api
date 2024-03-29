# Bump API

This Bump API is aimed at making stateless version numbering available via API endpoint.

Bump API is build on top of [treeder/bump](https://hub.docker.com/r/treeder/bump/)

## Documentation

Software versioning is the process of assigning either unique version names or unique version numbers to unique states of computer software. Within a given version number category (major, minor and patch), these numbers are generally assigned in increasing order and correspond to new developments in the software. 

Semantic versioning (aka SemVer), currently the best known and most widely adopted version scheme in this category, uses a sequence of three digits (Major.Minor.Patch), an optional prerelease tag and optional build meta tag. In this scheme, risk and functionality are the measures of significance.

For further [information](https://en.wikipedia.org/wiki/Software_versioning)

## Deployment

As a container:

```shell
docker run -d -p 7070:7070 docker.io/saidsef/bump-api:latest
```

As a Python application:

```shell
pip install -r requirements.txt

PORT=7070 bump-api.py
```

## The Request

The quest must be POST method:

```shell
curl -XPOST http://localhost:7070/api/v1/version -H 'Content-Type: application/json' @test/bump-api.json
```

And the response will look like:

```shell
{
  "new_version": "2.3.1",
}
```

## Kubernetes Deployment

```shell
kubectl apply -k ./deployment
```

## Source

Our latest and greatest source of Jenkins can be found on [GitHub](#deployment). Fork us!

## Contributing

We would :heart:  you to contribute by making a [pull request](https://github.com/saidsef/bump-api/pulls).

Please read the official [Contribution Guide](./CONTRIBUTING.md) for more information on how you can contribute.
