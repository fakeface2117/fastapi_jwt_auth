from app.auth.auth_schemas import UserSchema
from app.auth.utils import hash_password

petr = UserSchema(
    username="petr",
    password=hash_password("1234"),
    email="petr@example.com",
)

ivan = UserSchema(
    username="ivan",
    password=hash_password("1234"),
)

user_db: dict = {
    petr.username: petr,
    ivan.username: ivan,
}
