from heaobject.data import AWSS3FileObject
from heaserver.service.runner import init_cmd_line, routes, start
from heaserver.service.db import awsservicelib
from heaserver.service.db import database
from heaserver.service.db.aws import S3Manager
from heaserver.service.db.awss3bucketobjectkey import KeyDecodeException, decode_key, split, encode_key
from heaserver.service.wstl import builder_factory, action, add_run_time_action
from heaserver.service import response
from aiohttp import web, hdrs
import mimetypes
import logging
from typing import Union
from multidict import istr

_logger = logging.getLogger(__name__)

# Non-standard mimetypes that we may assign to files in AWS S3 buckets.
MIME_TYPES = {'application/x.fastq': ['.fq', '.fastq'],  # https://en.wikipedia.org/wiki/FASTQ_format
              'application/x.vcf': ['.vcf'],  # https://en.wikipedia.org/wiki/Variant_Call_Format
              'application/x.fasta': ['.fasta', '.fa', '.fna', '.ffn', '.faa', '.frn'],  # https://en.wikipedia.org/wiki/FASTA_format
              'application/x.sam': ['.sam'],  # https://en.wikipedia.org/wiki/SAM_(file_format)
              'application/x.bam': ['.bam'],  # https://support.illumina.com/help/BS_App_RNASeq_Alignment_OLH_1000000006112/Content/Source/Informatics/BAM-Format.htm#:~:text=A%20BAM%20file%20(*.,file%20naming%20format%20of%20SampleName_S%23.
              'application/x.bambai': ['.bam.bai'],  # https://support.illumina.com/help/BS_App_RNASeq_Alignment_OLH_1000000006112/Content/Source/Informatics/BAM-Format.htm#:~:text=A%20BAM%20file%20(*.,file%20naming%20format%20of%20SampleName_S%23.
              'application/x.gff3': ['.gff'],  # https://en.wikipedia.org/wiki/General_feature_format and https://github.com/The-Sequence-Ontology/Specifications/blob/master/gff3.md
              'application/x.gvf': ['.gvf']  # https://github.com/The-Sequence-Ontology/Specifications/blob/master/gvf.md
             }


@routes.get('/ping')
async def ping(request: web.Request) -> web.Response:
    """
    For testing whether the service is up.

    :param request: the HTTP request.
    :return: Always returns status code 200.
    """
    return response.status_ok()


@routes.route('OPTIONS', '/volumes/{volume_id}/buckets/{bucket_id}/awss3files/{id}')
async def get_file_options(request: web.Request) -> web.Response:
    """
    Gets the allowed HTTP methods for a file resource.

    :param request: the HTTP request (required).
    :return: the HTTP response.
    ---
    summary: Allowed HTTP methods.
    tags:
        - heaserver-files-aws-s3
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the volume to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
        - name: bucket_id
          in: path
          required: true
          description: The id of the bucket to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A bucket id
              value: my-bucket
        - $ref: '#/components/parameters/id'
    responses:
      '200':
        description: Expected response to a valid request.
        content:
            text/plain:
                schema:
                    type: string
                    example: "200: OK"
      '404':
        $ref: '#/components/responses/404'
    """
    resp = await awsservicelib.has_file(request)
    if resp.status == 200:
        return await response.get_options(request, ['GET', 'POST', 'DELETE', 'HEAD', 'OPTIONS'])
    else:
        headers: dict[Union[str, istr], str] = {hdrs.CONTENT_TYPE: 'text/plain; charset=utf-8'}
        return response.status_generic(status=resp.status, body=resp.text, headers=headers)


