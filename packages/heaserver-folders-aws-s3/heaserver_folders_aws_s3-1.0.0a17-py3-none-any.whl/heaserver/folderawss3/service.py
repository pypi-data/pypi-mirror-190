from heaserver.service.runner import init_cmd_line, routes, start
from heaserver.service.db import awsservicelib, aws
from heaserver.service.db.database import get_options
from heaserver.service.wstl import builder_factory, action, add_run_time_action
from heaserver.service import response
from heaserver.service.heaobjectsupport import new_heaobject_from_type
from heaserver.service.messagebroker import publisher_cleanup_context_factory, publish_desktop_object
from heaserver.service.oidcclaimhdrs import SUB
from heaserver.service.db.awss3bucketobjectkey import KeyDecodeException, decode_key, split, encode_key, join
from heaobject.folder import AWSS3Item, AWSS3Folder
from heaobject.data import AWSS3FileObject
from heaobject.activity import AWSActivity, Status
from heaobject.error import DeserializeException
from aiohttp import web, hdrs
from typing import Union, Callable
from multidict import istr
import logging

_logger = logging.getLogger(__name__)


@routes.get('/ping')
async def ping(request: web.Request) -> web.Response:
    """
    For testing whether the service is up.

    :param request: the HTTP request.
    :return: Always returns status code 200.
    """
    return response.status_ok()


@routes.get('/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{folder_id}/items')
@routes.get('/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{folder_id}/items/')
@action(name='heaserver-awss3folders-item-get-actual', rel='hea-actual', path='{+actual_object_uri}')
async def get_items(request: web.Request) -> web.Response:
    """
    Gets the items of the folder with the specified id.
    :param request: the HTTP request.
    :return: the requested items, or Not Found if the folder was not found.
    ---
    summary: All items in a folder.
    tags:
        - heaserver-folders-folder-items
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
        - name: folder_id
          in: path
          required: true
          description: The id of the folder to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A folder id
              value: root
    responses:
      '200':
        $ref: '#/components/responses/200'
      '403':
        $ref: '#/components/responses/403'
    """
    return await awsservicelib.get_items(request)


@routes.route('OPTIONS', '/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{folder_id}/items/{id}')
async def get_item_options(request: web.Request) -> web.Response:
    """
    ---
    summary: Allowed HTTP methods.
    tags:
        - heaserver-folders-folder-items
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
        - name: folder_id
          in: path
          required: true
          description: The id of the folder to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A folder id
              value: root
        - $ref: '#/components/parameters/id'
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
    resp = await awsservicelib.has_item(request)
    if resp.status == 200:
        return await response.get_options(request, ['GET', 'POST', 'DELETE', 'HEAD', 'OPTIONS'])
    else:
        headers: dict[Union[str, istr], str] = {}
        headers[hdrs.CONTENT_TYPE] = 'text/plain; charset=utf-8'
        return response.status_generic(status=resp.status, body=resp.text, headers=headers)


@routes.route('OPTIONS', '/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{folder_id}/items')
@routes.route('OPTIONS', '/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{folder_id}/items/')
async def get_items_options(request: web.Request) -> web.Response:
    """
    Gets the allowed HTTP methods for a folder items resource.

    :param request: the HTTP request (required).
    :return: the HTTP response.
    ---
    summary: Allowed HTTP methods.
    tags:
        - heaserver-folders-folder-items
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
        - name: folder_id
          in: path
          required: true
          description: The id of the folder to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A folder id
              value: root
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
    resp = await awsservicelib.has_folder(request)
    if resp.status == 200:
        return await response.get_options(request, ['GET', 'POST', 'DELETE', 'HEAD', 'OPTIONS'])
    else:
        headers: dict[Union[str, istr], str] = {hdrs.CONTENT_TYPE: 'text/plain; charset=utf-8'}
        return response.status_generic(status=resp.status, body=resp.text, headers=headers)


