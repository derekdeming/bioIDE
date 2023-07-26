# import inspect
# import sys
# from .pipelines.abstract_pipeline import AbstractPipeline

# def get_pipeline(database_name: str):
#     subclasses = all_subclasses(AbstractPipeline)
#     pipeline_classes = {cls.__name__.lower(): cls for cls in subclasses}

#     pipeline_class = pipeline_classes.get(database_name.lower())
#     if pipeline_class is None:
#         raise ValueError(f"Unknown database: {database_name}")

#     return pipeline_class()

# def all_subclasses(cls):
#     return set(cls.__subclasses__()).union(
#         [s for c in cls.__subclasses__() for s in all_subclasses(c)]
#     )

# # add more functions or classes here as per existing file
