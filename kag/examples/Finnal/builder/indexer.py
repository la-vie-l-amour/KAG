import os
import copy
from kag.common.conf import KAG_CONFIG
from kag.common.registry import import_modules_from_path
from kag.builder.runner import BuilderChainRunner
from kag.interface import KAGBuilderChain as BuilderChainABC
from kag.builder.component.scanner.csv_scanner import CSVScanner
from kag.builder.component import KGWriter, RelationMapping, SPGTypeMapping
from kag.builder.component.vectorizer.batch_vectorizer import BatchVectorizer


# 处理Diease_applicableFood_Medicine这类文件
class ExplainRelationChain(BuilderChainABC):
    def __init__(self, spg_type_name: str):
        super().__init__()
        self.spg_type_name = spg_type_name

    def build(self, **kwargs):
        subject_name, relation, object_name = self.spg_type_name.split("_")
        self.mapping = (
            RelationMapping(subject_name, relation, object_name)
            .add_src_id_mapping("src")
            .add_dst_id_mapping("dst")
            # 如果边有属性的化可以使用下列的例子，参考riskmining的例子
            # .add_sub_property_mapping("transDate", "transDate")
            # .add_sub_property_mapping("transAmt", "transAmt")
        )
        self.vectorizer = BatchVectorizer.from_config(
            KAG_CONFIG.all_config["chain_vectorizer"]
        )
        self.sink = KGWriter()
        return self.mapping >> self.vectorizer >> self.sink

def import_data():
    pwd = os.path.dirname(__file__)

    # 处理结构化数据HumanBodyPart.csv这些
    spo_runner_config = KAG_CONFIG.all_config["spg_runner"]
    for spg_type_name in ["HumanBodyPart", "HospitalDepart"]:
        runner_config = copy.deepcopy(spo_runner_config)
        runner_config["chain"]["mapping"]["spg_type_name"] = spg_type_name
        file_path = os.path.join(pwd, f"data/{spg_type_name}.csv")
        runner = BuilderChainRunner.from_config(runner_config)
        runner.invoke(file_path)

    # 处理结构化数据 Diease_applicableFood_Medicine.csv
    for spg_type_name in ["Disease_applicableFood_Medicine","Factory_produce_Medicine"]:
        chain = ExplainRelationChain(spg_type_name=spg_type_name)
        runner = BuilderChainRunner(
            scanner=CSVScanner(),
            chain=chain,
        )
        runner.invoke(os.path.join(pwd, f"data/{spg_type_name}.csv"))


    # 处理半结构化数据Diease.csv
    extract_runner_config = KAG_CONFIG.all_config["extract_runner"]
    extract_runner = BuilderChainRunner.from_config(extract_runner_config)
    extract_runner.invoke(os.path.join(pwd, "data/Disease.csv"))

    # 处理 SPO.csv
    spo_runner_config = KAG_CONFIG.all_config["spo_runner"]
    spo_runner = BuilderChainRunner.from_config(spo_runner_config)
    spo_runner.invoke(os.path.join(pwd, "data/SPO.csv"))

    # 处理txt文件
    txt_runner_config = KAG_CONFIG.all_config["kag_builder_pipeline"]
    txt_runner = BuilderChainRunner.from_config(txt_runner_config)
    txt_runner.invoke(os.path.join(pwd, "data/"))
if __name__ == "__main__":
    import_modules_from_path(".")
    import_data()
