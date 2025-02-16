"""Module compliance_suite.models.v1_0_0_specs.py

Pydantic generated models for TES API Specs v1.0.0
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

from pydantic import AnyUrl, BaseModel, Field, EmailStr, validator, ValidationError
from pydantic.tools import parse_obj_as


class TesCancelTaskResponse(BaseModel):
    pass


class TesCreateTaskResponse(BaseModel):
    id: str = Field(..., description='Task identifier assigned by the server.')


class TesExecutor(BaseModel):
    image: str = Field(
        ...,
        description='Name of the container image. The string will be passed as the image\nargument to the '
                    'containerization run command. Examples:\n   - `ubuntu`\n   - `quay.io/aptible/ubuntu`\n   - '
                    '`gcr.io/my-org/my-image`\n   - `myregistryhost:5000/fedora/httpd:version1.0`',
        example='ubuntu:20.04',
    )
    command: List[str] = Field(
        ...,
        description='A sequence of program arguments to execute, where the first argument\nis the program to '
                    'execute (i.e. argv). Example:\n```\n{\n  "command" : ["/bin/md5", "/data/file1"]\n}\n```',
        example=['/bin/md5', '/data/file1'],
    )
    workdir: Optional[str] = Field(
        None,
        description='The working directory that the command will be executed in.\nIf not defined, the system will '
                    'default to the directory set by\nthe container image.',
        example='/data/',
    )
    stdin: Optional[str] = Field(
        None,
        description='Path inside the container to a file which will be piped\nto the executor\'s stdin. This must be '
                    'an absolute path. This mechanism\ncould be used in conjunction with the input declaration to '
                    'process\na data file using a tool that expects STDIN.\n\nFor example, to get the MD5 sum of a '
                    'file by reading it into the STDIN\n```\n{\n  "command" : ["/bin/md5"],\n  '
                    '"stdin" : "/data/file1"\n}\n```',
        example='/data/file1',
    )
    stdout: Optional[str] = Field(
        None,
        description='Path inside the container to a file where the executor\'s\nstdout will be written to. '
                    'Must be an absolute path. Example:\n```\n{\n  "stdout" : "/tmp/stdout.log"\n}\n```',
        example='/tmp/stdout.log',
    )
    stderr: Optional[str] = Field(
        None,
        description='Path inside the container to a file where the executor\'s\nstderr will be written to. Must be '
                    'an absolute path. Example:\n```\n{\n  "stderr" : "/tmp/stderr.log"\n}\n```',
        example='/tmp/stderr.log',
    )
    env: Optional[Dict[str, str]] = Field(
        None,
        description='Enviromental variables to set within the container. Example:\n```\n{\n  "env" : {\n    '
                    '"ENV_CONFIG_PATH" : "/data/config.file",\n    "BLASTDB" : "/data/GRC38",\n    '
                    '"HMMERDB" : "/data/hmmer"\n  }\n}\n```',
        example={'BLASTDB': '/data/GRC38', 'HMMERDB': '/data/hmmer'},
    )


class TesExecutorLog(BaseModel):
    start_time: Optional[str] = Field(
        None,
        description='Time the executor started, in RFC 3339 format.',
        example='2020-10-02T15:00:00.000Z',
    )
    end_time: Optional[str] = Field(
        None,
        description='Time the executor ended, in RFC 3339 format.',
        example='2020-10-02T16:00:00.000Z',
    )
    stdout: Optional[str] = Field(
        None,
        description='Stdout content.\n\nThis is meant for convenience. No guarantees are made about the '
                    'content.\nImplementations may chose different approaches: only the head, only the tail,\na URL '
                    'reference only, etc.\n\nIn order to capture the full stdout client should set '
                    'Executor.stdout\nto a container file path, and use Task.outputs to upload that file\nto '
                    'permanent storage.',
    )
    stderr: Optional[str] = Field(
        None,
        description='Stderr content.\n\nThis is meant for convenience. No guarantees are made about the '
                    'content.\nImplementations may chose different approaches: only the head, only the tail,\na URL '
                    'reference only, etc.\n\nIn order to capture the full stderr client should set '
                    'Executor.stderr\nto a container file path, and use Task.outputs to upload that file\nto '
                    'permanent storage.',
    )
    exit_code: int = Field(..., description='Exit code.')


class TesFileType(Enum):
    FILE = 'FILE'
    DIRECTORY = 'DIRECTORY'


class TesInput(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = Field(
        None,
        description='REQUIRED, unless "content" is set.\n\nURL in long term storage, for example:\n - '
                    's3://my-object-store/file1\n - gs://my-bucket/file2\n - file:///path/to/my/file\n - '
                    '/path/to/my/file',
        example='s3://my-object-store/file1',
    )
    path: str = Field(
        ...,
        description='Path of the file inside the container.\nMust be an absolute path.',
        example='/data/file1',
    )
    type: TesFileType
    content: Optional[str] = Field(
        None,
        description='File content literal.\n\nImplementations should support a minimum of 128 KiB in this '
                    'field\nand may define their own maximum.\n\nUTF-8 encoded\n\nIf content is not empty, '
                    '"url" must be ignored.',
    )


class TesOutput(BaseModel):
    name: Optional[str] = Field(None, description='User-provided name of output file')
    description: Optional[str] = Field(
        None,
        description='Optional users provided description field, can be used for documentation.',
    )
    url: str = Field(
        ...,
        description='URL for the file to be copied by the TES server after the task is complete.\nFor '
                    'Example:\n - `s3://my-object-store/file1`\n - `gs://my-bucket/file2`\n - '
                    '`file:///path/to/my/file`',
    )
    path: str = Field(
        ...,
        description='Path of the file inside the container.\nMust be an absolute path.',
    )
    type: TesFileType


class TesOutputFileLog(BaseModel):
    url: str = Field(
        ..., description='URL of the file in storage, e.g. s3://bucket/file.txt'
    )
    path: str = Field(
        ...,
        description='Path of the file inside the container. Must be an absolute path.',
    )
    size_bytes: str = Field(
        ...,
        description="Size of the file in bytes. Note, this is currently coded as a string\nbecause official "
                    "JSON doesn't support int64 numbers.",
        example=['1024'],
    )


class TesResources(BaseModel):
    cpu_cores: Optional[int] = Field(
        None, description='Requested number of CPUs', example=4
    )
    preemptible: Optional[bool] = Field(
        None,
        description="Define if the task is allowed to run on preemptible compute instances,\nfor example, "
                    "AWS Spot. This option may have no effect when utilized\non some backends that don't have "
                    "the concept of preemptible jobs.",
        example=False,
    )
    ram_gb: Optional[float] = Field(
        None, description='Requested RAM required in gigabytes (GB)', example=8
    )
    disk_gb: Optional[float] = Field(
        None, description='Requested disk size in gigabytes (GB)', example=40
    )
    zones: Optional[List[str]] = Field(
        None,
        description='Request that the task be run in these compute zones. How this string\nis utilized '
                    'will be dependent on the backend system. For example, a\nsystem based on a cluster '
                    'queueing system may use this string to define\npriorty queue to which the job is assigned.',
        example='us-west-1',
    )


class Artifact(Enum):
    tes = 'tes'


class TesState(Enum):
    UNKNOWN = 'UNKNOWN'
    QUEUED = 'QUEUED'
    INITIALIZING = 'INITIALIZING'
    RUNNING = 'RUNNING'
    PAUSED = 'PAUSED'
    COMPLETE = 'COMPLETE'
    EXECUTOR_ERROR = 'EXECUTOR_ERROR'
    SYSTEM_ERROR = 'SYSTEM_ERROR'
    CANCELED = 'CANCELED'


class TesTaskLog(BaseModel):
    logs: List[TesExecutorLog] = Field(..., description='Logs for each executor')
    metadata: Optional[Dict[str, str]] = Field(
        None,
        description='Arbitrary logging metadata included by the implementation.',
        example={'host': 'worker-001', 'slurmm_id': 123456},
    )
    start_time: Optional[str] = Field(
        None,
        description='When the task started, in RFC 3339 format.',
        example='2020-10-02T15:00:00.000Z',
    )
    end_time: Optional[str] = Field(
        None,
        description='When the task ended, in RFC 3339 format.',
        example='2020-10-02T16:00:00.000Z',
    )
    outputs: List[TesOutputFileLog] = Field(
        ...,
        description='Information about all output files. Directory outputs are\nflattened into separate items.',
    )
    system_logs: Optional[List[str]] = Field(
        None,
        description='System logs are any logs the system decides are relevant,\nwhich are not tied directly '
                    'to an Executor process.\nContent is implementation specific: format, size, etc.\n\nSystem '
                    'logs may be collected here to provide convenient access.\n\nFor example, the system may '
                    'include the name of the host\nwhere the task is executing, an error message '
                    'that caused\na SYSTEM_ERROR state (e.g. disk is full), etc.\n\nSystem logs are '
                    'only included in the FULL task view.',
    )


class ServiceType(BaseModel):
    group: str = Field(
        ...,
        description="Namespace in reverse domain name format. Use `org.ga4gh` for implementations compliant "
                    "with official GA4GH specifications. For services with custom APIs not standardized by "
                    "GA4GH, or implementations diverging from official GA4GH specifications, use a different "
                    "namespace (e.g. your organization's reverse domain name).",
        example='org.ga4gh',
    )
    artifact: str = Field(
        ...,
        description='Name of the API or GA4GH specification implemented. Official GA4GH types should be assigned '
                    'as part of standards approval process. Custom artifacts are supported.',
        example='beacon',
    )
    version: str = Field(
        ...,
        description='Version of the API or specification. GA4GH specifications use semantic versioning.',
        example='1.0.0',
    )


class Organization(BaseModel):
    name: str = Field(
        ...,
        description='Name of the organization responsible for the service',
        example='My organization',
    )
    url: AnyUrl = Field(
        ...,
        description='URL of the website of the organization (RFC 3986 format)',
        example='https://example.com',
    )


class Service(BaseModel):
    id: str = Field(
        ...,
        description='Unique ID of this service. Reverse domain name notation is recommended, though not required. '
                    'The identifier should attempt to be globally unique so it can be used in downstream '
                    'aggregator services e.g. Service Registry.',
        example='org.ga4gh.myservice',
    )
    name: str = Field(
        ...,
        description='Name of this service. Should be human readable.',
        example='My project',
    )
    type: ServiceType
    description: Optional[str] = Field(
        None,
        description='Description of the service. Should be human readable and provide information about the service.',
        example='This service provides...',
    )
    organization: Organization = Field(
        ..., description='Organization providing the service'
    )
    contactUrl: Optional[str] = Field(
        None,
        description='URL of the contact for the provider of this service, e.g. a link to a contact form '
                    '(RFC 3986 format), or an email (RFC 2368 format).',
        example='mailto:support@example.com',
    )
    documentationUrl: Optional[AnyUrl] = Field(
        None,
        description='URL of the documentation of this service (RFC 3986 format). This should help someone '
                    'learn how to use your service, including any specifics required to access data, '
                    'e.g. authentication.',
        example='https://docs.myservice.example.com',
    )
    createdAt: Optional[datetime] = Field(
        None,
        description='Timestamp describing when the service was first deployed and available (RFC 3339 format)',
        example='2019-06-04T12:58:19Z',
    )
    updatedAt: Optional[datetime] = Field(
        None,
        description='Timestamp describing when the service was last updated (RFC 3339 format)',
        example='2019-06-04T12:58:19Z',
    )
    environment: Optional[str] = Field(
        None,
        description='Environment the service is running in. Use this to distinguish between production, '
                    'development and testing/staging deployments. Suggested values are prod, test, dev, '
                    'staging. However this is advised and not enforced.',
        example='test',
    )
    version: str = Field(
        ...,
        description='Version of the service being described. Semantic versioning is recommended, but '
                    'other identifiers, such as dates or commit hashes, are also allowed. The version should '
                    'be changed whenever the service is updated.',
        example='1.0.0',
    )

    @validator('contactUrl')
    def check_url_or_email(cls, value):
        if value.startswith("mailto:"):
            email = value[len("mailto:"):]
            try:
                EmailStr.validate(email)
                return value
            except ValidationError:
                raise ValueError("Invalid email address")
        else:
            try:
                parse_obj_as(AnyUrl, value)
                return value
            except ValidationError:
                raise ValueError("Invalid URL")


class TesServiceType(ServiceType):
    artifact: Artifact = Field(..., example='tes')


class TesServiceInfo(Service):
    storage: Optional[List[str]] = Field(
        None,
        description='Lists some, but not necessarily all, storage locations supported\nby the service.',
        example=[
            'file:///path/to/local/funnel-storage',
            's3://ohsu-compbio-funnel/storage',
        ],
    )
    type: TesServiceType = Field(...)


class TesTask(BaseModel):
    id: Optional[str] = Field(
        None,
        description='Task identifier assigned by the server.',
        example='job-0012345',
    )
    state: Optional[TesState] = None
    name: Optional[str] = Field(None, description='User-provided task name.')
    description: Optional[str] = Field(
        None,
        description='Optional user-provided description of task for documentation purposes.',
    )
    inputs: Optional[List[TesInput]] = Field(
        None,
        description='Input files that will be used by the task. Inputs will be downloaded\nand mounted into '
                    'the executor container as defined by the task request\ndocument.',
        example=[{'url': 's3://my-object-store/file1', 'path': '/data/file1'}],
    )
    outputs: Optional[List[TesOutput]] = Field(
        None,
        description='Output files.\nOutputs will be uploaded from the executor container to long-term storage.',
        example=[
            {
                'path': '/data/outfile',
                'url': 's3://my-object-store/outfile-1',
                'type': 'FILE',
            }
        ],
    )
    resources: Optional[TesResources] = None
    executors: List[TesExecutor] = Field(
        ...,
        description='An array of executors to be run. Each of the executors will run one\nat a time sequentially. '
                    'Each executor is a different command that\nwill be run, and each can utilize a different '
                    'docker image. But each of\nthe executors will see the same mapped inputs and volumes '
                    'that are declared\nin the parent CreateTask message.\n\nExecution stops on the first error.',
    )
    volumes: Optional[List[str]] = Field(
        None,
        description='Volumes are directories which may be used to share data between\nExecutors. Volumes are '
                    'initialized as empty directories by the\nsystem when the task starts and are mounted at the '
                    'same path\nin each Executor.\n\nFor example, given a volume defined at `/vol/A`,\nexecutor 1 '
                    'may write a file to `/vol/A/exec1.out.txt`, then\nexecutor 2 may read from that '
                    'file.\n\n(Essentially, this translates to a `docker run -v` flag where\nthe container path '
                    'is the same for each executor).',
        example=['/vol/A/'],
    )
    tags: Optional[Dict[str, str]] = Field(
        None,
        description='A key-value map of arbitrary tags. These can be used to store meta-data\nand annotations '
                    'about a task. Example:\n```\n{\n  "tags" : {\n      "WORKFLOW_ID" : "cwl-01234",\n      '
                    '"PROJECT_GROUP" : "alice-lab"\n  }\n}\n```',
        example={'WORKFLOW_ID': 'cwl-01234', 'PROJECT_GROUP': 'alice-lab'},
    )
    logs: Optional[List[TesTaskLog]] = Field(
        None,
        description='Task logging information.\nNormally, this will contain only one entry, but in the case '
                    'where\na task fails and is retried, an entry will be appended to this list.',
    )
    creation_time: Optional[str] = Field(
        None,
        description='Date + time the task was created, in RFC 3339 format.\nThis is set by the system, not the client.',
        example='2020-10-02T15:00:00.000Z',
    )


class TesListTasksResponse(BaseModel):
    tasks: List[TesTask] = Field(
        ...,
        description='List of tasks. These tasks will be based on the original submitted\ntask document, but with '
                    'other fields, such as the job state and\nlogging info, added/changed as the job progresses.',
    )
    next_page_token: Optional[str] = Field(
        None,
        description='Token used to return the next page of results. This value can be used\nin the `page_token` '
                    'field of the next ListTasks request.',
    )


# Extra models manually added for Minimal View
class TesTaskMinimal(BaseModel):
    id: str = Field(
        ...,
        description='Task identifier assigned by the server.',
        example='job-0012345',
    )
    state: TesState = Field(..., example='UNKNOWN')


class TesListTasksResponseMinimal(BaseModel):
    tasks: List[TesTaskMinimal] = Field(
        ...,
        description='List of tasks. These tasks will be based on the original submitted\ntask document, but with '
                    'other fields, such as the job state and\nlogging info, added/changed as the job progresses.',
    )