@routes.route('OPTIONS', '/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{id}')
async def get_folder_options(request: web.Request) -> web.Response:
    """
    Gets the allowed HTTP methods for a folder resource.

    :param request: the HTTP request (required).
    :return: the HTTP response.
    ---
    summary: Allowed HTTP methods.
    tags:
        - heaserver-folders-folders
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
    resp = await awsservicelib.has_folder(request)
    if resp.status == 200:
        return await response.get_options(request, ['GET', 'POST', 'DELETE', 'HEAD', 'OPTIONS'])
    else:
        headers: dict[Union[str, istr], str] = {hdrs.CONTENT_TYPE: 'text/plain; charset=utf-8'}
        return response.status_generic(status=resp.status, body=resp.text, headers=headers)


@routes.get('/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{folder_id}/items/{id}')
@action(name='heaserver-awss3folders-item-get-actual', rel='hea-actual',
        path='{+actual_object_uri}')  # Maybe have a different syntax when we do not want to encode.
@action(name='heaserver-awss3folders-item-get-volume', rel='hea-volume', path='/volumes/{volume_id}')
async def get_item(request: web.Request) -> web.Response:
    """
    Gets the requested item from the given folder.

    :param request: the HTTP request. Required.
    :return: the requested item, or Not Found if it was not found.
    ---
    summary: A specific folder item.
    tags:
        - heaserver-folders-folder-items
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
        - name: folder_id
          in: path
          required: true
          description: The id of the folder to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A folder id
              value: root
        - $ref: '#/components/parameters/id'
    responses:
      '200':
        $ref: '#/components/responses/200'
      '403':
        $ref: '#/components/responses/403'
      '404':
        $ref: '#/components/responses/404'
    """
    return await _get_item_response(request)


@routes.get('/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{id}/duplicator')
@action(name='heaserver-awss3folders-folder-duplicate-form')
async def get_folder_duplicator(request: web.Request) -> web.Response:
    """
    Gets a form template for duplicating the requested folder.

    :param request: the HTTP request. Required.
    :return: the requested form, or Not Found if the requested folder was not found.
    ---
    summary: A folder to duplicate.
    tags:
        - heaserver-folders-folders
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
    logger = logging.getLogger(__name__)
    id_ = request.match_info['id']
    try:
        id = encode_key(split(decode_key(id_))[0])
        add_run_time_action(request, name='heaserver-awss3folders-folder-get-target', rel='headata-target', path=('/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/' + id) if id else '/volumes/{volume_id}/buckets/{bucket_id}')
        return await _get_folder(request)
    except KeyDecodeException as e:
        logger.exception('Error getting parent key')
        return response.status_bad_request(f'Error getting parent folder: {e}')