@routes.get('/volumes/{volume_id}/buckets/{bucket_id}/awss3files/{id}/duplicator')
@action(name='heaserver-awss3files-file-duplicate-form')
async def get_file_duplicator(request: web.Request) -> web.Response:
    """
    Gets a form template for duplicating the requested file.

    :param request: the HTTP request. Required.
    :return: the requested form, or Not Found if the requested file was not found.
    """
    logger = logging.getLogger(__name__)
    id_ = request.match_info['id']
    try:
        id = encode_key(split(decode_key(id_))[0])
        add_run_time_action(request, name='heaserver-awss3files-file-get-target', rel='headata-target', path=(
            '/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/' + id) if id else '/volumes/{volume_id}/buckets/{bucket_id}')
        return await awsservicelib.get_file(request)
    except KeyDecodeException as e:
        logger.exception('Error getting parent key')
        return response.status_bad_request(f'Error getting parent folder: {e}')


@routes.post('/volumes/{volume_id}/buckets/{bucket_id}/awss3files/{id}/mover')
async def post_file_mover(request: web.Request) -> web.Response:
    """
    Posts the provided file to move it.

    :param request: the HTTP request.
    :return: a Response object with a status of No Content.
    ---
    summary: A specific file.
    tags:
        - heaserver-files-aws-s3
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the volume.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
        - name: bucket_id
          in: path
          required: true
          description: The id of the bucket.
          schema:
            type: string
          examples:
            example:
              summary: A bucket id
              value: my-bucket
        - $ref: '#/components/parameters/id'
    requestBody:
        description: The new name of the file and target for moving it.
        required: true
        content:
            application/vnd.collection+json:
              schema:
                type: object
              examples:
                example:
                  summary: The new name of the file and target for moving it.
                  value: {
                    "template": {
                      "data": [
                      {
                        "name": "display_name",
                        "value": "TheNewNameOfTheFile"
                      },
                      {
                        "name": "target",
                        "value": "http://localhost:8080/volumes/666f6f2d6261722d71757578/buckets/my-bucket/awss3files/"
                      }]
                    }
                  }
            application/json:
              schema:
                type: object
              examples:
                example:
                  summary: The new name of the file and target for moving it.
                  value: {
                    "display_name": "TheNewNameOfTheFile",
                    "target": "http://localhost:8080/volumes/666f6f2d6261722d71757578/buckets/my-bucket/awss3files/"
                  }
    responses:
      '204':
        $ref: '#/components/responses/204'
      '400':
        $ref: '#/components/responses/400'
      '404':
        $ref: '#/components/responses/404'
    """
    return await _move_object(request)


@routes.post('/volumes/{volume_id}/buckets/{bucket_id}/awss3files/{id}/duplicator')
async def post_file_duplicator(request: web.Request) -> web.Response:
    """
    Posts the provided file for duplication.

    :param request: the HTTP request.
    :return: a Response object with a status of Created and the object's URI in the
    ---
    summary: A specific file.
    tags:
        - heaserver-files-aws-s3
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the volume.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
        - name: bucket_id
          in: path
          required: true
          description: The id of the bucket.
          schema:
            type: string
          examples:
            example:
              summary: A bucket id
              value: my-bucket
        - $ref: '#/components/parameters/id'
    requestBody:
        description: The new name of the file and target for duplicating it.
        required: true
        content:
            application/vnd.collection+json:
              schema:
                type: object
              examples:
                example:
                  summary: The new name of the file and target for duplicating it.
                  value: {
                    "template": {
                      "data": [
                      {
                        "name": "display_name",
                        "value": "TheNewNameOfTheFile"
                      },
                      {
                        "name": "target",
                        "value": "http://localhost:8080/volumes/666f6f2d6261722d71757578/buckets/my-bucket"
                      }]
                    }
                  }
            application/json:
              schema:
                type: object
              examples:
                example:
                  summary: The new name of the file and target for moving it.
                  value: {
                    "display_name": "TheNewNameOfTheFile",
                    "target": "http://localhost:8080/volumes/666f6f2d6261722d71757578/buckets/my-bucket"
                  }
    responses:
      '201':
        $ref: '#/components/responses/201'
      '400':
        $ref: '#/components/responses/400'
      '404':
        $ref: '#/components/responses/404'
    """
    return await _duplicate_object(request)


