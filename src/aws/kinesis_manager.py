import boto3
import botocore.errorfactory
import base64
import json

class KinesisManager(object):

    def __init__(self):

        self.client = boto3.client('kinesis')
        self.stream_name = None

    def create_stream(self, stream_name, shard_count=1):
        self.stream_name = stream_name
        self.client.create_stream(StreamName=self.stream_name, ShardCount=shard_count)

    def delete_stream(self):

        self.client.delete_stream(StreamName=self.stream_name)

    def read_next_n_records(self, n):

        output_dict = {}
        shard_iterator = self._get_shard_iterator()
        records_read = 0
        while records_read < n:
            get_records_response = self.client.get_records(ShardIterator=shard_iterator, Limit=5000)
            records = get_records_response['Records']
            shard_iterator = get_records_response['NextShardIterator']
            output_dict = self._handle_records(records, output_dict)

            records_read += len(records)

        return output_dict

    def _handle_records(self, records, output_dict):
        for r in records:
            output_dict = self._handle_single_record(r, output_dict)

        return output_dict

    def _handle_single_record(self, record, output_dict):
        data = json.loads(record['Data'].decode('utf-8'))
        if data['left_uuid'] not in output_dict:
            output_dict['left_uuid'] = data['performances'][0]
        else:
            output_dict['left_uuid'] += data['performances'][0]
        if data['right_uuid'] not in output_dict:
            output_dict['right_uuid'] = data['performances'][1]
        else:
            output_dict['right_uuid'] += data['performances'][1]
        return output_dict

    def _get_shard_iterator(self):
        shard_id = self._get_shard_id()
        return self.client.get_shard_iterator(StreamName=self.stream_name,
                                       ShardId=shard_id,
                                       ShardIteratorType='LATEST')['ShardIterator']


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