@routes.get('/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{id}/mover')
@action(name='heaserver-awss3folders-folder-move-form')
async def get_folder_mover(request: web.Request) -> web.Response:
    """
    Gets a form template for moving the requested folder.

    :param request: the HTTP request. Required.
    :return: the requested form, or Not Found if the requested folder was not found.
    ---
    summary: A folder to move.
    tags:
        - heaserver-folders-folders
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
    logger = logging.getLogger(__name__)
    id_ = request.match_info['id']
    try:
        id = encode_key(split(decode_key(id_))[0])
        add_run_time_action(request, name='heaserver-awss3folders-folder-get-target', rel='headata-target', path=('/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/' + id) if id else '/volumes/{volume_id}/buckets/{bucket_id}')
        return await _get_folder(request)
    except KeyDecodeException as e:
        logger.exception('Error getting parent key')
        return response.status_bad_request(f'Error getting parent folder: {e}')


@routes.post('/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{id}/mover')
async def post_folder_mover(request: web.Request) -> web.Response:
    """
    Posts the provided folder to move it.

    :param request: the HTTP request.
    :return: a Response object with a status of No Content.
    ---
    summary: A specific folder.
    tags:
        - heaserver-folders-folders
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
        description: The new name of the folder and target for moving it.
        required: true
        content:
            application/vnd.collection+json:
              schema:
                type: object
              examples:
                example:
                  summary: The new name of the folder and target for moving it.
                  value: {
                    "template": {
                      "data": [
                      {
                        "name": "display_name",
                        "value": "TheNewNameOfTheFolder"
                      },
                      {
                        "name": "target",
                        "value": "http://localhost:8080/volumes/666f6f2d6261722d71757578/buckets/my-bucket/awss3folders/"
                      }]
                    }
                  }
            application/json:
              schema:
                type: object
              examples:
                example:
                  summary: The new name of the folder and target for moving it.
                  value: {
                    "display_name": "TheNewNameOfTheFolder",
                    "target": "http://localhost:8080/volumes/666f6f2d6261722d71757578/buckets/my-bucket/awss3folders/"
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


@routes.post('/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{id}/duplicator')
async def post_folder_duplicator(request: web.Request) -> web.Response:
    """
    Posts the provided item for duplication.

    :param request: the HTTP request.
    :return: a Response object with a status of Created and the object's URI in the
    ---
    summary: A specific folder item.
    tags:
        - heaserver-folders-folders
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
        description: The new name of the folder and target for duplicating it.
        required: true
        content:
            application/vnd.collection+json:
              schema:
                type: object
              examples:
                example:
                  summary: The new name of the folder and target for duplicating it.
                  value: {
                    "template": {
                      "data": [
                      {
                        "name": "display_name",
                        "value": "TheNewNameOfTheFolder"
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
                  summary: The new name of the folder and target for moving it.
                  value: {
                    "display_name": "TheNewNameOfTheFolder",
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


@routes.post('/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{folder_id}/items')
@routes.post('/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{folder_id}/items/')
async def post_item_in_folder(request: web.Request) -> web.Response:
    """
    Creates a new folder item.

    :param request: the HTTP request. The body of the request is expected to be an item or an actual object.
    :return: the response, with a 204 status code if an item was created or a 400 if not. If an item was created, the
    Location header will contain the URL of the created item.
    ---
    summary: A specific folder item.
    tags:
        - heaserver-folders-folder-items
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
        - name: folder_id
          in: path
          required: true
          description: The id of the folder.
          schema:
            type: string
          examples:
            example:
              summary: A folder id
              value: root
    requestBody:
        description: A new folder item object.
        required: true
        content:
            application/vnd.collection+json:
              schema:
                type: object
              examples:
                example:
                  summary: Item example
                  value: {
                    "template": {
                      "data": [{
                        "name": "created",
                        "value": null
                      },
                      {
                        "name": "derived_by",
                        "value": null
                      },
                      {
                        "name": "derived_from",
                        "value": []
                      },
                      {
                        "name": "description",
                        "value": null
                      },
                      {
                        "name": "display_name",
                        "value": "Bob"
                      },
                      {
                        "name": "invited",
                        "value": []
                      },
                      {
                        "name": "modified",
                        "value": null
                      },
                      {
                        "name": "name",
                        "value": "bob"
                      },
                      {
                        "name": "owner",
                        "value": "system|none"
                      },
                      {
                        "name": "shares",
                        "value": []
                      },
                      {
                        "name": "source",
                        "value": null
                      },
                      {
                        "name": "version",
                        "value": null
                      },
                      {
                        "name": "actual_object_id",
                        "value": "666f6f2d6261722d71757578"
                      },
                      {
                        "name": "actual_object_type_name",
                        "value": "heaobject.data.AWSS3FileObject"
                      },
                      {
                        "name": "actual_object_uri",
                        "value": "/volumes/666f6f2d6261722d71757578/buckets/my-bucket/folders/666f6f2d6261722d71757578"
                      },
                      {
                        "name": "type",
                        "value": "heaobject.folder.AWSS3Item"
                      }]
                    }
                  }
            application/json:
              schema:
                type: object
              examples:
                example:
                  summary: Item example
                  value: {
                    "created": null,
                    "derived_by": null,
                    "derived_from": [],
                    "description": null,
                    "display_name": "Joe",
                    "invited": [],
                    "modified": null,
                    "name": "joe",
                    "owner": "system|none",
                    "shares": [],
                    "source": null,
                    "type": "heaobject.folder.AWSS3Item",
                    "version": null,
                    "folder_id": "root",
                    "actual_object_id": "666f6f2d6261722d71757578",
                    "actual_object_type_name": "heaobject.registry.Component",
                    "actual_object_uri": "/volumes/666f6f2d6261722d71757578/buckets/my-bucket/folders/666f6f2d6261722d71757578"
                  }
    responses:
      '201':
        $ref: '#/components/responses/201'
      '400':
        $ref: '#/components/responses/400'
      '404':
        $ref: '#/components/responses/404'
    """
    return await _post_item_in_folder(request)


@routes.delete('/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{folder_id}/items/{id}')
async def delete_item(request: web.Request) -> web.Response:
    """
    Deletes the item with the specified id.

    :param request: the HTTP request.
    :return: No Content or Not Found.
    ---
    summary: Folder item deletion
    tags:
        - heaserver-folders-folder-items
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
        - name: folder_id
          in: path
          required: true
          description: The id of the folder.
          schema:
            type: string
          examples:
            example:
              summary: A folder id
              value: root
        - $ref: '#/components/parameters/id'
    responses:
      '204':
        $ref: '#/components/responses/204'
      '404':
        $ref: '#/components/responses/404'
    """
    return await awsservicelib.delete_object(request, recursive=True, activity_cb=publish_desktop_object)


@routes.get('/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{id}')
@action(name='heaserver-awss3folders-folder-get-open-choices', rel='hea-opener-choices hea-context-menu',
        path='/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{id}/opener')
@action(name='heaserver-awss3folders-folder-get-properties', rel='hea-properties hea-context-menu')
@action(name='heaserver-awss3folders-folder-duplicate', rel='hea-duplicator hea-context-menu',
        path='/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{id}/duplicator')
@action(name='heaserver-awss3folders-folder-move', rel='hea-mover hea-context-menu',
        path='/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{id}/mover')
@action(name='heaserver-awss3folders-folder-get-create-choices', rel='hea-creator-choices hea-context-menu',
        path='/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{id}/creator')
@action(name='heaserver-awss3folders-folder-get-self', rel='self', path='/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{id}')
@action(name='heaserver-awss3folders-folder-get-volume', rel='hea-volume', path='/volumes/{volume_id}')
@action(name='heaserver-awss3folders-folder-get-awsaccount', rel='hea-account', path='/volumes/{volume_id}/awsaccounts/me')
async def get_folder(request: web.Request) -> web.Response:
    """
    Gets the folder with the specified id.

    :param request: the HTTP request.
    :return: the requested folder or Not Found.
    ---
    summary: A specific folder.
    tags:
        - heaserver-folders-folders
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
    return await _get_folder(request)


@routes.get('/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/byname/{name}')
@action(name='heaserver-awss3folders-folder-get-self', rel='self', path='/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{id}')
@action(name='heaserver-awss3folders-folder-get-volume', rel='hea-volume', path='/volumes/{volume_id}')
@action(name='heaserver-awss3folders-folder-get-awsaccount', rel='hea-account', path='/volumes/{volume_id}/awsaccounts/me')
async def get_folder_by_name(request: web.Request) -> web.Response:
    """
    Gets the folder with the specified name.

    :param request: the HTTP request.
    :return: the requested folder or Not Found.
    ---
    summary: A specific folder.
    tags:
        - heaserver-folders-folders
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
    return await _get_folder_by_name(request)


@routes.get('/volumes/{volume_id}/buckets/{bucket_id}/awss3folders')
@routes.get('/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/')
@action('heaserver-awss3folders-folder-get-open-choices', rel='hea-opener-choices hea-context-menu',
        path='/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{id}/opener')
@action(name='heaserver-awss3folders-folder-get-properties', rel='hea-properties hea-context-menu')
@action(name='heaserver-awss3folders-folder-duplicate', rel='hea-duplicator hea-context-menu',
        path='/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{id}/duplicator')
@action(name='heaserver-awss3folders-folder-move', rel='hea-mover hea-context-menu',
        path='/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{id}/mover')
@action(name='heaserver-awss3folders-folder-get-create-choices', rel='hea-creator-choices hea-context-menu',
        path='/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{id}/creator')
@action(name='heaserver-awss3folders-folder-get-self', rel='self', path='/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{id}')
async def get_folders(request: web.Request) -> web.Response:
    """
    Gets all folders in the bucket.

    :param request: the HTTP request.
    :return: the requested folder or Not Found.
    ---
    summary: All folders.
    tags:
        - heaserver-folders-folders
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
    return await awsservicelib.get_all_folders(request)

@routes.route('OPTIONS', '/volumes/{volume_id}/buckets/{bucket_id}/awss3folders')
@routes.route('OPTIONS', '/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/')
async def get_folders_options(request: web.Request) -> web.Response:
    """
    Gets the allowed HTTP methods for a folders resource.

    :param request: the HTTP request (required).
    :response: the HTTP response.
    ---
    summary: Allowed HTTP methods.
    tags:
        - heaserver-folders-folders
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
    return await get_options(request, ['GET', 'DELETE', 'HEAD', 'OPTIONS'], awsservicelib.has_bucket)


@routes.delete('/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{id}')
async def delete_folder(request: web.Request) -> web.Response:
    """
    Deletes the folder with the specified id.

    :param request: the HTTP request.
    :return: No Content or Not Found.
    ---
    summary: Folder deletion
    tags:
        - heaserver-folders-folders
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
    return await awsservicelib.delete_folder(request)


@routes.post('/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{id}/newfolder')
@routes.post('/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{id}/newfolder/')
async def post_new_folder(request: web.Request) -> web.Response:
    """
    Gets form for creating a new folder within this one.

    :param request: the HTTP request. Required.
    :return: the current folder, with a template for creating a child folder or Not Found if the requested item does not
    exist.
    ---
    summary: A folder.
    tags:
        - heaserver-folders-folders
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
        description: A new folder.
        required: true
        content:
            application/vnd.collection+json:
              schema:
                type: object
              examples:
                example:
                  summary: Folder example
                  value: {
                    "template": {
                      "data": [
                      {
                        "name": "display_name",
                        "value": "Bob"
                      },
                      {
                        "name": "type",
                        "value": "heaobject.folder.AWSS3Folder"
                      }]
                    }
                  }
            application/json:
              schema:
                type: object
              examples:
                example:
                  summary: Item example
                  value: {
                    "display_name": "Joe",
                    "type": "heaobject.folder.AWSS3Folder"
                  }
    responses:
      '201':
        $ref: '#/components/responses/201'
      '400':
        $ref: '#/components/responses/400'
      '404':
        $ref: '#/components/responses/404'
    """
    return await awsservicelib.post_folder(request)


@routes.get('/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{id}/newfolder')
@routes.get('/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{id}/newfolder/')
@action('heaserver-awss3folders-folder-new-form')
async def get_new_folder_form(request: web.Request) -> web.Response:
    """
    Gets form for creating a new folder within this one.

    :param request: the HTTP request. Required.
    :return: the current folder, with a template for creating a child folder or Not Found if the requested item does not
    exist.
    ---
    summary: A folder.
    tags:
        - heaserver-folders-folders
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
    responses:
      '200':
        $ref: '#/components/responses/200'
      '404':
        $ref: '#/components/responses/404'
    """
    return await awsservicelib.get_folder(request)

@routes.get('/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{id}/creator')
@action('heaserver-awss3folders-folder-create-folder', rel='hea-creator hea-default application/x.folder',
        path='/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{id}/newfolder')
async def get_folder_creator(request: web.Request) -> web.Response:
    """
    Opens the requested folder.

    :param request: the HTTP request. Required.
    :return: the opened folder, or Not Found if the requested item does not exist.
    ---
    summary: Folder creator choices
    tags:
        - heaserver-folders-folders
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
    responses:
      '300':
        $ref: '#/components/responses/300'
      '404':
        $ref: '#/components/responses/404'
    """
    return await awsservicelib.get_folder_opener(request)

@routes.get('/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{id}/opener')
@action('heaserver-awss3folders-folder-open-default', rel='hea-opener hea-default application/x.folder',
        path='/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{id}/items/')
async def get_folder_opener(request: web.Request) -> web.Response:
    """
    Opens the requested folder.

    :param request: the HTTP request. Required.
    :return: the opened folder, or Not Found if the requested item does not exist.
    ---
    summary: Folder opener choices
    tags:
        - heaserver-folders-folders
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
    return await awsservicelib.get_folder_opener(request)


def main():
    config = init_cmd_line(description='Repository of folders', default_port=8080)
    start(db=aws.S3Manager, wstl_builder_factory=builder_factory(__package__),
          cleanup_ctx=[publisher_cleanup_context_factory(config)],
          config=config)


async def _get_folder(request: web.Request) -> web.Response:
    """
    Gets the folder with the specified id.

    :param request: the HTTP request.
    :return: the requested folder or Not Found.
    """
    return await awsservicelib.get_folder(request)


async def _get_folder_by_name(request: web.Request) -> web.Response:
    """
    Gets the folder with the specified id.

    :param request: the HTTP request.
    :return: the requested folder or Not Found.
    """
    return await awsservicelib.get_folder_by_name(request)


async def _get_item_response(request) -> web.Response:
    """
    Gets the item with the specified id and in the specified folder.

    :param request: the HTTP request.
    :return: a response containing the returned item or an empty body.
    """
    return await awsservicelib.get_item(request)


async def _duplicate_object(request: web.Request) -> web.Response:
    return await awsservicelib.copy_object(request)


async def _move_object(request: web.Request) -> web.Response:
    copy_response = await _duplicate_object(request)
    match copy_response.status:
        case 201:
            return await awsservicelib.delete_object(request, recursive=True)
        case _:
            return response.status_generic(copy_response.status)


async def _post_item_in_folder(request: web.Request) -> web.Response:
    try:
        item = await new_heaobject_from_type(request, AWSS3Item)
    except DeserializeException as e:
        return response.status_bad_request(str(e).encode())
    return await awsservicelib.post_object(request, item)
