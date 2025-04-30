import whisper

model = whisper.load_model("base")  # 可以换成 "small" 或 "medium" 提高准确率
result = model.transcribe("新录音-8.wav", language="ja")

print(result["text"])
