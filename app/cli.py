import asyncio
import click
from alembic.config import Config
from alembic import command
from sqlalchemy.ext.asyncio import create_async_engine
from app.core.config import settings
from app.models.base import Base

@click.group()
def cli():
    """Database management commands"""
    pass

@cli.command()
def init_db():
    """Initialize database with Alembic"""
    click.echo("Initializing Alembic...")
    alembic_cfg = Config("alembic.ini")
    command.init(alembic_cfg, "alembic")
    click.echo("Alembic initialized!")

@cli.command()
@click.option('--message', '-m', required=True, help='Migration message')
def create_migration(message: str):
    """Create a new migration"""
    click.echo(f"Creating migration: {message}")
    alembic_cfg = Config("alembic.ini")
    command.revision(alembic_cfg, message=message, autogenerate=True)
    click.echo("Migration created!")

@cli.command()
def upgrade():
    """Run database migrations"""
    click.echo("Running migrations...")
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
    click.echo("Migrations completed!")

@cli.command()
@click.option('--revision', '-r', default='-1', help='Revision to downgrade to')
def downgrade(revision: str):
    """Downgrade database"""
    click.echo(f"Downgrading to revision: {revision}")
    alembic_cfg = Config("alembic.ini")
    command.downgrade(alembic_cfg, revision)
    click.echo("Downgrade completed!")

@cli.command()
def current():
    """Show current revision"""
    alembic_cfg = Config("alembic.ini")
    command.current(alembic_cfg)

@cli.command()
def history():
    """Show migration history"""
    alembic_cfg = Config("alembic.ini")
    command.history(alembic_cfg)

if __name__ == '__main__':
    cli()