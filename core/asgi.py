"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = get_asgi_application()

# from fastapi import FastAPI
# from portfolio.urls import router as p_router

# app = FastAPI(
#     title='Cumbia',
#     description='API del portfolio de la productora Cumbia.',
#     version='0.1'
# )

# app.include_router(p_router, prefix='/portfolio')