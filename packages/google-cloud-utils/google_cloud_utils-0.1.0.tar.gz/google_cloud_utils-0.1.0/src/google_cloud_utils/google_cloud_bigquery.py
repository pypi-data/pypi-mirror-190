import io
import json
import bigquery
import datetime
from dotenv import load_dotenv
from google.api_core.exceptions import BadRequest
from bigquery_schema_generator.generate_schema import SchemaGenerator

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code this line is to test if we can push things that are longer than that of 88 lines ?"""
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))

def convert_to_jsonl(json_object):
    jsonl_object = ""
    for entry in json_object:
        jsonl_object += json.dumps(entry, default=json_serial) + "\n"
    return jsonl_object

def generate_bq_schema(jsonl_object, quoted_values_are_strings=True):
    generator = SchemaGenerator(
        input_format="json",
        keep_nulls=True,
        quoted_values_are_strings=quoted_values_are_strings,
        preserve_input_sort_order=True,
    )
    output_file=io.StringIO()
    generator.run(
        input_file=io.StringIO(jsonl_object),
        output_file=output_file,
    )
    output_file.seek(0)
    return json.load(output_file)

class BigQuery :
    def __init__(
        self, bq_project, bq_dataset, bq_dataset_location, credentials, logger=None, ts=None,
    ) -> None:
        self.bq_project = bq_project
        self.bq_dataset = bq_dataset
        self.bq_dataset_location = bq_dataset_location
        self.__credentials = credentials
        self.bq_client = bigquery.Client(
            project=self.bq_project, credentials=self.__credentials
        )
        self.logger = logger
        self.ts = ts

    def load_to_bq(
            self, bq_table, schema_object, data_jsonl_object, write_disposition=bigquery.WriteDisposition.WRITE_APPEND
        ):
        load_dotenv()
        # Configures the load job to append the data to the destination table,
        # allowing field addition
        job_config = bigquery.LoadJobConfig()
        job_config.write_disposition = write_disposition
        job_config.schema_update_options = [
            bigquery.SchemaUpdateOption.ALLOW_FIELD_ADDITION
        ]
        # In this example, the existing table contains only the 'full_name' column.
        # 'REQUIRED' fields cannot be added to an existing schema, so the
        # additional column must be 'NULLABLE'.
        job_config.schema = schema_object
        job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
        job_config.autodetect = False
        ########
        dataset_ref = self.bq_client.dataset(self.bq_dataset)
        table_ref = dataset_ref.table(bq_table)
        job = self.bq_client.load_table_from_file(
            io.StringIO(data_jsonl_object),
            table_ref,
            location=self.bq_dataset_location,
            project=self.bq_project,
            job_config=job_config,
        )
        try:
            job.result()
        except BadRequest as e:
            tmp_list = []
            for e in job.errors:
                tmp_list.append(e["message"])
            if self.logger is not None:
                self.logger.error(
                    json.dumps(
                        {"ts": self.ts, "message": "BQ load failed.", "error": tmp_list}
                    )
                )
            else:
                print(f"ts: {self.ts}; BQ LOAD ERROR: {tmp_list}")
            return "BQ_LOAD_FAILED"
        return "BQ_LOAD_SUCCESS"
