# -*- coding: utf-8 -*-
"""
.. See the NOTICE file distributed with this work for additional information
   regarding copyright ownership.
   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at
       http://www.apache.org/licenses/LICENSE-2.0
   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from ensembl_dbcopy.api.serializers import *
from ensembl_dbcopy.models import *

class RequestJobViewSet(viewsets.ModelViewSet):
    serializer_class = RequestJobSerializerUser
    queryset = RequestJob.objects.all()


class TransferLogViewSet(viewsets.ModelViewSet):
    serializer_class = TransferLogSerializer
    queryset = TransferLog.objects.filter()
    http_method_names = ['get']