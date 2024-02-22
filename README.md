# MedicalAid Summarizer

This repository contains the required functions & classes for the project: MedicalAid Summarizer
The intention of this project is to be capable to generate insights from PubMed articles regarding a specific brand so that
users can generate marketing materials for healthcare professionals.

## Clone of the project

```
git clone https://github.com/ericmatamoros/hcp_llm.git

cd hcp_llm
```

## Handling environment

This project is compatible with environments. We highly encourage to create a new environment for this project to better handle all
dependencies and avoid conflicts.

## Set up virtual environment & install dependencies

All the project dependencies are found in the requirements.txt file.

```
# Install specific environments
make venv
```

## Configuration Files

Configuration parameters can be found inside the folder hcp_llm}/config/, with the config.yaml filename.

## API Keys

Since the project is using OpenAI models, you need to gather an API first and then place it in a .env file on the root
directory of the project as follows:

OPENAI_KEY=api_key

## Run Streamlit App

Streamlit app can be executed through:

```
streamlit run app.py
```

## Contributors

- [Eric Matamoros](ericmatamoros1999@gmail.com) or (eric.matamoros@novartis.net)