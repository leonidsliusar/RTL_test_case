from datetime import datetime

from app.core.dal import DBManager, db
from app.core.query import AggregateManger


async def get_data(aggregate_filter: dict, db_manager: DBManager = db) -> dict:
    start_date = datetime.fromisoformat(aggregate_filter.get('dt_from'))
    end_date = datetime.fromisoformat(aggregate_filter.get('dt_upto'))
    group_type = aggregate_filter.get('group_type')
    aggregator = AggregateManger(start_date, end_date, group_type)
    pipeline = aggregator.pipeline
    doc = await db_manager.aggregate(pipeline)
    date_list = aggregator.date_range
    iso_date_list = [date.strftime('%Y-%m-%dT%H:%M:%S') for date in date_list]
    labels = set(doc.get('labels'))
    dataset = doc.get('dataset')
    i = 0
    while i < len(iso_date_list):
        if iso_date_list[i] not in labels:
            dataset.insert(i, 0)
        i += 1
    return {'dataset': dataset, 'labels': iso_date_list}
