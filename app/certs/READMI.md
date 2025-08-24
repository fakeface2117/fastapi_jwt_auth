Сгенерировать приватный ключ 

```PowerShell
& 'C:\Program Files\OpenSSL-Win64\bin\openssl.exe' genrsa -out jwt-private.pem 2048
```

Сгенерировать публичный ключ

```PowerShell
& 'C:\Program Files\OpenSSL-Win64\bin\openssl.exe' rsa -in jwt-private.pem -pubout -out jwt-public.pem
```