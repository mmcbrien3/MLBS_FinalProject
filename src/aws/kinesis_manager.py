import boto3
import json
import uuid
import time
import src.ml.match

class KinesisManager(object):

    def __init__(self):

        self.client = boto3.client('kinesis')
        self.stream_name = None
        self.shard_iterator = None

    def create_stream(self, stream_name, shard_count=1):
        self.stream_name = stream_name + str(uuid.uuid4())
        self.client.create_stream(StreamName=self.stream_name, ShardCount=shard_count)

        stream_not_active = True
        while stream_not_active:
            summary = self.client.describe_stream_summary(StreamName=self.stream_name)
            stream_not_active = 'ACTIVE' != summary['StreamDescriptionSummary']['StreamStatus']

        self.shard_iterator = self._get_shard_iterator()

    def delete_stream(self):

        self.client.delete_stream(StreamName=self.stream_name)

    def read_next_n_records(self, n):

        output_dict = {}
        records_read = 0
        any_records_received = False
        iterations_since_last_received = 0
        while records_read < n:
            get_records_response = self.client.get_records(ShardIterator=self.shard_iterator, Limit=5000)
            records = get_records_response['Records']

            self.shard_iterator = get_records_response['NextShardIterator'] \
                if len(records) > 0 else self.shard_iterator

            output_dict = self._handle_records(records, output_dict)

            records_read += len(records)

            if len(records) > 0:
                print('Read {} records from kinesis...'.format(records_read))
                any_records_received = True
                iterations_since_last_received = 0
            else:
                iterations_since_last_received += 1

            if any_records_received and iterations_since_last_received > 4:
                print('terminating early due to no recent records')
                break

            time.sleep(0.25)

        return output_dict

    def _handle_records(self, records, output_dict):
        for r in records:
            output_dict = self._handle_single_record(r, output_dict)

        return output_dict

    def _handle_single_record(self, record, output_dict):
        data = json.loads(record['Data'].decode('utf-8'))

        if data['left_uuid'] not in output_dict:
            output_dict[data['left_uuid']] = data['performances'][0]
        else:
            output_dict[data['left_uuid']] += data['performances'][0]

        if data['right_uuid'] not in output_dict:
            output_dict[data['right_uuid']] = data['performances'][1]
        else:
            output_dict[data['right_uuid']] += data['performances'][1]

        return output_dict

    def _get_shard_iterator(self):
        shard_id = self._get_shard_id()
        return self.client.get_shard_iterator(StreamName=self.stream_name,
                                       ShardId=shard_id,
                                       ShardIteratorType='TRIM_HORIZON')['ShardIterator']


    def _get_shard_id(self):
        shards = self.client.list_shards(StreamName=self.stream_name)
        return shards['Shards'][0]['ShardId']

if __name__ == "__main__":
    km = KinesisManager()
    try:
        km.create_stream('ktest')
    except:
        pass
    km.read_next_n_records(2)