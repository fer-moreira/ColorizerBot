from core.engine import DeepLearning

dp = DeepLearning("sample_bw.jpg", "sample_predict.jpg")

dp.resolution_x = 200
dp.resolution_y = 200

dp.load()
dp.build()