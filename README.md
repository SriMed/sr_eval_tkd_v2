# Evaluating Taekwondo Moves

Following modules from Bianco & Tisato's 2013 article "Karate Moves Recognition from Skeletal Motion" - Skeleton Recognition, Pose Classification, Temporal Alignment, & Scoring

##Skeleton Recognition

System estimates 3D coordinates of body joints from one video source through [Facebook’s VideoPose3D](https://github.com/facebookresearch/VideoPose3D) model.

##Pose Classification

System classifies performed video into key poses (ex. A front kick has three parts: knee-up/chamber, extension, re-chamber) through K-nearest neighbors algorithm.

##Temporal Alignment &  Scoring

System compares performed sequence of poses to exemplar poses with Dynamic Time Warping and outputs similarity score as evaluation.