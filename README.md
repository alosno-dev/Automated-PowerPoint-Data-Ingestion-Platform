# Automated-PowerPoint-Data-Ingestion-Platform
End-to-end system that automatically extracts, normalizes, and ingests vehicle data from PowerPoint files into a web platform using FastAPI, n8n, and AI agents.

## Key Features
- Automated ingestion of vehicle data from PowerPoint
- OCR and computer vision–based image classification
- Automatic detection, extraction, and publishing of vehicle label images
- AI-powered data normalization
- Orchestrated workflows with n8n

## Problem
Vehicle providers delivered data in inconsistent PowerPoint formats, requiring manual processing and high operational cost.

## Solution
I designed and implemented an automated pipeline that:
1. Extracts structured and unstructured data from PowerPoint
2. Processes images and pricing tables
3. Normalizes data using AI agents
4. Stores validated data directly into the platform database

## Architecture

- FastAPI backend (Dockerized)
- n8n as workflow orchestrator
- OCR with Tesseract
- Computer Vision with OpenCV for visual element detection and image categorization
- AI agents for normalization

## Data Ingestion Flow

1. PowerPoint file uploaded to the system
2. Backend extracts:
   - Slide text
   - Images
   - Pricing tables (OCR)
3. OpenCV analyzes slide images to:
   - Categorize vehicle label images
   - Detect label position and size within the slide
   - Extract and crop label images based on spatial metadata
4. Extracted label images are uploaded to the web server and linked to the corresponding vehicle records
5. n8n orchestrates:
   - API calls
   - Data persistence
   - AI-based normalization
6. Clean data is stored in the database

## Tech Stack
Backend
- Python
- FastAPI – REST API for data ingestion and processing
- Uvicorn – ASGI server
- Docker – Containerization and deployment
- Render – Cloud deployment platform

Workflow Orchestration & Automation
- n8n – Workflow orchestration, API consumption, data persistence, and automation logic

Data Extraction & Processing
- python-pptx – PowerPoint slide parsing
- Tesseract OCR – Extraction of pricing tables from slides
- OpenCV – Image processing, visual element categorization, and spatial analysis to extract vehicle label images based on size and position

Artificial Intelligence
- LLM-based AI Agent – Data normalization, structuring, and validation of unstructured information

Databases
- Redis - N8N orchestration between paralallel workflows executions
- Relational Database (MySQL) – Vehicle data persistence

DevOps & Tooling
- Docker Compose – Local development orchestration
- Git & GitHub – Version control and collaboration
- Environment-based configuration (.env)

## Computer Vision Logic

OpenCV is used to analyze slide images and identify vehicle label elements based on visual characteristics, spatial position, and relative size.  
Once detected, label images are dynamically cropped, categorized, and uploaded to the web server, where they are associated with the corresponding vehicle records.
