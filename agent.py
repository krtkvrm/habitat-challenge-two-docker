import pickle

import grpc
import argparse
from baselines.agents.simple_agents import get_agent_cls
import evaluation_pb2
import evaluation_pb2_grpc
import time

time.sleep(10)


channel = grpc.insecure_channel("localhost:8080")

stub = evaluation_pb2_grpc.EnvironmentStub(channel)


def pack_for_grpc(entity):
    return pickle.dumps(entity)


def unpack_for_grpc(entity):
    return pickle.loads(entity)


parser = argparse.ArgumentParser()
parser.add_argument("--agent-class", type=str, default="GoalFollower")
args = parser.parse_args()

agent = get_agent_cls(args.agent_class)(success_distance=0.2)

result = unpack_for_grpc(
    stub.get_action_space(evaluation_pb2.Package(SerializedEntity=pack_for_grpc(agent))).SerializedEntity
)
