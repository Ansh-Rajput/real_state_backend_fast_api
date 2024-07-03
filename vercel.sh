#!/bin/bash
# Install Python dependencies
pip install -r requirements.txt

# Generate Prisma client
prisma generate
