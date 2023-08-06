"""
Utility classes and functions for working with AWS.
"""
from enum import auto

from heaobject import root
from typing import Optional
from .awss3bucketobjectkey import KeyDecodeException, encode_key, decode_key, is_folder
import re



class S3StorageClass(root.EnumAutoName):
    """
    The S3 storage classes. The list of storage classes is documented at
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.list_objects_v2, and
    each storage class is explained in detail at
    https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-class-intro.html.
    """
    STANDARD = auto()  # S3 Standard
    REDUCED_REDUNDANCY = auto()  # Reduced Redundancy (RRS)
    GLACIER = auto()  # S3 Glacier Flexible Retrieval
    STANDARD_IA = auto()  # S3 Standard-IR (infrequent access)
    ONEZONE_IA = auto()  # S3 One Zone-IR
    INTELLIGENT_TIERING = auto()  # S3 Intelligent-Tiering
    DEEP_ARCHIVE = auto()  # S3 Glacier Deep Archive
    OUTPOSTS = auto()  # S3 Outposts
    GLACIER_IR = auto()  # S3 Glacier Instant Retrieval
    OTHER = auto()


class S3URIMixin:
    """
    Mixing for adding a S3 URI to a desktop object.
    """

    @property
    def bucket_id(self) -> Optional[str]:
        """
        The object's bucket name.
        """
        try:
            return self.__bucket_id
        except AttributeError:
            self.__bucket_id: str | None = None
            return self.__bucket_id

    @bucket_id.setter
    def bucket_id(self, bucket_id: Optional[str]):
        self.__bucket_id = bucket_id

    @property
    def id(self) -> Optional[str]:
        return self.bucket_id

    @id.setter
    def id(self, id: Optional[str]):
        self.bucket_id = id

    @property
    def name(self) -> Optional[str]:
        return self.bucket_id

    @name.setter
    def name(self, name: Optional[str]):
        self.bucket_id = name

    @property
    def display_name(self) -> str:
        return self.bucket_id

    @display_name.setter
    def display_name(self, display_name: str):
        self.bucket_id = display_name

    @property
    def s3_uri(self) -> Optional[str]:
        """
        The object's S3 URI, computed from the bucket id field or set with this property.
        """
        return s3_uri(self.bucket_id)

    @s3_uri.setter
    def s3_uri(self, s3_uri: Optional[str]):
        if s3_uri is not None and not s3_uri.startswith('s3://'):
            raise ValueError(f'Invalid S3 bucket URI {s3_uri}')
        match = _s3_uri_bucket_pattern.fullmatch(s3_uri) if s3_uri else None
        if match:
            bucket_and_key = match.groupdict()
            self.bucket_id = bucket_and_key['bucket']
        elif s3_uri is not None:
            raise ValueError(f'Invalid s3 bucket URI {s3_uri}')
        else:
            self.bucket_id = None

    @property
    def presigned_url(self) -> Optional[str]:
        """
        The object's presigned url.
        """
        try:
            return self.__presigned_url
        except AttributeError:
            return None

    @presigned_url.setter
    def presigned_url(self, presigned_url: Optional[str]):
        presigned_url_ = str(presigned_url) if presigned_url is not None else None
        if presigned_url_ is not None and not presigned_url_.startswith('https://'):
            raise ValueError(f'Invalid presigned URL {presigned_url_}')
        self.__presigned_url = presigned_url_


