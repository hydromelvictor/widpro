#!/usr/bin/env python3
import pymongo
from bson import ObjectId
import datetime
import typing

from ..mongo import MongoConfig


class Base:

    def __init__(self, **kwargs) -> None:
        self.collection = MongoConfig.db[self.__class__.__name__.lower()]

    def fieldsChecker(self, **kwargs) -> bool:
        NotImplementedError('fieldsChecker must be implemented')

    def create(self, **kwargs) -> str:

        if not self.fieldsChecker(kwargs):
            raise AttributeError('data invalid !!!')

        kwargs['_id'] = str(ObjectId())
        kwargs[
            'createdAt'
        ] = kwargs[
            'updatedAt'
        ] = datetime.datetime.now().isoformat()

        res = self.collection.insert_one(kwargs)
        return res.inserted_id

    def findOne(self, key: str, **kwargs) -> typing.Dict:

        res = self.collection.find({'_id': key} | kwargs)
        if not res:
            raise ValueError('data not found')
        return dict(res)

    def find(self, **kwargs) -> typing.List[typing.Dict]:
        page = kwargs.get('page', 1)
        offset = (page - 1) * kwargs.get('limit', 10)
        limit = kwargs.get('limit', 10)
        sort = kwargs.get('sort', 'created_at')

        if 'page' in kwargs.keys():
            del kwargs['page']

        if 'limit' in kwargs.keys():
            del kwargs['limit']

        if 'sort' in kwargs.keys():
            del kwargs['sort']

        res = self.collection.find(kwargs)\
                             .skip(offset)\
                             .limit(limit)\
                             .sort(sort, pymongo.DESCENDING)

        totalItems = self.count()
        hasPrevPage = page > 1
        hasNextPage = (offset + limit) < totalItems
        prevPage = page - 1 if hasPrevPage else None
        nextPage = page + 1 if hasNextPage else None
        totalPages = totalItems // limit
        pagingCounter = offset + 1

        return {
            'values': list(res),
            'pagination': {
                'totalItems': totalItems,
                'limit': limit,
                'page': page,
                'totalPages': totalPages,
                'pagingCounter': pagingCounter,
                'hasPrevPage': hasPrevPage,
                'hasNextPage': hasNextPage,
                'prevPage': prevPage,
                'nextPage': nextPage
            }
        }

    def updateOne(self, key, **kwargs) -> bool:

        if '_id' in kwargs.keys():
            del kwargs['_id']

        if not self.fieldsChecker(kwargs):
            raise AttributeError('data invalid !!!')

        res = self.collection.update_one(
            {'_id': key},
            {
                '$set': kwargs,
                '$currentDate': {'updatedAt': True}
            }
        )
        return True if res.modified_count > 0 else False

    def update(self, keys: typing.List, **kwargs) -> bool:

        assert isinstance(keys, list), f'{keys} must be list'

        if '_id' in kwargs.keys():
            del kwargs['_id']

        if not self.fieldsChecker(kwargs):
            raise AttributeError('data invalid !!!')

        res = self.collection.update_many(
            keys,
            {
                '$set': kwargs,
                '$currentDate': {'updated_at': True}
            }
        )
        return True if res.modified_count > 0 else False

    def deleteOne(self, key) -> pymongo.results.DeleteResult:
        res = self.collection.delete_one({'_id': key})
        return True if res.deleted_count > 0 else False

    def delete(self, **kwargs) -> pymongo.results.DeleteResult:
        res = self.collection.delete_many(kwargs)
        return True if res.deleted_count > 0 else False

    def count(self, **kwargs) -> int:
        return self.collection.count_documents(kwargs)
