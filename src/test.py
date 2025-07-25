import sys
sys.path.append("src")
from agent import predict_sleep_stage

print(predict_sleep_stage(1, mood="tired"))