@routes.get('/volumes/{volume_id}/buckets/{bucket_id}/awss3files/{id}/mover')
@action(name='heaserver-awss3files-file-move-form')
async def get_file_mover(request: web.Request) -> web.Response:
    """
    Gets a form template for moving the requested file.

    :param request: the HTTP request. Required.
    :return: the requested form, or Not Found if the requested file was not found.
    """
    logger = logging.getLogger(__name__)
    id_ = request.match_info['id']
    try:
        id = encode_key(split(decode_key(id_))[0])
        add_run_time_action(request, name='heaserver-awss3files-file-get-target', rel='headata-target', path=(
                '/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/' + id) if id else '/volumes/{volume_id}/buckets/{bucket_id}')
        return await awsservicelib.get_file(request)
    except KeyDecodeException as e:
        logger.exception('Error getting parent key')
        return response.status_bad_request(f'Error getting parent folder: {e}')


@routes.put('/volumes/{volume_id}/buckets/{bucket_id}/awss3files/{id}/content')
async def put_file_content(request: web.Request) -> web.Response:
    """
    Updates the content of the requested file.
    :param request: the HTTP request. Required.
    :return: a Response object with the value No Content or Not Found.
    ---
    summary: File content
    tags:
        - heaserver-files-aws-s3
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the volume to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
        - name: bucket_id
          in: path
          required: true
          description: The id of the bucket to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A bucket id
              value: my-bucket
        - $ref: '#/components/parameters/id'
    requestBody:
        description: File contents.
        required: true
        content:
            application/octet-stream:
                schema:
                    type: string
                    format: binary
    responses:
      '204':
        $ref: '#/components/responses/204'
      '404':
        $ref: '#/components/responses/404'
    """
    return await awsservicelib.put_object_content(request)


@routes.get('/volumes/{volume_id}/buckets/{bucket_id}/awss3files/{id}/content')
async def get_file_content(request: web.Request) -> web.StreamResponse:
    """
    :param request:
    :return:
    ---
    summary: File content
    tags:
        - heaserver-files-aws-s3
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the volume to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
        - name: bucket_id
          in: path
          required: true
          description: The id of the bucket to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A bucket id
              value: my-bucket
        - $ref: '#/components/parameters/id'
    responses:
      '200':
        $ref: '#/components/responses/200'
      '403':
        $ref: '#/components/responses/403'
      '404':
        $ref: '#/components/responses/404'
    """
    return await awsservicelib.get_object_content(request)


@routes.get('/volumes/{volume_id}/buckets/{bucket_id}/awss3files/{id}')
@action('heaserver-awss3files-file-get-open-choices', rel='hea-opener-choices hea-context-menu',
        path='/volumes/{volume_id}/buckets/{bucket_id}/awss3files/{id}/opener')
@action(name='heaserver-awss3files-file-get-properties', rel='hea-properties hea-context-menu')
@action(name='heaserver-awss3files-file-duplicate', rel='hea-duplicator hea-context-menu',
        path='/volumes/{volume_id}/buckets/{bucket_id}/awss3files/{id}/duplicator')
@action(name='heaserver-awss3files-file-move', rel='hea-mover hea-context-menu',
        path='/volumes/{volume_id}/buckets/{bucket_id}/awss3files/{id}/mover')
@action('heaserver-awss3files-file-get-self', rel='self', path='/volumes/{volume_id}/buckets/{bucket_id}/awss3files/{id}')
@action(name='heaserver-awss3files-file-get-volume', rel='hea-volume', path='/volumes/{volume_id}')
@action(name='heaserver-awss3files-file-get-awsaccount', rel='hea-account', path='/volumes/{volume_id}/awsaccounts/me')
async def get_file(request: web.Request) -> web.Response:
    """
    Gets the file with the specified id.

    :param request: the HTTP request.
    :return: the requested file or Not Found.
    ---
    summary: A specific file.
    tags:
        - heaserver-files-aws-s3
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the volume to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
        - name: bucket_id
          in: path
          required: true
          description: The id of the bucket to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A bucket id
              value: my-bucket
        - $ref: '#/components/parameters/id'
    responses:
      '200':
        $ref: '#/components/responses/200'
      '404':
        $ref: '#/components/responses/404'
    """
    return await awsservicelib.get_file(request)


