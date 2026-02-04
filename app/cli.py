import getpass
from uuid import uuid4

import click
from flask.cli import with_appcontext

from app.auth import hash_password
from app.db import session_scope
from app.models import AdminUser


def register_cli(app):
    @app.cli.command("create-admin")
    @click.argument("username")
    @with_appcontext
    def create_admin(username: str):
        password = getpass.getpass("Пароль администратора: ")
        password_confirm = getpass.getpass("Повторите пароль: ")
        if password != password_confirm:
            raise click.ClickException("Пароли не совпадают.")
        with session_scope() as session:
            existing = session.query(AdminUser).filter_by(username=username).one_or_none()
            if existing:
                raise click.ClickException("Пользователь уже существует.")
            session.add(
                AdminUser(
                    id=uuid4().hex,
                    username=username,
                    password_hash=hash_password(password),
                    is_active=True,
                )
            )
        click.echo("Администратор создан.")
