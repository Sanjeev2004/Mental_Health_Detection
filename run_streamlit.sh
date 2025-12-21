#!/bin/bash
echo "Starting Mental Health Detection Streamlit App..."
echo ""
streamlit run app/app.py --server.port 8501 --server.address localhost
