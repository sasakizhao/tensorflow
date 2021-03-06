# Lint as: python3
# Copyright 2020 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""TF2 parameter server training utilities.

Parameter server training in TF2 is currently under development.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from absl import logging
from tensorflow.python.training import server_lib


def start_server(cluster_resolver):
  """Start a server and block the process from exiting."""
  # Note: If the user is using borg/xmanager/tfx, they can simply have
  # workers and ps's start tensorflow std server without having to run
  # this the python binary. This function is for multi-processing
  # test or users who would like to have every job run the same binary for
  # simplicity.
  assert (cluster_resolver.task_type == 'worker' or
          cluster_resolver.task_type == 'ps')
  server = server_lib.Server(
      cluster_resolver.cluster_spec().as_cluster_def(),
      job_name=cluster_resolver.task_type,
      task_index=cluster_resolver.task_id,
      protocol='grpc+loas')

  logging.info('TensorFlow server started for job %s, task %d.',
               cluster_resolver.task_type, cluster_resolver.task_id)

  # Blocking the process that starts a server from exiting.
  server.join()