@routes.get('/volumes/{volume_id}/buckets/{bucket_id}/awss3files/byname/{name}')
@action('heaserver-awss3files-file-get-self', rel='self', path='/volumes/{volume_id}/buckets/{bucket_id}/awss3files/{id}')
@action(name='heaserver-awss3files-file-get-volume', rel='hea-volume', path='/volumes/{volume_id}')
@action(name='heaserver-awss3files-file-get-awsaccount', rel='hea-account', path='/volumes/{volume_id}/awsaccounts/me')
async def get_file_by_name(request: web.Request) -> web.Response:
    """
    Gets the file with the specified name.

    :param request: the HTTP request.
    :return: the requested file or Not Found.
    ---
    summary: A specific file.
    tags:
        - heaserver-files-aws-s3
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the volume to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
        - name: bucket_id
          in: path
          required: true
          description: The id of the bucket to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A bucket id
              value: my-bucket
        - $ref: '#/components/parameters/name'
    responses:
      '200':
        $ref: '#/components/responses/200'
      '404':
        $ref: '#/components/responses/404'
    """
    return await awsservicelib.get_file_by_name(request)


@routes.get('/volumes/{volume_id}/buckets/{bucket_id}/awss3files')
@routes.get('/volumes/{volume_id}/buckets/{bucket_id}/awss3files/')
@action('heaserver-awss3files-file-get-open-choices', rel='hea-opener-choices hea-context-menu',
        path='/volumes/{volume_id}/buckets/{bucket_id}/awss3files/{id}/opener')
@action(name='heaserver-awss3files-file-get-properties', rel='hea-properties hea-context-menu')
@action(name='heaserver-awss3files-file-duplicate', rel='hea-duplicator hea-context-menu', path='/volumes/{volume_id}/buckets/{bucket_id}/awss3files/{id}/duplicator')
@action(name='heaserver-awss3files-file-move', rel='hea-mover hea-context-menu', path='/volumes/{volume_id}/buckets/{bucket_id}/awss3files/{id}/mover')
@action('heaserver-awss3files-file-get-self', rel='self', path='/volumes/{volume_id}/buckets/{bucket_id}/awss3files/{id}')
async def get_files(request: web.Request) -> web.Response:
    """
    Gets the file with the specified id.

    :param request: the HTTP request.
    :return: the requested file or Not Found.
    ---
    summary: A specific file.
    tags:
        - heaserver-files-aws-s3
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the volume to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
        - name: bucket_id
          in: path
          required: true
          description: The id of the bucket to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A bucket id
              value: my-bucket
    responses:
      '200':
        $ref: '#/components/responses/200'
      '404':
        $ref: '#/components/responses/404'
    """
    return await awsservicelib.get_all_files(request)


@routes.route('OPTIONS', '/volumes/{volume_id}/buckets/{bucket_id}/awss3files')
@routes.route('OPTIONS', '/volumes/{volume_id}/buckets/{bucket_id}/awss3files/')
async def get_files_options(request: web.Request) -> web.Response:
    """
    Gets the allowed HTTP methods for a files resource.

    :param request: the HTTP request (required).
    :response: the HTTP response.
    ---
    summary: Allowed HTTP methods.
    tags:
        - heaserver-files-aws-s3
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the volume to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
        - name: bucket_id
          in: path
          required: true
          description: The id of the bucket to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A bucket id
              value: my-bucket
    responses:
      '200':
        description: Expected response to a valid request.
        content:
            text/plain:
                schema:
                    type: string
                    example: "200: OK"
      '403':
        $ref: '#/components/responses/403'
      '404':
        $ref: '#/components/responses/404'
    """
    return await database.get_options(request, ['GET', 'DELETE', 'HEAD', 'OPTIONS'], awsservicelib.has_bucket)


