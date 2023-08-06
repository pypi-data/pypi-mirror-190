import os
import typing as t

from sarus_data_spec import typing as st
from sarus_data_spec.manager.asyncio.private_manager import PrivateManager
from sarus_data_spec.manager.asyncio.worker.arrow_computation import (
    ToArrowComputation,
)
from sarus_data_spec.manager.asyncio.worker.cache_scalar_computation import (
    CacheScalarComputation,
)
from sarus_data_spec.manager.asyncio.worker.caching_computation import (
    ToParquetComputation,
    ToSQLComputation,
)
from sarus_data_spec.manager.asyncio.worker.schema_computation import (
    SchemaComputation,
)
from sarus_data_spec.manager.asyncio.worker.sql_computation import (
    SQLComputation,
)
from sarus_data_spec.manager.asyncio.worker.value_computation import (
    ValueComputation,
)
from sarus_data_spec.manager.asyncio.worker.worker_computation import (
    WorkerComputation,
)
from sarus_data_spec.manager.ops.asyncio.foreign_keys import fk_visitor
from sarus_data_spec.manager.ops.asyncio.primary_keys import pk_visitor
from sarus_data_spec.manager.ops.asyncio.processor.routing import (
    TransformedDataset,
)
from sarus_data_spec.manager.ops.asyncio.source.routing import (
    source_dataset_schema,
)
from sarus_data_spec.storage.typing import Storage
import sarus_data_spec.protobuf as sp
import sarus_data_spec.storage.typing as storage_typing

try:
    from sarus_data_spec.manager.asyncio.worker.bounds_computation import (
        BoundsComputation,
    )
    from sarus_data_spec.manager.asyncio.worker.links_computation import (
        LinksComputation,
    )
    from sarus_data_spec.manager.asyncio.worker.marginals_computation import (
        MarginalsComputation,
    )
    from sarus_data_spec.manager.asyncio.worker.size_computation import (
        SizeComputation,
    )
except Exception:
    pass


computation_timeout = os.environ.get('WORKER_COMPUTATION_TIMEOUT', default=600)
computation_max_delay = os.environ.get(
    'WORKER_COMPUTATION_MAX_DELAY', default=10
)


class WorkerManager(PrivateManager):
    """Manager that always executes computations
    in its process"""

    def __init__(
        self, storage: storage_typing.Storage, protobuf: sp.Manager
    ) -> None:
        super().__init__(storage, protobuf)
        self.schema_computation = SchemaComputation(self)
        self.to_arrow_computation = ToArrowComputation(
            self, parquet_computation=ToParquetComputation(self)
        )
        self.to_parquet_computation = ToParquetComputation(self)
        self.cache_scalar_computation = CacheScalarComputation(self)
        self.value_computation = ValueComputation(
            self, CacheScalarComputation(self)
        )
        try:
            self.sql_computation = SQLComputation(self, ToSQLComputation(self))
            self.to_sql_computation = ToSQLComputation(self)
            self.size_computation = SizeComputation(self)
            self.bounds_computation = BoundsComputation(self)
            self.marginals_computation = MarginalsComputation(self)
            self.links_computation = LinksComputation(self)

        except Exception:
            pass

    def dataspec_computation(
        self, dataspec: st.DataSpec, sql: bool = False
    ) -> WorkerComputation:
        """Return the computation for a DataSpec."""
        proto = dataspec.prototype()
        if proto == sp.Dataset:
            if sql:
                return self.sql_computation
            return self.to_arrow_computation
        return self.value_computation

    async def async_schema(self, dataset: st.Dataset) -> st.Schema:
        """reads schema of a dataset asynchronously"""
        return await self.schema_computation.task_result(dataspec=dataset)

    async def async_to_parquet(self, dataset: st.Dataset) -> None:
        await self.to_parquet_computation.complete_task(dataspec=dataset)

    async def async_to_sql(self, dataset: st.Dataset) -> None:
        await self.to_sql_computation.complete_task(dataspec=dataset)

    async def async_cache_scalar(self, scalar: st.Scalar) -> None:
        await self.cache_scalar_computation.complete_task(dataspec=scalar)

    async def async_size(self, dataset: st.Dataset) -> st.Size:
        if not dataset.is_transformed():
            raise NotImplementedError(
                'Sizes cannot be computed on source dataset'
            )
        if dataset.transform().name() not in [
            'budget_assignment',
            'Filter',
            'get_item',
            'Project',
            'DifferentiatedSample',
            'Sample',
        ]:
            raise NotImplementedError(
                f'Sizes cannot be computed for dataset '
                f'transformed by {dataset.transform().name()}'
            )

        return await self.size_computation.task_result(dataset)

    async def async_bounds(self, dataset: st.Dataset) -> st.Bounds:
        if not dataset.is_transformed():
            raise NotImplementedError(
                'Bounds cannot be computed on source dataset'
            )

        if dataset.transform().name() not in [
            'budget_assignment',
            'Filter',
            'get_item',
            'Project',
            'Shuffle',
            'DifferentiatedSample',
            'Sample',
        ]:
            raise NotImplementedError(
                f'Bounds cannot be computed for dataset'
                f' transformed by {dataset.transform().name()}'
            )

        return await self.bounds_computation.task_result(dataset)

    async def async_marginals(self, dataset: st.Dataset) -> st.Marginals:
        if not dataset.is_transformed():
            raise NotImplementedError(
                'Marginals cannot be computed on source dataset'
            )

        if dataset.transform().name() not in [
            'budget_assignment',
            'Filter',
            'get_item',
            'Project',
            'Shuffle',
            'DifferentiatedSample',
            'Sample',
        ]:
            raise NotImplementedError(
                f'Marginals cannot be computed for dataset'
                f' transformed by {dataset.transform().name()}'
            )
        return await self.marginals_computation.task_result(dataset)

    async def async_schema_op(self, dataset: st.Dataset) -> st.Schema:
        if dataset.is_transformed():
            return await TransformedDataset(dataset).schema()
        return await source_dataset_schema(dataset=dataset)

    async def async_foreign_keys(
        self, dataset: st.Dataset
    ) -> t.Dict[st.Path, st.Path]:
        """Gets foreign keys from the schema"""
        schema = await self.async_schema(dataset)
        return fk_visitor(schema.type())

    async def async_primary_keys(self, dataset: st.Dataset) -> t.List[st.Path]:
        """Gets primary keys from the schema"""
        return pk_visitor((await self.async_schema(dataset)).type())

    async def async_links(self, dataset: st.Dataset) -> t.Any:
        return await self.links_computation.task_result(dataset)

    def computation_timeout(self, dataspec: st.DataSpec) -> int:
        if dataspec.is_transformed() and dataspec.transform().name() in [
            'User Settings',
            'automatic_user_settings',
            'Protect',
        ]:
            return 5 * int(computation_timeout)
        return int(computation_timeout)

    def computation_max_delay(self, dataspec: st.DataSpec) -> int:
        return int(computation_max_delay)

    def sql_pushing_schema_prefix(self, dataset: st.Dataset) -> str:
        return 'st51_'


def manager(storage: Storage, **kwargs: str) -> WorkerManager:
    properties = {'type': 'worker_manager'}
    properties.update(kwargs)
    return WorkerManager(storage, sp.Manager(properties=properties))
