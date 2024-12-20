#!/usr/bin/env python3
import pymongo
from bson import ObjectId
import datetime
import typing

from ..mongo import MongoConfig
from abc import ABC, abstractmethod


class Base(ABC):
    @abstractmethod
    def fieldsChecker(self, **kwargs) -> bool:
        pass

    def __init__(self, **kwargs):

        try:
            self.collection = MongoConfig.db[self.__class__.__name__.lower()]
            if 'index' in kwargs.keys():
                for index in kwargs['index']:
                    self.collection.create_index(index, unique=True)
        except Exception as e:
            raise ValueError(e)

    def create(self, **kwargs) -> str:

        if not self.fieldsChecker(kwargs):
            raise AttributeError('data invalid !!!')

        kwargs['_id'] = str(ObjectId())
        kwargs['createdAt'] = kwargs['updatedAt'] = datetime\
            .datetime.now().isoformat()

        try:
            res = self.collection.insert_one(kwargs)
            return res.inserted_id
        except Exception as e:
            raise ValueError(e)

    def get(self, id: str = None, **kwargs) -> typing.Dict | typing.List:

        try:
            if id:
                res = self.collection.find_one({'_id': id})
                if not res:
                    raise ValueError('data not found')
                return dict(res)
            else:
                page = kwargs.get('page', 1)
                offset = (page - 1) * kwargs.get('limit', 10)
                limit = kwargs.get('limit', 10)
                sort_field = kwargs.get('sort', 'created_at')
                sort_dir = pymongo.DESCENDING\
                    if kwargs.get('desc', True) else pymongo.ASCENDING

                if 'page' in kwargs.keys():
                    del kwargs['page']

                if 'limit' in kwargs.keys():
                    del kwargs['limit']

                if 'sort' in kwargs.keys():
                    del kwargs['sort']

                res = self.collection.find(kwargs)\
                                     .skip(offset)\
                                     .limit(limit)\
                                     .sort(sort_field, sort_dir)

                totalItems = self.count(**kwargs)
                hasPrevPage = page > 1
                hasNextPage = (offset + limit) < totalItems
                prevPage = page - 1 if hasPrevPage else None
                nextPage = page + 1 if hasNextPage else None
                totalPages = totalItems // limit
                pagingCounter = offset + 1

                return dict(
                    values=list(res),
                    pagination=dict(
                        totalItems=totalItems,
                        limit=limit,
                        page=page,
                        totalPages=totalPages,
                        pagingCounter=pagingCounter,
                        hasPrevPage=hasPrevPage,
                        hasNextPage=hasNextPage,
                        prevPage=prevPage,
                        nextPage=nextPage
                    )
                )
        except Exception as e:
            raise ValueError(e)

    def update(self, id: str, **kwargs) -> bool:

        if '_id' in kwargs.keys():
            del kwargs['_id']

        if 'createdAt' in kwargs.keys():
            del kwargs['createdAt']

        if 'updatedAt' in kwargs.keys():
            del kwargs['updatedAt']

        if not self.fieldsChecker(kwargs):
            raise AttributeError('data invalid !!!')

        if not self.get(id):
            raise ValueError('data not found')

        try:
            res = self.collection.update_one(
                {'_id': id},
                {
                    '$set': kwargs,
                    '$currentDate': {'updatedAt': True}
                }
            )
            return True if res.modified_count > 0 else False
        except Exception as e:
            raise ValueError(e)

    def delete(self, id: str, **kwargs) -> bool:

        if not self.get(id):
            raise ValueError('data not found')

        try:
            res = self.collection.delete_one({'_id': id})
            return True if res.deleted_count > 0 else False
        except Exception as e:
            raise ValueError(e)

    def count(self, **kwargs) -> int:
        try:
            res = self.collection.count_documents(kwargs)
            return res
        except Exception as e:
            raise ValueError(e)
