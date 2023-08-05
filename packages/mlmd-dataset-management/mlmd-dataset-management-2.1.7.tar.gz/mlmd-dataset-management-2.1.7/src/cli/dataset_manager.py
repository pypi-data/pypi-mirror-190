import requests
import json

def get_prediction(execution_id):
    from submodules.analytics_dao.prediction_dao import get_prediction_gen
    gen = get_prediction_gen(execution_id)
    for doc in gen:
        print(doc.to_dict())

def main():
    import sys
    import os
    arg1 = sys.argv[1]
    if arg1 == "get-prediction":
        execution_id = sys.argv[2]
        get_prediction(execution_id)
        return
    if arg1 == "get-execution":
        from submodules.analytics_dao.moap_execution_dao import get_moap_execution
        execution_id = sys.argv[2]
        exe = get_moap_execution(execution_id)
        print(exe)
        return
    if arg1 == "get-dataset":
        dataset_name = sys.argv[2]
        from dataset_manager.dataset_manager import get_dataset
        ds = get_dataset(dataset_name)
        pretty_json = json.dumps(str(ds), indent=4)
        print(pretty_json)
        return
    if arg1 == "list-datasets":
        from dataset_manager.dataset_manager import list_datasets
        datasets =list_datasets()
        pretty_json = json.dumps(datasets, indent=4)
        print(pretty_json)
        return
    if arg1 == "download-dataset":
        dataset_name = sys.argv[2]
        from dataset_manager.dataset_manager import get_dataset
        ds = get_dataset(dataset_name)
        ds.download_to_dir(".")
        return
    if arg1 == "download-images":
        dataset_name = sys.argv[2]
        filelist = sys.argv[3].split(",")
        from dataset_manager.dataset_manager import get_dataset
        ds = get_dataset(dataset_name)
        ds.download_to_dir(".", filelist=filelist)
        return
    print("Unsupport command: {}".format(arg1))

if __name__ == "__main__":
    main()