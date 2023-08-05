import requests
import json

def get_prediction(execution_id):
    from submodules.analytics_dao.prediction_dao import get_prediction_gen
    gen = get_prediction_gen(execution_id)
    for doc in gen:
        print(doc.to_dict())

def parse_r_detection_label(label, dtype="array_of_objects", filtering_labels=None, filtering_indexes=None):
    try:
        if not label:
            return False
        data = label.split(":")
        predictions = json.loads(data[1])
        labels = json.loads(data[2])
        if len(predictions) <= 0:
            return False
        if dtype == "array_of_objects":
            ret = []
            for idx, prediction in enumerate(predictions):
                if (not filtering_labels or label in filtering_labels) and \
                    (not filtering_indexes or idx in filtering_indexes):
                    label = labels[int(prediction[1])]
                    ret.append({
                        "parent_index": int(prediction[0]),
                        "label_index": prediction[1],
                        "label": label,
                        "score": prediction[2],
                        "coord": prediction[3:]
                    })
        else:
            ret = {"label_indexes":[],"scores":[],"coords":[], "parent_indexes":[], "label":[]}
            for idx, prediction in enumerate(predictions):
                label = labels[int(prediction[1])]
                if (not filtering_labels or label in filtering_labels) and \
                    (not filtering_indexes or idx in filtering_indexes):
                    ret["parent_indexes"].append(int(prediction[0]))
                    ret["label_indexes"].append(prediction[1])
                    ret["label"].append(label)
                    ret["scores"].append(prediction[2])
                    ret["coords"].append(prediction[3:])
        return ret
    except Exception as e:
        print(e)
        return False

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
    if arg1 == "decorate-with-prediction":
        import os
        from PIL import Image, ImageDraw
        dataset_name = sys.argv[2]
        from dataset_manager.dataset_manager import get_dataset
        ds = get_dataset(dataset_name)
        curr_files = os.listdir(".")
        g = ds.get_filelist(get_annotation=True)
        for file_name, annotation in g:
            if file_name in curr_files:
                source_img = Image.open(file_name).convert("RGB")
                draw = ImageDraw.Draw(source_img)
                parsed_annotations = parse_r_detection_label(annotation)
                print(parsed_annotations)
                for idx, ann in enumerate(parsed_annotations['coords']):
                    draw.rectangle(((ann[0], ann[1]), (ann[2], ann[3])), width=3)
                    draw.text((ann[0]+3, ann[1]), parsed_annotations['label'][idx])
                source_img.save(file_name, "JPEG")

        return
    print("Unsupport command: {}".format(arg1))

if __name__ == "__main__":
    main()