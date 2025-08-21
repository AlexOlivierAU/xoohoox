from setuptools import setup, find_packages

setup(
    name="xoohoox-backend",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "alembic",
        "pydantic",
        "pydantic-settings",
        "python-jose[cryptography]",
        "passlib[bcrypt]",
        "python-multipart",
        "redis",
        "httpx",
        "pytest",
        "pytest-asyncio",
        "email-validator",
        "aiofiles",
        "python-dateutil",
        "pytz"
    ],
) 