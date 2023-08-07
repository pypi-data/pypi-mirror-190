import setuptools


setuptools.setup(
    name="comm_ddp",
    version="0.0.2",
    author="Chaoyi Zhang",
    description="communication tools for pytorch-DDP",
    packages=['comm_ddp'], 
    long_description='communication tools for pytorch-DDP (single-node with multi-gpus). See more details as in https://github.com/chaoyivision/comm_ddp.'
)