import pickle
import time

import grpc
import habitat

from concurrent import futures

import evaluation_pb2
import evaluation_pb2_grpc


def pack_for_grpc(entity):
    return pickle.dumps(entity)

def unpack_for_grpc(entity):
    return pickle.loads(entity)


class Environment(evaluation_pb2_grpc.EnvironmentServicer):

    def get_action_space(self, request, context):
        challenge = habitat.Challenge()
        agent = unpack_for_grpc(request.SerializedEntity)
        challenge.submit(agent)
        return evaluation_pb2.Package(SerializedEntity=agent)

server = grpc.server(futures.ThreadPoolExecutor(max_workers = 10))
evaluation_pb2_grpc.add_EnvironmentServicer_to_server(Environment(), server)


print('Starting server. Listening on port 8080.')
server.add_insecure_port('[::]:8080')
server.start()
# time.sleep(10)
try:
    while True:
        time.sleep(4)
except KeyboardInterrupt:
    server.stop(0)
