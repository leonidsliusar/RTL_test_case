from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta


class AggregateManger:
    def __init__(self, start_date: datetime, end_date: datetime, group_type: str):
        self.start = start_date
        self.end = end_date
        self.type = group_type

    @property
    def pipeline(self) -> list:
        pipeline_map = {
            'hour': {
                '$group': {
                    '_id': {'year': {'$year': '$dt'}, 'month': {'$month': '$dt'}, 'day': {'$dayOfMonth': '$dt'},
                            'hour': {'$hour': '$dt'}},
                    'total_value': {'$sum': '$value'},
                    'labels': {
                        '$push': {
                            '$dateToString': {
                                'format': "%Y-%m-%dT%H:00:00",
                                'date': '$dt'
                            }
                        }
                    }
                }
            },
            'day': {
                '$group': {
                    '_id': {'year': {'$year': '$dt'}, 'month': {'$month': '$dt'}, 'day': {'$dayOfMonth': '$dt'}},
                    'total_value': {'$sum': '$value'},
                    'labels': {
                        '$push': {
                            '$dateToString': {
                                'format': "%Y-%m-%dT00:00:00",
                                'date': '$dt'
                            }
                        }
                    }
                },
            },
            'week': {
                '$group': {
                    '_id': {'year': {'$year': '$dt'}, 'week': {'$isoWeek': '$dt'}},
                    'total_value': {'$sum': '$value'},
                    'labels': {
                        '$push': {
                            '$dateToString': {
                                'format': "%Y-%wT00:00:00",
                                'date': '$dt'
                            }
                        }
                    }
                }
            },
            'month': {
                '$group': {
                    '_id': {'year': {'$year': '$dt'}, 'month': {'$month': '$dt'}},
                    'total_value': {'$sum': '$value'},
                    'labels': {'$push': {
                        '$dateToString': {
                            'format': "%Y-%m-01T00:00:00",
                            'date': {
                                '$dateFromParts': {
                                    'year': {'$year': '$dt'},
                                    'month': {'$month': '$dt'},
                                    'day': 1
                                }
                            }
                        }
                    }}
                }}
        }
        pipeline = [
            {'$match': {
                'dt': {'$gte': self.start, '$lte': self.end}
            }},
            pipeline_map.get(self.type),
            {'$sort': {
                '_id.year': 1,
                '_id.month': 1,
                '_id.day': 1,
                '_id.hour': 1
            }},
            {'$group': {
                '_id': None,
                'dataset': {'$push': '$total_value'},
                'labels': {'$push': {'$first': '$labels'}},
            }},
            {'$project': {
                '_id': 0,
                'dataset': 1,
                'labels': 1,
            }
            }]
        return pipeline

    @property
    def month(self) -> list:
        date_list_month = []
        current_date = self.start
        while current_date <= self.end:
            date_list_month.append(current_date)
            current_date += relativedelta(months=1)
        return date_list_month

    @property
    def date_range(self) -> list:
        agr_map = {
            'hour': [self.start + timedelta(hours=x) for x in
                     range(int((self.end - self.start).total_seconds() / 3600) + 1)],
            'day': [self.start + timedelta(days=x) for x in range((self.end - self.start).days + 1)],
            'week': [self.start + timedelta(weeks=x) for x in range(int(((self.end - self.start).days) / 7) + 1)],
            'month': self.month
        }
        return agr_map.get(self.type)
