# 使用官方的 Python 映像
FROM python:3.10-slim

# 設置工作目錄
WORKDIR /app

# 複製 requirements.txt 並安裝 Python 依賴
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製應用程式碼到容器內
COPY . .

# 創建 cache 目錄
RUN mkdir -p /app/cache

# 設置 transformers cache 目錄
ENV HF_HOME=/app/cache

# 暴露端口
EXPOSE 7860

# 運行應用
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
