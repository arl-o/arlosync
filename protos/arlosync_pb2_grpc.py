# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from arlosync.protos import arlosync_pb2 as arlosync__pb2


class SyncClientStub(object):
    """RPC server of the sync client.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetBytesAndTokensForFile = channel.unary_stream(
                '/arlosync.SyncClient/GetBytesAndTokensForFile',
                request_serializer=arlosync__pb2.FileAndTokens.SerializeToString,
                response_deserializer=arlosync__pb2.BytesAndTokens.FromString,
                )
        self.GetBytesAndTokensForDirectoryDescriptor = channel.unary_stream(
                '/arlosync.SyncClient/GetBytesAndTokensForDirectoryDescriptor',
                request_serializer=arlosync__pb2.FileAndTokens.SerializeToString,
                response_deserializer=arlosync__pb2.BytesAndTokens.FromString,
                )


class SyncClientServicer(object):
    """RPC server of the sync client.
    """

    def GetBytesAndTokensForFile(self, request, context):
        """Returns an ordered stream of literal bytes and tokens which can be used to
        reconstruct the client's version of the specified file.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetBytesAndTokensForDirectoryDescriptor(self, request, context):
        """Returns an ordered stream of literal bytes and tokens which can be used to
        reconstruct the client's `DirectoryDescriptor` proto.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_SyncClientServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetBytesAndTokensForFile': grpc.unary_stream_rpc_method_handler(
                    servicer.GetBytesAndTokensForFile,
                    request_deserializer=arlosync__pb2.FileAndTokens.FromString,
                    response_serializer=arlosync__pb2.BytesAndTokens.SerializeToString,
            ),
            'GetBytesAndTokensForDirectoryDescriptor': grpc.unary_stream_rpc_method_handler(
                    servicer.GetBytesAndTokensForDirectoryDescriptor,
                    request_deserializer=arlosync__pb2.FileAndTokens.FromString,
                    response_serializer=arlosync__pb2.BytesAndTokens.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'arlosync.SyncClient', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class SyncClient(object):
    """RPC server of the sync client.
    """

    @staticmethod
    def GetBytesAndTokensForFile(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/arlosync.SyncClient/GetBytesAndTokensForFile',
            arlosync__pb2.FileAndTokens.SerializeToString,
            arlosync__pb2.BytesAndTokens.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetBytesAndTokensForDirectoryDescriptor(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/arlosync.SyncClient/GetBytesAndTokensForDirectoryDescriptor',
            arlosync__pb2.FileAndTokens.SerializeToString,
            arlosync__pb2.BytesAndTokens.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
