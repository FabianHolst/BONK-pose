# 6D pose estimation dataset

This folder contains a draft of how the final 6D pose estimation dataset could look like. THIS CAN BE SUBJECT TO CHANGE

Files are associated by their name between folders.
- calib: contains the intrinsic camera matrix, can be used to transform pose into pixel values as visualisation of the annotation. Read via 'np.loadtxt'
- image: The image, read via PIL Image.open
- label: The annotations per image, List of vessel objects