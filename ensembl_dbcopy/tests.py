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

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from ensembl_dbcopy.models import *
import json

User = get_user_model()


class RequestJobTest(APITestCase):
    """ Test module for RequestJob model """
    multi_db = True
    using_db = 'dbcopy'
    fixtures = ['ensembl_dbcopy']
    # Test requestjob endpoint
    def testRequestJob(self):
        # Check get all
        response = self.client.get(reverse('requestjob-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Test post
        response = self.client.post(reverse('requestjob-list'),
                                    {'src_host': 'mysql-ens-sta-1', 'src_incl_db': 'homo_sapiens_core_99_38', 'tgt_host': 'mysql-ens-general-dev-1', 'user' : 'testuser'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Test user email
        response_dict = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response_dict['email_list'], 'testuser@ebi.ac.uk')
        # Test bad post
        response = self.client.post(reverse('requestjob-list'),
                                    {'src_host': '', 'src_incl_db': 'homo_sapiens_core_99_38', 'tgt_host': 'mysql-ens-general-dev-1'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Test get
        response = self.client.get(reverse('requestjob-detail', kwargs={'job_id': '8f084180-07ae-11ea-ace0-9801a79243a5'}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Test bad get
        response = self.client.get(reverse('requestjob-detail', kwargs={'job_id': 'd662656c-0a18-11ea-ab6c-9801a79243a5'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # Test Transfer log
        response = self.client.get(reverse('requestjob-detail', kwargs={'job_id': 'ddbdc15a-07af-11ea-bdcd-9801a79243a5'}))
        response_dict = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(response_dict['transfer_log']), 2)
        # Test put
        response = self.client.put(reverse('requestjob-detail', kwargs={'job_id': '8f084180-07ae-11ea-ace0-9801a79243a5'}),
                                    {'src_host': 'mysql-ens-sta-1', 'src_incl_db': 'homo_sapiens_core_99_38', 'tgt_host': 'mysql-ens-general-dev-2'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Test bad put
        response = self.client.put(reverse('requestjob-detail', kwargs={'job_id':'d662656c-0a18-11ea-ab6c-9801a79243a5'}),
                                    {'src_host': 'mysql-ens-sta-1', 'src_incl_db': 'homo_sapiens_core_99_38', 'tgt_host': 'mysql-ens-general-dev-2'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # Test patch
        response = self.client.patch(reverse('requestjob-detail', kwargs={'job_id': '8f084180-07ae-11ea-ace0-9801a79243a5'}),
                                      {'src_incl_db': 'homo_sapiens_funcgen_99_38'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Test bad patch
        response = self.client.patch(reverse('requestjob-detail', kwargs={'job_id': 'd662656c-0a18-11ea-ab6c-9801a79243a5'}),
                                      {'src_incl_db': 'homo_sapiens_funcgen_99_38'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # Test delete
        response = self.client.delete(reverse('requestjob-detail', kwargs={'job_id': '8f084180-07ae-11ea-ace0-9801a79243a5'}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Test bad delete
        response = self.client.delete(reverse('requestjob-detail', kwargs={'job_id': '673f3b10-09e6-11ea-9206-9801a79243a5'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Test host endpoint
    def testHost(self):
        # Test get
        response = self.client.get(reverse('host-detail', kwargs={'name': 'mysql-ens-sta-1'}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Test bad get
        response = self.client.get(reverse('host-detail', kwargs={'name': 'mysql-ens-compara-2'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # Test getting 2 mysql-ens-sta-2 servers
        response = self.client.get(reverse('host-list'), {'name': 'mysql-ens-sta'})
        response_dict = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response_dict['count'], 2)
        # Test getting mysql-ens-general-dev-1 server
        response = self.client.get(reverse('host-list'), {'name': 'mysql-ens-general'})
        response_dict = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response_dict['count'], 1)

    # Test DatabaseList endpoint
    def testDatabaseList(self):
        # Test getting test Production dbs
        response = self.client.get(reverse('databaselist'), {'host': '127.0.0.1','port': '3306','user':'ensembl','database': 'test_ensembl_production'})
        response_list = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(response_list), 2)

    # Test TableList endpoint
    def testTableList(self):
        # Test getting meta_key table for Production dbs
        response = self.client.get(reverse('tablelist'), {'host': '127.0.0.1','port': '3306','user':'ensembl','database': 'test_ensembl_production','table':'meta'})
        response_list = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(response_list), 1)