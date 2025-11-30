param([int]$Port = 8501)
Write-Host "Starting Streamlit on port $Port"
& "C:/ProgramData/Anaconda3/python.exe" -m streamlit run aap.py --server.port $Port --server.address 0.0.0.0 --server.headless true