class S3URIWithKeyMixin(S3URIMixin):
    @property
    def id(self) -> Optional[str]:
        s3_uri_ = self.s3_uri
        return encode_key(s3_uri_) if s3_uri_ else None

    @id.setter
    def id(self, id: Optional[str]):
        try:
            self.s3_uri = decode_key(id) if id is not None else None
        except KeyDecodeException as e:
            raise ValueError(f'Invalid id {id}') from e

    @property
    def name(self) -> Optional[str]:
        s3_uri_ = self.s3_uri
        return encode_key(s3_uri_) if s3_uri_ else None

    @name.setter
    def name(self, name: Optional[str]):
        try:
            self.s3_uri = decode_key(name) if name is not None else None
        except KeyDecodeException as e:
            raise ValueError(f'Invalid name {name}') from e

    @property
    def key(self) -> Optional[str]:
        """
        The object's key.
        """
        try:
            return self.__key
        except AttributeError:
            self.__key: str | None = None
            return self.__key

    @key.setter
    def key(self, key: Optional[str]):
        if key:
            self.__key = key
            if self.__key is not None and is_folder(self.__key):
                key_: str | None = self.__key.strip('/')
            else:
                key_ = self.__key
            if key_ is not None:
                self.__display_name: str | None = key_.rsplit('/', maxsplit=1)[-1]
            else:
                self.__display_name = None
        else:
            self.__display_name = None

    @property
    def display_name(self) -> str:
        """
        The object's display name. It's the last part of the object's key, minus any trailing slash for folders.
        Assumes the object is a file.
        """
        try:
            result = self.__display_name
        except AttributeError:
            self.__display_name = None
            result = self.__display_name
        return result if result is not None else super().display_name  # type: ignore

    @display_name.setter
    def display_name(self, display_name: str):
        if display_name is not None:
            try:
                key = self.__key
                if key is not None and len(key) > 1:
                    key_rsplit = key.rsplit('/', 1)
                    if len(key_rsplit) > 1:
                        key = key_rsplit[-2] + f'/{display_name}' if len(key_rsplit) > 1 else display_name
                    else:
                        key = f'{display_name}'
                else:
                    key = f'{display_name}'
                self.key = key
            except AttributeError:
                pass

    @property
    def s3_uri(self) -> Optional[str]:
        """
        The object's S3 URI, computed from the bucket id and the id field.
        """
        return s3_uri(self.bucket_id, self.key)

    @s3_uri.setter
    def s3_uri(self, s3_uri: Optional[str]):
        """
        The object's S3 URI, computed from the bucket id and the id field.
        """
        if s3_uri is not None and not s3_uri.startswith('s3://'):
            raise ValueError(f'Invalid s3 URI {s3_uri}')
        match = S3_URI_PATTERN.fullmatch(s3_uri) if s3_uri else None
        if match:
            bucket_and_key = match.groupdict()
            self.bucket_id = bucket_and_key['bucket']
            self.key = bucket_and_key['key']
        elif s3_uri is not None:
            raise ValueError(f'Invalid s3 URI {s3_uri}')
        else:
            self.bucket_id = None
            self.key = None


def s3_uri(bucket: str | None, key: str | None = None) -> str | None:
    """
    Creates and returns a S3 URI from the given bucket and key.

    :param bucket: a bucket name (optional).
    :param key: a key (optional).
    :return: None if the bucket is None, else a S3 URI string.
    """
    if bucket is None:
        return None
    return f"s3://{bucket}/{key if key is not None else ''}"


S3_URI_PATTERN = re.compile(r's3://(?P<bucket>.+?)/(?P<key>.+)')
S3_URI_BUCKET_PATTERN = re.compile(r's3://(?P<bucket>.+?)/')

class S3StorageClassMixin:
    """
    Mixin for adding a storage class property to a desktop object.
    """

    def __init__(self):
        self.__storage_class = S3StorageClass.STANDARD

    @property
    def storage_class(self) -> S3StorageClass:
        """The AWS S3 storage class of this file. The default value is STANDARD."""
        try:
            return self.__storage_class
        except AttributeError:
            return S3StorageClass.STANDARD

    @storage_class.setter
    def storage_class(self, storage_class: S3StorageClass):
        if storage_class is None:
            self.__storage_class = S3StorageClass.STANDARD
        elif isinstance(storage_class, S3StorageClass):
            self.__storage_class = storage_class
        else:
            try:
                self.__storage_class = S3StorageClass[str(storage_class)]
            except KeyError:
                raise ValueError(f'Invalid storage class {storage_class}')

    def set_storage_class_from_str(self, storage_class: Optional[str]):
        """
        Sets the storage class property to the storage class corresponding to the provided string. A None value will
        result in the storage class being set to STANDARD.
        """
        if storage_class is None:
            self.__storage_class = S3StorageClass.STANDARD
        else:
            try:
                self.__storage_class = S3StorageClass[str(storage_class)]
            except KeyError:
                raise ValueError(f'Invalid storage class {storage_class}')
