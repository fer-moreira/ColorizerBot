from core.engine import DeepLearning

dp = DeepLearning("sample_bw.jpg", "sample_predict.jpg")

dp.prototxt_path = "./core/models/network.prototxt"
dp.caffemodel_path = "./core/models/model.caffemodel"

dp.resolution_x = 200
dp.resolution_y = 200

dp.load()
dp.build()