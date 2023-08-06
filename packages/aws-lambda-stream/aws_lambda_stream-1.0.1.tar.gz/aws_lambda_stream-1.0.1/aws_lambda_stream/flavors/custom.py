from reactivex import Observable
from aws_lambda_stream.utils.faults import faulty
from aws_lambda_stream.filters import out_source_is_self
from aws_lambda_stream.utils.filters import on_event_type
from aws_lambda_stream.utils.operators import tap
from aws_lambda_stream.utils.operators import rx_filter, rx_map


def custom_pipeline(rule):
    def wrapper(source: Observable):
        return source.pipe(
            rx_filter(out_source_is_self),
            rx_filter(on_event_type(rule)),
            rx_map(faulty(rule['action'](rule))),
            tap(lambda uow: rule['logger'].info(uow)) # pylint: disable=unnecessary-lambda
        )
    return wrapper
