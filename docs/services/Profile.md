# Profile

## Profile API

Get Profile

```curl
curl -X GET \
  $URL/user \
  -H 'authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IlFrSXpSVFkxTlRjMk1ESkVRVFJEUkRFeFF6RTBOekl3T1RnMlF6RkZNalExUWpNMlJFWXdNdyJ9.eyJuaWNrbmFtZSI6InFmcDE5NjM3IiwibmFtZSI6InFmcDE5NjM3QGJjYW9vLmNvbSIsInBpY3R1cmUiOiJodHRwczovL3MuZ3JhdmF0YXIuY29tL2F2YXRhci9mYmQ3ZDEwNDcyMTM4ZGI2YmRlNGIyMjdkOTMwN2JlMD9zPTQ4MCZyPXBnJmQ9aHR0cHMlM0ElMkYlMkZjZG4uYXV0aDAuY29tJTJGYXZhdGFycyUyRnFmLnBuZyIsInVwZGF0ZWRfYXQiOiIyMDE5LTA2LTIwVDAyOjAxOjQxLjQ4OVoiLCJlbWFpbCI6InFmcDE5NjM3QGJjYW9vLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwiaXNzIjoiaHR0cHM6Ly9uZW90aGVpY2ViaXJkLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZDA4MWRmODcxZGVlYTBkZDE0Y2U2M2EiLCJhdWQiOiJ0N2lvTkdYZmF1Q0U4aFN0Mzk1MU5uUlFWRno0RmNnciIsImlhdCI6MTU2MDk5NjEwMSwiZXhwIjoxNTYxMDMyMTAxfQ.yIFiTG4Sq3uTgiBlsFHAzmCy-8pPs1ODZfG_AN0ZP_WOimitUFeNnqoP7s1KrCjpIJOiZhbhmKXE0Jy4DsTeAj_mT9LlS-W4muvEfQm_MX2XL70aCFHA2ws_IVN-OzCNVZmhNGVCAtIsFMNBOKaAnD7CitiI8kmOii1p5NVrY5A5HYm9aV7odp3lmJKQmTOVbxq0zuQ9E_8tPChdvysv1_TsBiSz_sdMLpg7Iq-nhyiOd1Eg4oiBoEAS7NgmVIxcdzBv3jc3zZOvVFsJdjdbWQzC4UtspaQFOl3VSfCZ3_KxnZJsvtk9P9CkOnAyHZKFFrQIUjT2sXExzKTKAAOaVw' \
  -H 'cache-control: no-cache'
```

Update Profile

