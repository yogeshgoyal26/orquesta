# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging

from orchestra.specs import types
from orchestra.specs.mistral.v2 import base
from orchestra.specs.mistral.v2 import tasks


LOG = logging.getLogger(__name__)


def instantiate(definition):
    definition.pop('version', None)

    if len(definition.keys()) > 1:
        raise ValueError('Workflow definition contains more than one workflow.')

    wf_name, wf_spec = list(definition.items())[0]

    return WorkflowSpec(wf_spec, name=wf_name)


class WorkflowSpec(base.Spec):
    _schema = {
        'type': 'object',
        'properties': {
            'vars': types.NONEMPTY_DICT,
            'input': types.UNIQUE_STRING_OR_ONE_KEY_DICT_LIST,
            'output': types.NONEMPTY_DICT,
            'task-defaults': tasks.TaskDefaultsSpec,
            'tasks': tasks.TaskMappingSpec
        },
        'required': ['tasks'],
        'additionalProperties': False
    }

    _context_evaluation_sequence = [
        'input',
        'vars',
        'tasks',
        'output'
    ]

    _context_inputs = [
        'input',
        'vars'
    ]


class WorkbookSpec(base.Spec):
    _schema = {
        'type': 'object',
        'properties': {
            'workflows': {
                'type': 'object',
                'minProperties': 1,
                'patternProperties': {
                    '^(?!version)\w+$': WorkflowSpec
                }
            }
        },
        'additionalProperties': False
    }
