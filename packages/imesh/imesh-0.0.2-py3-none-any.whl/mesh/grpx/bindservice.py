#
# Copyright (c) 2000, 2099, trustbe and/or its affiliates. All rights reserved.
# TRUSTBE PROPRIETARY/CONFIDENTIAL. Use is subject to license terms.
#
#

import mesh.log as log

import grpc

from mesh.grpx.marshaller import GrpcMarshaller


class GrpcBindableService(grpc.GenericRpcHandler):

    def __init__(self):
        self.marshaller = GrpcMarshaller()
        rpc_method_handlers = {
            "mesh-rpc/v1": grpc.stream_stream_rpc_method_handler(
                "mesh-rpc/v1",
                request_deserializer=self.marshaller.deserialize,
                response_serializer=self.marshaller.serialize,
            ),
        }
        grpc.method_handlers_generic_handler("mesh-rpc", rpc_method_handlers)

    def service(self, handler_call_details):
        log.info(handler_call_details)
