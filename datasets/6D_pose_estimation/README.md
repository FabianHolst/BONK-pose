# 6D pose estimation dataset

This folder contains two sample images from the dataset. The files-structure is the same as the complete dataset.

Files are associated by their name between folders.
- calib: contains the intrinsic camera matrix, can be used to transform pose into pixel values as visualization of the annotation. Read via 'np.loadtxt'
- image: The image, read via PIL Image.open
- label: The annotations per image, List of vessel objects

The top level contains the images with visualized annotations. These are not part of the dataset, but they can be created from it with no auxiliary data. 

VisualizeDataset.py can be used to create these visualizations and also provide a starting point on how to load and use the dataset.

## Commented annotation
```json
{
    "objects": [ // List of all 3D objects found by our approach
        {
            "identifier": "16d85289b2ac78f0", // Identifier for the vessel. Derived from AIS name, should be consistent across dataset
            "bbImage2d": [ // The 2D BB prediction of the Object detector that was matched with the AIS data.
                1178.287109375,
                808.1433715820312,
                1507.4140625,
                954.7300415039062
            ],
            "height": 8, // Object height, approximated by our approach
            "width": 7, // Object width, from AIS
            "length": 19, // Object length, from AIS
            "position": {
                "centroid": [8.404038544480727, -2.8828951527907876, 357.62172860078886], // Centroid of the object in camera space. Unit is meters.
                "eulerAngles": [[0.26530433473635484], [2.1583877413373616], [-1.9853862977887418]] // Actually axis angle representation, used to encode the object axis in world space. See visualization script for correct interpretation.
            }
        }
    ],
    "2d_annotation_gt": [ // When the image is among those we manually created 2D annotations for, the 2D coco style annotations are linked here. The category_ids are our own, see the 2D dataset or our paper for details.
    // Is None if the image has no 2D ground truth.
        {
            "id": 2567,
            "image_id": 590,
            "category_id": 0,
            "segmentation": [],
            "bbox": [
                1187.4586605626935,
                862.7989087495521,
                321.0413185300465,
                94.42391721472032
            ],
            "ignore": 0,
            "iscrowd": 0,
            "area": 30313.978883385767
        },
        {
            "id": 2568,
            "image_id": 590,
            "category_id": 0,
            "segmentation": [],
            "bbox": [
                1067.4847422192872,
                661.7315085629148,
                192.1804432723116,
                49.98913264308689
            ],
            "ignore": 0,
            "iscrowd": 0,
            "area": 9606.93367014682
        },
        {
            "id": 2569,
            "image_id": 590,
            "category_id": 0,
            "segmentation": [],
            "bbox": [
                1287.4369258488662,
                506.20976256219893,
                168.8521813722068,
                211.0652267152561
            ],
            "ignore": 0,
            "iscrowd": 0,
            "area": 35638.82394269037
        },
        {
            "id": 2570,
            "image_id": 590,
            "category_id": 2,
            "segmentation": [],
            "bbox": [
                1119.695614090953,
                491.7684575764184,
                205.5108786438043,
                177.73913828653244
            ],
            "ignore": 0,
            "iscrowd": 0,
            "area": 36527.32647865792
        },
        {
            "id": 2571,
            "image_id": 590,
            "category_id": 3,
            "segmentation": [],
            "bbox": [
                807.5412524752356,
                286.2575789326184,
                1056.4370031905692,
                282.160882029868
            ],
            "ignore": 0,
            "iscrowd": 0,
            "area": 298085.19662924146
        }
    ],
    "vessels": [ // The AIS based vessel state we used for our matching algorithm. Contains all vessels near the camera that emitted enough AIS to derive a vessel state for.
        {
            "identifier": "16d85289b2ac78f0", // The identifier for the vessel that is also used in the objects list. Based on the MMSI
            "lat": 53.53972, // Last broadcasted location ping of the vessel before the image was taken
            "long": 9.980115,
            "heading": 112, // Last broadcasted heading of the vessel before the image was taken
            "size": { // AIS broadcasted vessel dimensions
                "to_stern": 11,
                "to_bow": 8,
                "to_starboard": 3,
                "to_port": 4
            },
            "speed": 9.7,  // Last broadcasted speed of the vessel before the image was taken
            "secondsSinceLastPositionReport": 1.5150599999997212 // The age of the dynamic vessel information (lat, long, heading, speed) at the time the picture was taken.
        }
    ]
}
```