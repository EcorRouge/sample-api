# User Session

API to handle user session

## Signup

```curl
curl -X POST \
  $URL/signup \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/json' \
  -d '{
	"email": "qfp19637@bcaoo.com",
	"password": "SuperSecret123!"
}'
```

## Login

```curl
curl -X POST \
  $URL/login \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/json' \
  -d '{
  "username": "qfp19637@bcaoo.com",
  "password": "SuperSecret123!"
}'
```

## Reset password

```curl
curl -X POST \
  $URL/password-reset \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/json' \
  -d '{
	"email": "b3797012@urhen.com"
}'
```