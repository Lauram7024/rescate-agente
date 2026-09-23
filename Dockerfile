FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
ENV LLM_API_KEY=sk-live-lab10-9f3b2c7d1e4a4b8c9d0e1f2a3b4c5d6e
EXPOSE 8080
CMD ["python", "-m", "agent.server"]