```curl
curl -X PUT \
  $URL/user \
  -H 'authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IlFrSXpSVFkxTlRjMk1ESkVRVFJEUkRFeFF6RTBOekl3T1RnMlF6RkZNalExUWpNMlJFWXdNdyJ9.eyJuaWNrbmFtZSI6InFmcDE5NjM3IiwibmFtZSI6InFmcDE5NjM3QGJjYW9vLmNvbSIsInBpY3R1cmUiOiJodHRwczovL3MuZ3JhdmF0YXIuY29tL2F2YXRhci9mYmQ3ZDEwNDcyMTM4ZGI2YmRlNGIyMjdkOTMwN2JlMD9zPTQ4MCZyPXBnJmQ9aHR0cHMlM0ElMkYlMkZjZG4uYXV0aDAuY29tJTJGYXZhdGFycyUyRnFmLnBuZyIsInVwZGF0ZWRfYXQiOiIyMDE5LTA2LTIwVDAyOjAxOjQxLjQ4OVoiLCJlbWFpbCI6InFmcDE5NjM3QGJjYW9vLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwiaXNzIjoiaHR0cHM6Ly9uZW90aGVpY2ViaXJkLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZDA4MWRmODcxZGVlYTBkZDE0Y2U2M2EiLCJhdWQiOiJ0N2lvTkdYZmF1Q0U4aFN0Mzk1MU5uUlFWRno0RmNnciIsImlhdCI6MTU2MDk5NjEwMSwiZXhwIjoxNTYxMDMyMTAxfQ.yIFiTG4Sq3uTgiBlsFHAzmCy-8pPs1ODZfG_AN0ZP_WOimitUFeNnqoP7s1KrCjpIJOiZhbhmKXE0Jy4DsTeAj_mT9LlS-W4muvEfQm_MX2XL70aCFHA2ws_IVN-OzCNVZmhNGVCAtIsFMNBOKaAnD7CitiI8kmOii1p5NVrY5A5HYm9aV7odp3lmJKQmTOVbxq0zuQ9E_8tPChdvysv1_TsBiSz_sdMLpg7Iq-nhyiOd1Eg4oiBoEAS7NgmVIxcdzBv3jc3zZOvVFsJdjdbWQzC4UtspaQFOl3VSfCZ3_KxnZJsvtk9P9CkOnAyHZKFFrQIUjT2sXExzKTKAAOaVw' \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/json'
  -d '{
    "marketplaces": [
        {
            "name": "codementor",
            "profile_url": "www.codementor.io/prashanthx","enabled": true,
            "picture": false,
            "skills": false,
            "focus": true,
            "pricing": false
        },
        {
            "name": "upwork",
            "profile_url": "www.upwork.com/prashanthg","enabled": false,
            "picture": false,
            "skills": false,
            "focus": false,
            "pricing": false
        }
    ],
    "lastname": "User",
    "firstname": "Test",
    "user_id": "5d0810c271deea0dd14ce5a6",
    "email": "ocw69080@onqus.com",
    "affiliate_id": "XNBQFO",
    "timezone_name": "utc",
    "timezone_utc_offset": 0,
    "workday_start_time": "09:00",
    "entity_id": "5d0810c271deea0dd14ce5a6",
    "version": "2adbe6c6-0b10-4610-b119-223c7250d601",
    "changed_on": "2019-06-06T08:41:06Z"
}'
```

Delete Profile

```curl
curl -X DELETE \
  $URL/user \
  -H 'authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IlFrSXpSVFkxTlRjMk1ESkVRVFJEUkRFeFF6RTBOekl3T1RnMlF6RkZNalExUWpNMlJFWXdNdyJ9.eyJuaWNrbmFtZSI6InFmcDE5NjM3IiwibmFtZSI6InFmcDE5NjM3QGJjYW9vLmNvbSIsInBpY3R1cmUiOiJodHRwczovL3MuZ3JhdmF0YXIuY29tL2F2YXRhci9mYmQ3ZDEwNDcyMTM4ZGI2YmRlNGIyMjdkOTMwN2JlMD9zPTQ4MCZyPXBnJmQ9aHR0cHMlM0ElMkYlMkZjZG4uYXV0aDAuY29tJTJGYXZhdGFycyUyRnFmLnBuZyIsInVwZGF0ZWRfYXQiOiIyMDE5LTA2LTIwVDAyOjAxOjQxLjQ4OVoiLCJlbWFpbCI6InFmcDE5NjM3QGJjYW9vLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwiaXNzIjoiaHR0cHM6Ly9uZW90aGVpY2ViaXJkLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZDA4MWRmODcxZGVlYTBkZDE0Y2U2M2EiLCJhdWQiOiJ0N2lvTkdYZmF1Q0U4aFN0Mzk1MU5uUlFWRno0RmNnciIsImlhdCI6MTU2MDk5NjEwMSwiZXhwIjoxNTYxMDMyMTAxfQ.yIFiTG4Sq3uTgiBlsFHAzmCy-8pPs1ODZfG_AN0ZP_WOimitUFeNnqoP7s1KrCjpIJOiZhbhmKXE0Jy4DsTeAj_mT9LlS-W4muvEfQm_MX2XL70aCFHA2ws_IVN-OzCNVZmhNGVCAtIsFMNBOKaAnD7CitiI8kmOii1p5NVrY5A5HYm9aV7odp3lmJKQmTOVbxq0zuQ9E_8tPChdvysv1_TsBiSz_sdMLpg7Iq-nhyiOd1Eg4oiBoEAS7NgmVIxcdzBv3jc3zZOvVFsJdjdbWQzC4UtspaQFOl3VSfCZ3_KxnZJsvtk9P9CkOnAyHZKFFrQIUjT2sXExzKTKAAOaVw' \
  -H 'cache-control: no-cache'
```