@routes.delete('/volumes/{volume_id}/buckets/{bucket_id}/awss3files/{id}')
async def delete_file(request: web.Request) -> web.Response:
    """
    Deletes the file with the specified id.

    :param request: the HTTP request.
    :return: No Content or Not Found.
    ---
    summary: File deletion
    tags:
        - heaserver-files-aws-s3
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the volume to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
        - name: bucket_id
          in: path
          required: true
          description: The id of the bucket to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A bucket id
              value: my-bucket
        - $ref: '#/components/parameters/id'
    responses:
      '204':
        $ref: '#/components/responses/204'
      '404':
        $ref: '#/components/responses/404'
    """
    return await awsservicelib.delete_file(request)


@routes.get('/volumes/{volume_id}/buckets/{bucket_id}/awss3files/{id}/opener')
@action('heaserver-awss3files-file-open-default', rel='hea-opener hea-default',
        path='/volumes/{volume_id}/buckets/{bucket_id}/awss3files/{id}/content')
@action('heaserver-awss3files-file-open-url', rel=f'hea-opener hea-context-aws {AWSS3FileObject.DEFAULT_MIME_TYPE}',
        path='/volumes/{volume_id}/buckets/{bucket_id}/awss3files/{id}/presigned-url')
async def get_file_opener(request: web.Request) -> web.Response:
    """
    Opens the requested file.

    :param request: the HTTP request. Required.
    :return: the opened file, or Not Found if the requested file does not exist.
    ---
    summary: File opener choices
    tags:
        - heaserver-files-aws-s3
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the volume to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
        - name: bucket_id
          in: path
          required: true
          description: The id of the bucket to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A bucket id
              value: my-bucket
        - $ref: '#/components/parameters/id'
    responses:
      '300':
        $ref: '#/components/responses/300'
      '404':
        $ref: '#/components/responses/404'
    """
    return await awsservicelib.get_file(request)


@routes.get('/volumes/{volume_id}/buckets/{bucket_id}/awss3files/{id}/presigned-url')
async def generate_presigned_url(request: web.Request) -> web.Response:
    """
    Generates a  with the specified id.

    :param request: the HTTP request.
    :return: No Content or Not Found.
    ---
    summary: Presigned url for file
    tags:
        - heaserver-files-aws-s3
    parameters:
        - name: volume_id
          in: path
          required: true
          description: The id of the volume to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A volume id
              value: 666f6f2d6261722d71757578
        - name: expiration
          in: query
          required: false
          description: Expiration time of presigned objects url in seconds
          schema:
            type: number
          examples:
            example:
              summary: Expiration time
              value: 259200
        - name: bucket_id
          in: path
          required: true
          description: The id of the bucket to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A bucket id
              value: my-bucket
        - $ref: '#/components/parameters/id'
    responses:
      '204':
        $ref: '#/components/responses/204'
      '404':
        $ref: '#/components/responses/404'
    """
    return await awsservicelib.generate_presigned_url(request)


def main():
    for mime_type, extensions in MIME_TYPES.items():
        for extension in extensions if isinstance(extensions, list) else [extensions]:
            mimetypes.add_type(mime_type, extension)
    config = init_cmd_line(description='Repository of files in AWS S3 buckets', default_port=8080)
    start(db=S3Manager, wstl_builder_factory=builder_factory(__package__), config=config)


async def _duplicate_object(request: web.Request) -> web.Response:
    return await awsservicelib.copy_object(request)


async def _move_object(request: web.Request) -> web.Response:
    copy_response = await _duplicate_object(request)
    match copy_response.status:
        case 201:
            return await awsservicelib.delete_object(request, recursive=True)
        case _:
            return response.status_generic(copy_response.status)
