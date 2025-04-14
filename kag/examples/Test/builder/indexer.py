# Copyright 2023 OpenSPG Authors
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
# in compliance with the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License
# is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied.

import os

from kag.builder.component.reader import DocxReader, PDFReader
from kag.builder.component.splitter import LengthSplitter, OutlineSplitter
from knext.builder.builder_chain_abc import BuilderChainABC
from kag.builder.component.extractor import KAGExtractor
from kag.builder.component.vectorizer.batch_vectorizer import BatchVectorizer
from kag.builder.component.writer import KGWriter
from kag.solver.logic.solver_pipeline import SolverPipeline

import logging
from kag.common.env import init_kag_config

file_path = os.path.dirname(__file__)

suffix_mapping = {
    "docx": DocxReader,
    "pdf": PDFReader
}



class TestBuildChain(BuilderChainABC):
    def build(self, **kwargs):
        file_path = kwargs.get("file_path")
        suffix = file_path.split(".")[-1]


        # 读取文档
        reader = suffix_mapping[suffix]()
        if reader is None:
            raise NotImplementedError
        project_id = int(os.getenv("KAG_PROJECT_ID"))
        
        # 分割文档，chunck
        splitter = LengthSplitter(split_length=2000)
        #  关键组件，实现了从非结构化文本到结构化知识图谱的自动创建
        extractor = KAGExtractor(project_id=project_id)
        # embedding
        vectorizer = BatchVectorizer()
        # 写入到数据库
        writer = KGWriter()
        # 这个其实是每次处理一个chunk的过程
        chain = reader >> extractor >> vectorizer >> writer
        return chain
    
def buildKG(test_file,**kwargs):
    chain = TestBuildChain(file_path = test_file)
    chain.invoke(test_file, max_workers=10)
    

if __name__ == "__main__":
    test_file = os.path.join(file_path,"/data/zxx/KAG/kag/examples/Test/builder/data/supermarket.docx")
    buildKG(test_file)
